document.addEventListener('DOMContentLoaded', () => {
   const aiAssistantButton = document.getElementById('aiAssistantButton');
   const userName = document.getElementById('userName').textContent;
   const chatBox = document.getElementById("chatBox");
   const aiContainer = document.getElementById("aiContainer");
   const chatHistory = sessionStorage.getItem('chatHistory');
   if (chatHistory) { chatBox.value = chatHistory; };
   const chatUserInput = document.getElementById("chatUserInput");
   const sendButton = document.getElementById("sendButton");
   const chooseAiModelBtn = document.getElementById("chooseAiModelBtn");
   const chooseAiModelMenu = document.getElementById("chooseAiModelMenu");
   let activeEventSource = null;
   let currentAiStartIndex = null;
   let activeModel = "cohere";

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

   // Send a message to the backend.
   async function sendMessage() {
      const message = chatUserInput.value.trim();
      if (!message) return;

      // Show spinner and disable button
      sendButton.disabled = true;
      sendButton.firstChild.textContent = "Wait ";
      document.getElementById('aiSendButtonSpinner').classList.remove("d-none");

      // Add the user's message to the chat box.
      appendMessage(userName, message);
      chatUserInput.value = "";

      currentAiStartIndex = chatBox.value.length;
      appendMessage("AI", "");

      const cerberasModels = new Set(["gpt", "zai", "llama", "qwen"]);
      let streamUrl = "";
      if (cerberasModels.has(activeModel)) {
         streamUrl = `/chat/cerberas/stream/?model_name=${encodeURIComponent(activeModel)}&message=${encodeURIComponent(message)}`;
      } else {
         streamUrl = `/chat/${activeModel}/stream/?message=${encodeURIComponent(message)}`;
      }
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
         sendButton.firstChild.textContent = "Send";
         document.getElementById('aiSendButtonSpinner').classList.add('d-none');
      });

      activeEventSource.onerror = () => {
         if (activeEventSource) {
            activeEventSource.close();
            activeEventSource = null;
         }
         appendMessage("AI", "Error: Could not get a streamed response.");
         sendButton.disabled = false;
         sendButton.firstChild.textContent = "Send";
         document.getElementById('aiSendButtonSpinner').classList.add('d-none');
      };
   }

   sendButton.addEventListener('click', sendMessage);
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
            chooseAiModelBtn.textContent = `Model: ${label}`;
         }
      });
   }

   aiAssistantButton.addEventListener('click', () => {
      aiContainer.classList.toggle("d-none");
   });

   const autoResize = (element) => {
      element.style.height = 'auto';
      element.style.height = element.scrollHeight + 'px';
   };

   chatUserInput.addEventListener('input', () => autoResize(chatUserInput));
});
