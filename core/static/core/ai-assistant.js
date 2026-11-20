document.addEventListener('DOMContentLoaded', () => {
   const aiAssistantVisibilityButton = document.getElementById('aiAssistantVisibilityButton');
   const aiAssistantVisibilityIcon = document.getElementById('aiAssistantVisibilityIcon');
   const aiAssistantWidthButton = document.getElementById('aiAssistantWidthButton');
   const aiAssistantWidthIcon = document.getElementById('aiAssistantWidthIcon');
   const aiAssistantTab = document.getElementById('aiAssistantTab');
   const appearanceTab = document.getElementById('appearanceTab');
   const aiAssistantColumn = document.getElementById('aiAssistantColumn');
   const mainContentColumn = document.getElementById('mainContentColumn');
   const aiAssistantCard = document.getElementById('aiContainer');
   const appearanceContainer = document.getElementById('appearanceContainer');
   const pageContentRow = document.getElementById('pageContentRow');
   const userName = document.getElementById('userName').textContent;
   const chatBox = document.getElementById("chatBox");
   const aiContainer = document.getElementById("aiContainer");
   const chatHistory = sessionStorage.getItem('chatHistory');
   if (chatHistory) { chatBox.value = chatHistory; };
   const chatUserInput = document.getElementById("chatUserInput");
   const sendButton = document.getElementById("sendButton");
   const sendButtonLabel = document.getElementById("aiSendButtonLabel");
   const aiSolveProblemButton = document.getElementById("aiSolveProblemButton");
   const chooseAiModelBtn = document.getElementById("chooseAiModelBtn");
   const chooseAiModelMenu = document.getElementById("chooseAiModelMenu");
   let activeEventSource = null;
   let currentAiStartIndex = null;
   let activeModel = "cohere";
   const assistantWidths = [
      { assistant: "col-md-0", content: "col-md-12" },
      { assistant: "col-md-3", content: "col-md-9" },
      { assistant: "col-md-6", content: "col-md-6" },
   ];
   let assistantWidthIndex = 1;
   let lastVisibleWidthIndex = assistantWidthIndex;
   let activeSidebarPanel = "assistant";
   const appearanceOptions = {
      text: ["small", "standard", "large"],
      width: ["standard", "wide"],
      color: ["automatic", "light", "dark"],
   };
   const appearanceDefaults = { text: "standard", width: "standard", color: "automatic" };

   function updateSidebarPanelVisibility() {
      const assistantVisible =
         assistantWidthIndex !== 0 && activeSidebarPanel === "assistant";
      const appearanceVisible =
         assistantWidthIndex !== 0 && activeSidebarPanel === "appearance";
      aiAssistantCard.classList.toggle("d-none", !assistantVisible);
      appearanceContainer.classList.toggle("d-none", !appearanceVisible);
      appearanceContainer.hidden = !appearanceVisible;
   }

   function selectSidebarPanel(panel) {
      const showAppearance = panel === "appearance";
      activeSidebarPanel = panel;
      updateSidebarPanelVisibility();
      aiAssistantTab.classList.toggle("btn-primary", !showAppearance);
      aiAssistantTab.classList.toggle("btn-outline-secondary", showAppearance);
      aiAssistantTab.setAttribute("aria-selected", String(!showAppearance));
      appearanceTab.classList.toggle("btn-primary", showAppearance);
      appearanceTab.classList.toggle("btn-outline-secondary", !showAppearance);
      appearanceTab.setAttribute("aria-selected", String(showAppearance));
   }

   function setAppearanceOption(setting, value) {
      if (!appearanceOptions[setting].includes(value)) return;
      localStorage.setItem(`appearance${setting[0].toUpperCase()}${setting.slice(1)}`, value);

      if (setting === "text") {
         document.documentElement.classList.remove(
            "appearance-text-small", "appearance-text-large");
         if (value !== "standard") {
            document.documentElement.classList.add(`appearance-text-${value}`);
         }
      } else if (setting === "width") {
         pageContentRow.classList.toggle("appearance-width-standard", value === "standard");
         pageContentRow.classList.toggle("appearance-width-wide", value === "wide");
      } else {
         document.dispatchEvent(new CustomEvent("appearance-color-change", {
            detail: { color: value },
         }));
      }

      document.querySelectorAll(`[data-appearance-setting="${setting}"]`)
         .forEach((input) => { input.checked = input.value === value; });
   }

   for (const [setting, values] of Object.entries(appearanceOptions)) {
      const storageKey = `appearance${setting[0].toUpperCase()}${setting.slice(1)}`;
      const storedValue = localStorage.getItem(storageKey);
      const value = values.includes(storedValue) ? storedValue : appearanceDefaults[setting];
      setAppearanceOption(setting, value);

      document.querySelectorAll(`[data-appearance-setting="${setting}"]`)
         .forEach((input) => {
            input.addEventListener("change", () => {
               if (input.checked) setAppearanceOption(setting, input.value);
            });
         });
   }

   function setAssistantWidth(index) {
      assistantWidthIndex = index;
      if (index !== 0) lastVisibleWidthIndex = index;
      const width = assistantWidths[index];
      aiAssistantColumn.classList.remove(...assistantWidths.map((size) => size.assistant));
      aiAssistantColumn.classList.add(width.assistant);
      mainContentColumn.classList.remove(...assistantWidths.map((size) => size.content));
      mainContentColumn.classList.add(width.content);
      updateSidebarPanelVisibility();
      aiAssistantWidthButton.classList.toggle("d-none", index === 0);
      aiAssistantVisibilityIcon.classList.toggle("fa-indent", index !== 0);
      aiAssistantVisibilityIcon.classList.toggle("fa-outdent", index === 0);
      aiAssistantVisibilityButton.setAttribute("aria-expanded", String(index !== 0));
      aiAssistantVisibilityButton.setAttribute(
         "aria-label", index === 0 ? "Show sidebar" : "Hide sidebar");
      aiAssistantVisibilityButton.title =
         index === 0 ? "Show sidebar" : "Hide sidebar";
      aiAssistantWidthIcon.classList.toggle("fa-expand-alt", index === 1);
      aiAssistantWidthIcon.classList.toggle("fa-compress-alt", index === 2);
      aiAssistantWidthButton.setAttribute(
         "aria-label", index === 1 ? "Extend sidebar" : "Shrink sidebar");
      aiAssistantWidthButton.title =
         index === 1 ? "Extend sidebar" : "Shrink sidebar";
   }

   setAssistantWidth(assistantWidthIndex);

   function appendMessage(role, message) {
      chatBox.value += `\n${role}: ${message}`;
      chatBox.scrollTop = chatBox.scrollHeight;
      sessionStorage.setItem('chatHistory', chatBox.value)
   }

   function appendToLastMessage(text) {
      chatBox.value += text;
      sessionStorage.setItem('chatHistory', chatBox.value)
   }

   function replaceLastAiMessage(finalText) {
      if (currentAiStartIndex === null) return;
      chatBox.value =
         chatBox.value.slice(0, currentAiStartIndex) + `\nAI: ${finalText}`;
      sessionStorage.setItem('chatHistory', chatBox.value)
      currentAiStartIndex = null;
   }

   function getProblemSolvePrompt() {
      const contextElement = document.getElementById("ai-problem-context");
      if (!contextElement) return null;

      try {
         const context = JSON.parse(contextElement.textContent);
         const title = context.title?.trim();
         const description = context.description?.trim();
         const language = context.language?.trim();
         if (!title || !description || !language) return null;

         return `Solve the following programming problem in ${language}. `
            + `Explain the algorithm and its time and space complexity, then provide `
            + `a complete ${language} implementation that matches the required signature.\n\n`
            + `Title: ${title}\n\nProblem:\n${description}`;
      } catch {
         return null;
      }
   }

   // Send a message to the backend. Passing a message sends it without replacing
   // the text currently being composed by the user.
   async function sendMessage(
      message = chatUserInput.value.trim(), clearUserInput = true) {
      if (!message || activeEventSource) return;

      // Show spinner and disable button
      sendButton.disabled = true;
      if (aiSolveProblemButton) aiSolveProblemButton.disabled = true;
      sendButtonLabel.textContent = "Wait";
      document.getElementById('aiSendButtonSpinner').classList.remove("d-none");

      // Add the user's message to the chat box.
      appendMessage(userName, message);
      if (clearUserInput) chatUserInput.value = "";

      currentAiStartIndex = chatBox.value.length;
      appendMessage("AI", "");

      let streamUrl = "";
      streamUrl = `/chat/${activeModel}/stream/?message=${encodeURIComponent(message)}`;
      activeEventSource = new EventSource(streamUrl);

      activeEventSource.onmessage = (event) => {
         appendToLastMessage(event.data);
      };

      activeEventSource.addEventListener("done", (event) => {
         try {
            const payload = JSON.parse(event.data);
            if (payload && typeof payload.final === "string") {
               replaceLastAiMessage(payload.final);
            }
         } catch (e) {
            // If parsing fails, keep the streamed content as-is.
         }
         activeEventSource.close();
         activeEventSource = null;

         // Hide spinner and re-enable button
         sendButton.disabled = false;
         if (aiSolveProblemButton) aiSolveProblemButton.disabled = false;
         sendButtonLabel.textContent = "Send";
         document.getElementById('aiSendButtonSpinner').classList.add('d-none');
      });

      activeEventSource.onerror = () => {
         if (activeEventSource) {
            activeEventSource.close();
            activeEventSource = null;
         }
         appendMessage("AI", "Error: Could not get a streamed response.");
         sendButton.disabled = false;
         if (aiSolveProblemButton) aiSolveProblemButton.disabled = false;
         sendButtonLabel.textContent = "Send";
         document.getElementById('aiSendButtonSpinner').classList.add('d-none');
      };
   }

   sendButton.addEventListener('click', sendMessage);
   if (aiSolveProblemButton) {
      aiSolveProblemButton.addEventListener('click', () => {
         const prompt = getProblemSolvePrompt();
         if (!prompt) return;
         if (assistantWidthIndex === 0) {
            setAssistantWidth(1);
         }
         sendMessage(prompt, false);
      });
   }
   chatUserInput.addEventListener('keydown', (event) => {
      if (event.key !== 'Enter') return;
      if (event.shiftKey) return;
      event.preventDefault();
      sendMessage();
   });

   if (chooseAiModelMenu) {
      chooseAiModelMenu.addEventListener("click", (event) => {
         const item = event.target.closest("[data-model]");
         if (!item) return;
         activeModel = item.getAttribute("data-model") || "cohere";
         const label = item.textContent.trim() || "Model";
         if (chooseAiModelBtn) {
            chooseAiModelBtn.textContent = label;
         }
      });
   }

   aiAssistantVisibilityButton.addEventListener('click', () => {
      setAssistantWidth(
         assistantWidthIndex === 0 ? lastVisibleWidthIndex : 0);
   });

   aiAssistantTab.addEventListener("click", () => selectSidebarPanel("assistant"));
   appearanceTab.addEventListener("click", () => selectSidebarPanel("appearance"));
   [aiAssistantTab, appearanceTab].forEach((tab, index) => {
      tab.addEventListener("keydown", (event) => {
         const nextTab = event.key === "ArrowRight" || event.key === "ArrowDown"
            ? 1 - index
            : event.key === "ArrowLeft" || event.key === "ArrowUp"
               ? 1 - index
               : event.key === "Home" ? 0
                  : event.key === "End" ? 1 : null;
         if (nextTab === null) return;
         event.preventDefault();
         const tabs = [aiAssistantTab, appearanceTab];
         tabs[nextTab].focus();
         selectSidebarPanel(nextTab === 1 ? "appearance" : "assistant");
      });
   });

   aiAssistantWidthButton.addEventListener('click', () => {
      setAssistantWidth(assistantWidthIndex === 1 ? 2 : 1);
   });

   const autoResize = (element) => {
      element.style.height = 'auto';
      element.style.height = element.scrollHeight + 'px';
   };

   chatUserInput.addEventListener('input', () => autoResize(chatUserInput));
});
