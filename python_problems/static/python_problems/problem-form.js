document.addEventListener("DOMContentLoaded", () => {
   const problemTypeField = document.getElementById("id_problem_type");
   const methodNameField = document.getElementById("id_method_name");
   const argumentNamesField = document.getElementById("id_argument_names");

   if (!problemTypeField || !methodNameField || !argumentNamesField) {
      return;
   }

   function syncProblemTypeFields() {
      const shouldDisable = problemTypeField.value === "class";

      methodNameField.disabled = shouldDisable;
      argumentNamesField.disabled = shouldDisable;
   }

   syncProblemTypeFields();
   problemTypeField.addEventListener("change", syncProblemTypeFields);
});
