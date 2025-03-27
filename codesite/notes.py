

# text
darkModeLabel.textContent = 'Light\nMode';
darkModeLabel.innerText = 'Light\nMode';
darkModeLabel.innerHTML = 'Light\nMode';

# markdown, pygments.css
<link rel="stylesheet" href="{% static 'css/pygments.css' %}">
      <div class="row mb-2 markdown-content">
        {{ markdown_content|safe }}
      </div>
        md_file = os.path.join(os.path.dirname(__file__), "temp.md")
        
        with open(md_file, "r", encoding="utf-8") as f:
            md_content = f.read()

        markdown_content = markdown.markdown(
            md_content,
            extensions=[
                "fenced_code",
                "codehilite",  # Requires Pygments (pip install pygments)
            ]
        )        
"markdown_content": markdown_content,

curl -X POST "https://api.cohere.ai/v1/generate" -H "Authorization: Bearer pass" -H "Content-Type: application/json" -d '{"model":"command","prompt":"Hello","max_tokens":10}'

# list proceses on port 8000
lsof -i :8000
kill <pid>

self.client.get() returns <class 'django.template.response.TemplateResponse'>
self.client.post() returns <class 'django.http.response.HttpResponse'>

"""
assertContains(response, text)	
  ✅ Yes, requires 200	
  ❌ No, fails with encoded characters	
  Validating presence in an HTTP response
assertIn(text, content)	
  ❌ No	
  ✅ Yes, works with decoded text	
  Checking text inside processed content
"""

"""
decode utf-8; get rid of b
response.content.decode()

&#x27; -> \'
content = html.unescape(response.content.decode())
"""


"""
Configuration for Testing
settings.py: 
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "testserver"]

settings.json:
{
    "python.testing.pytestEnabled": false,
    "python.testing.unittestEnabled": true,
    "python.testing.unittestArgs": [
        "-v",
        "-s",
        ".",
        "-p",
        "tests.py"
    ],
    "python.envFile": "${workspaceFolder}/.env"
}

.env
DJANGO_SETTINGS_MODULE=codesite.settings
"""









# generate empty migration
py manage.py makemigrations --empty python_problems --name populate_slugs

# migrations
py manage.py showmigrations python_problems

# backup/restore db witm a script
# backup db.sqlite3
python manage.py dumpdata > fixtures/db_data.json
# restore
py manage.py load_db fixtures/db_data.json 

# backup/restore db without a script
# backup
py manage.py dumpdata > db.json
# restore
# To load data without load_db.py first delete ContentType after migrate
from django.contrib.contenttypes.models import ContentType
# Delete all content types
ContentType.objects.all().delete()
py manage.py loaddata db.json


# Run and Debug create a lunch.json file, creates .vscode/lunch.json

# Docker:Add Docker Files to Workspace, creates Dockerfile, .dockerignore, .vscode/lunch.json, .vscode/tasks.json







In [28]: Problem.objects.get(title='Two Sum').solutions.get(pk=41)
Out[28]: <Solution: Two Sum (JavaScript)>

In [38]: Problem.objects.get(title='Two Sum').solutions.get(pk=41).solution
Out[38]: '// Using Plain Object:\r\nvar twoSum = (nums, target) => {\r\n    const seen = {}\r\n\r\n    for (let ind = 0; ind < nums.length; ind++) {\r\n        const num = nums[ind];\r\n        const diff = target - num;\r\n\r\n        if (diff in seen) {\r\n            return [seen[diff], ind];\r\n        }\r\n        seen[num] = ind;\r\n    }\r\n\r\n    return [-1, -1]\r\n};'

In [3]: Problem.objects.get(title='Two Sum').solutions_problem.all()
Out[3]: <QuerySet [<Solution: Two Sum (Python)>, <Solution: Two Sum (JavaScript)>]>

In [11]: Problem.objects.get(title='Two Sum').languages.values()
Out[11]: <QuerySet [{'id': 1, 'name': 'Python'}, {'id': 2, 'name': 'JavaScript'}]>

# Reason to add Soulution to a Problem, actually not because it forces Solution while upadating Problem.
In [36]: Problem.objects.get(title='Two Sum').solutions.all()
Out[36]: <QuerySet [<Solution: Two Sum (Python)>, <Solution: Two Sum (JavaScript)>]>
In [37]: Problem.objects.get(title='Sum of Pairs').solutions.all()
Out[37]: <QuerySet []>

In [19]: Problem.objects.get(title="Two Sum").solutions_problem.get(language=Language.objects.get(name="Python"))
Out[19]: <Solution: Two Sum (Python)>

In [5]: Problem.objects.get(title="Two Sum").solutions_problem.all()
Out[5]: <QuerySet [<Solution: Two Sum (Python)>, <Solution: Two Sum (JavaScript)>]>

Fixed bug where "grouped_anagrams.values()" from Group Anagrams problem returned "dict_values object" which caused function to run indefinetly'
Fixed bug where returning "grouped_anagrams.values()" from Group Anagrams problem caused function to run indefinitely by converting to list.


{% for solution in problem.solutions_problem.all %}
 <strong>Language:</strong> {{ solution.language.name }}<br>
 <pre>{{ solution.solution }}</pre>
{% endfor %}


"""
print(output_form.__dict__):
{'is_bound': False, 'data': <MultiValueDict: {}>, 'files': <MultiValueDict: {}>, 'auto_id': 'id_%s', 'initial': {'output_area': "Error: 'output'"}, 'error_class': <class 'django.forms.utils.ErrorList'>, 'label_suffix': ':', 'empty_permitted': False, '_errors': None, 'fields': {'output_area': <django.forms.fields.CharField object at 0x7832c705b1f0>}, '_bound_fields_cache': {}, 'renderer': <django.forms.renderers.DjangoTemplates object at 0x7832c701b0a0>}

"""

# hack my site
import os
cwd = os.getcwd()
f = open(cwd+'/'+'aaaaa.txt', 'w') # write a file
f.write('Hello\nWorld\nnew\n')
f.close()
output = cwd
















