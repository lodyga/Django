# Run, remember all textarea and append in every Run

<form id="code_form_id" action="{% url 'python_problems:detail' problem.id %}" method="POST" class="mb-5">
  {% csrf_token %}
  <div class="code-area-container mb-2">
    <label for="id_code_area">Code Area</label>
    <textarea name="code_area" id="id_code_area" cols="80" rows="10" class="python-code" required>{{ code_form.code_area }}</textarea>
  </div>
  <button id="submitButton" type="submit" class="btn btn-warning">
    Run
  </button>
</form>

<script>
  // Function to initialize CodeMirror
  function initializeCodeMirror() {
    var editor = CodeMirror.fromTextArea(document.getElementById("id_code_area"), {
      mode: "python",
      lineNumbers: true,
      autofocus: true
    });

    // Hide the original textarea after CodeMirror initialization
    document.getElementById("id_code_area").style.display = "none";
  }

  // Initialize CodeMirror when DOM content is loaded
  document.addEventListener("DOMContentLoaded", function() {
    initializeCodeMirror();
  });
</script>


# working Run, but no previous code
<form id="code_form_id" action="{% url 'python_problems:detail' problem.id %}" method="POST" class="mb-5">
  {% csrf_token %}
  <div class="code-area-container mb-2">
    <label for="id_code_area">Code Area</label>
    <textarea name="code_area" id="id_code_area" cols="80" rows="10" class="python-code" required>{{   }}</textarea>
  </div>
  <button id="submitButton" type="submit" class="btn btn-warning">
    Run
  </button>
</form>

<script>
  // Function to initialize CodeMirror
  function initializeCodeMirror() {
    var editor = CodeMirror.fromTextArea(document.getElementById("id_code_area"), {
      mode: "python",
      lineNumbers: true,
      autofocus: true
    });

    // Hide the original textarea after CodeMirror initialization
    document.getElementById("id_code_area").style.display = "none";
  }

  // Initialize CodeMirror when DOM content is loaded
  document.addEventListener("DOMContentLoaded", function() {
    initializeCodeMirror();
  });
</script>


# remember code in code area but add placeholder
<form id="code_form_id" action="{% url 'python_problems:detail' problem.id %}" method="POST" class="mb-5">
  {% csrf_token %}
  <div class="code-area-container mb-2">
    <label for="id_code_area">Code Area</label>
    <textarea name="code_area" id="id_code_area" cols="80" rows="10" class="python-code" required>
      {% if code_form.code_area %}
      {{ code_form.code_area }}
    {% else %}
      {{ code_form.code_area.field.widget.attrs.placeholder }}
    {% endif %}
    </textarea>
  </div>
  <button id="submitButton" type="submit" class="btn btn-warning">
    Run
  </button>
</form>

<script>
  // Function to initialize CodeMirror
  function initializeCodeMirror() {
    var editor = CodeMirror.fromTextArea(document.getElementById("id_code_area"), {
      mode: "python",
      lineNumbers: true,
      autofocus: true
    });

  }

  // Initialize CodeMirror when DOM content is loaded
  document.addEventListener("DOMContentLoaded", function() {
    initializeCodeMirror();
  });
</script>



# no CodeMirror, Run works
{% load crispy_forms_tags %}
<form id="code_form_id" action="{% url 'python_problems:detail' problem.id %}" method="POST" class="mb-5">
    {% csrf_token %}
    {{ code_form|crispy }}
    <button id="submitButton" type="submit" class="btn btn-warning">
        <span id="spinner" class="spinner-border spinner-border-sm d-none"></span>
        Run
    </button>
</form>

<script>
    document.getElementById('code_form_id').addEventListener('submit', function () {
        document.getElementById('submitButton').disabled = true; // Disable the submit button
        document.getElementById('spinner').classList.remove('d-none'); // Show the spinner
        document.getElementById('submitButton').innerHTML = '<span class="spinner-border spinner-border-sm"></span> Running';
    });
</script>



# just Run button
{% load crispy_forms_tags %}
<form id="code_form_id" action="{% url 'python_problems:detail' problem.id %}" method="POST" class="mb-5">
    {% csrf_token %}
    {{ code_form|crispy }}
    <button id="submitButton" type="submit" class="btn btn-warning">
        <span id="spinner" class="spinner-border spinner-border-sm d-none"></span>
        Run
    </button>
</form>


# Run and code_form.code_area 
{% load crispy_forms_tags %}
<form id="code_form_id" action="{% url 'python_problems:detail' problem.id %}" method="POST" class="mb-5">
    {% csrf_token %}
    <div class="code-area-container mb-2">
      <label for="id_code_area">Code Area</label>
      {{ code_form.code_area }}
    </div>
      <button id="submitButton" type="submit" class="btn btn-warning">
        <span id="spinner" class="spinner-border spinner-border-sm d-none"></span>
        Run
      </button>
</form>







# Run and CodeMirror, but works just when loaded until server reload

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.63.0/codemirror.min.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/codemirror@5.62.0/theme/monokai.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.63.0/codemirror.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.63.0/mode/python/python.min.js"></script>

{% load crispy_forms_tags %}
<form id="code_form_id" action="{% url 'python_problems:detail' problem.id %}" method="POST" class="mb-5">
    {% csrf_token %}
    <div class="code-area-container mb-2">
      <label for="id_code_area">Code Area</label>
      {{ code_form.code_area }}
    </div>
      <button id="submitButton" type="submit" class="btn btn-warning">
        Run
      </button>
</form>

<script>
  var editor = CodeMirror.fromTextArea(document.getElementById("id_code_area"), {
      mode: "python",
      lineNumbers: true, // Enable line numbers
      autofocus: true // Automatically focus on the editor
  });
</script>






# bad

<form id="id_code_form"
action="{% url 'python_problems:detail' problem.id %}"
      method="POST"
      class="mb-5">
  {% csrf_token %}
  <div class="code-area-container mb-2">
    <label for="id_code_area">Code Area</label>
    {{ code_form.code_area }}
  </div>
  <link rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.63.0/codemirror.min.css">
  <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/codemirror@5.62.0/theme/monokai.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.63.0/codemirror.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.63.0/mode/python/python.min.js"></script>
  <script>
    var storedDarkMode = localStorage.getItem('darkMode');
    var editor = CodeMirror.fromTextArea(document.getElementById("id_code_area"), {
        mode: "python",
        theme: storedDarkMode === "enabled" ? "monokai" : "default"
        lineNumbers: true, // Enable line numbers
        autofocus: true // Automatically focus on the editor
    });
  </script>
  <button id="submitButton" type="submit" class="btn btn-warning ">
    <span id="spinner" class="spinner-border spinner-border-sm d-none"></span>
    Run
  </button>
</form>
<script>
    document.getElementById('id_code_form').addEventListener('submit', function () {
        document.getElementById('submitButton').disabled = true; // Disable the submit button
        document.getElementById('spinner').classList.remove('d-none'); // Show the spinner
        document.getElementById('submitButton').innerHTML = '<span class="spinner-border spinner-border-sm"></span> Running';
    });
  </script>





  # good but no placeholder
  <form id="id_code_form"
  action="{% url 'python_problems:detail' problem.id %}"
  method="POST"
  class="mb-5">
{% csrf_token %}
<div class="code-area-container mb-2">
    <label for="id_code_area">Code Area</label>
    {{ code_form.code_area }}
</div>
<link rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.63.0/codemirror.min.css">
<link rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/codemirror@5.62.0/theme/monokai.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.63.0/codemirror.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.63.0/mode/python/python.min.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function () {
        var storedDarkMode = localStorage.getItem('darkMode');
        var theme = storedDarkMode === "enabled" ? "monokai" : "default";
        var editor = CodeMirror.fromTextArea(document.getElementById("id_code_area"), {
            mode: "python",
            theme: theme,
            lineNumbers: true, // Enable line numbers
            autofocus: true // Automatically focus on the editor
        });
    });
</script>
<button id="submitButton" type="submit" class="btn btn-warning ">
    <span id="spinner" class="spinner-border spinner-border-sm d-none"></span>
    Run
</button>
</form>
<script>
document.getElementById('id_code_form').addEventListener('submit', function () {
    document.getElementById('submitButton').disabled = true; // Disable the submit button
    document.getElementById('spinner').classList.remove('d-none'); // Show the spinner
    document.getElementById('submitButton').innerHTML = '<span class="spinner-border spinner-border-sm"></span> Running';
});
</script>





# placeholder messing codemirror
<form id="id_code_form"
      action="{% url 'python_problems:detail' problem.id %}"
      method="POST"
      class="mb-5">
    {% csrf_token %}
    <div class="code-area-container mb-2">
        <label for="id_code_area">Code Area</label>
        {{ code_form.code_area }}
    </div>
    <link rel="stylesheet"
          href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.63.0/codemirror.min.css">
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/codemirror@5.62.0/theme/monokai.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.63.0/codemirror.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.63.0/mode/python/python.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            var storedDarkMode = localStorage.getItem('darkMode');
            var theme = storedDarkMode === "enabled" ? "monokai" : "default";
            var editor = CodeMirror.fromTextArea(document.getElementById("id_code_area"), {
                mode: "python",
                theme: theme,
                lineNumbers: true, // Enable line numbers
                autofocus: true, // Automatically focus on the editor
                placeholder: "Enter your Python code here..." // Placeholder text
            });
        });
    </script>
    <button id="submitButton" type="submit" class="btn btn-warning ">
        <span id="spinner" class="spinner-border spinner-border-sm d-none"></span>
        Run
    </button>
</form>
<script>
    document.getElementById('id_code_form').addEventListener('submit', function () {
        document.getElementById('submitButton').disabled = true; // Disable the submit button
        document.getElementById('spinner').classList.remove('d-none'); // Show the spinner
        document.getElementById('submitButton').innerHTML = '<span class="spinner-border spinner-border-sm"></span> Running';
    });
</script>



    

# forma kolorowana          
          <form method="post">
            {% csrf_token %}
          
            <div class="code-area-container">
              <label for="id_code_area">Code Area</label>
              {{ code_form.code_area }}
            </div>
          
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.63.0/codemirror.min.css">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.63.0/codemirror.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.63.0/mode/python/python.min.js"></script>

          
            <script>
              var editor = CodeMirror.fromTextArea(document.getElementById("id_code_area"), {
                  mode: "python",
                  theme: "default", // You can change the theme if needed
                  lineNumbers: true, // Enable line numbers
                  autofocus: true // Automatically focus on the editor
              });
          </script>
          
          
            <input type="submit" value="Submit">
          </form>
