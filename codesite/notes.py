# activate django virtual env
source djangoenv/bin/activate

# run django server
py manage.py runserver




# Django fetch related data efficiently up front, instead of one query per row.

queryset = (
    Problem.objects
    .select_related("difficulty", "owner")
    .prefetch_related("tags", "solution_set__language")
)

# Py
Problem  # class
Problem.objects  # manager 
Problem.objects.all()  # queryset
Problem.objects.count()  # 520

Problem.title  # DeferredAttribute
Problem.difficulty  # ForwardManyToOneDescriptor
Problem.difficulty_id  # ForeignKeyDeferredAttribute
Problem.tags  # ManyToManyDescriptor

Problem.solution_set  # ReverseManyToOneDescriptor

Language  # class
Language.solution_set  # ReverseManyToOneDescriptor

Problem.objects.select_related("difficulty", "owner")  # QuerySet
Problem.objects.prefetch_related("tags", "solution_set__language")  # QuerySet


# html
problem.solution_set.values_list("language__name", flat=True).distinct() == <QuerySet ['Python', 'JavaScript']>




# all Solution objects
problem.solution_set.all()

# language names (can repeat)
problem.solution_set.values_list("language__name", flat=True)

# unique language names
problem.solution_set.values_list("language__name", flat=True).distinct()

# Language objects (unique)
Language.objects.filter(solution__problem=problem).distinct()

for debugger only, reverse PK
list(problem.solution_set.values_list("language__name", flat=True).distinct())





# Bootstrap blue color: #0d6efd; color: var(--bs-primary);
| Class             | Hex       | RGB                  |
| ----------------- | --------- | -------------------- |
| `.text-primary`   | `#0d6efd` | `rgb(13, 110, 253)`  |
| `.text-secondary` | `#6c757d` | `rgb(108, 117, 125)` |
| `.text-success`   | `#198754` | `rgb(25, 135, 84)`   |
| `.text-danger`    | `#dc3545` | `rgb(220, 53, 69)`   |
| `.text-warning`   | `#ffc107` | `rgb(255, 193, 7)`   |
| `.text-info`      | `#0dcaf0` | `rgb(13, 202, 240)`  |


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


python manage.py dumpdata \
  --natural-foreign \
  --natural-primary \
  --exclude contenttypes \
  --exclude auth.permission \
  --exclude sessions \
  > data.json


# Active database backend at runtime.
$ python manage.py shell
>> from django.db import connection
>> print(connection.vendor)









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



# hack my site
import os
cwd = os.getcwd()
f = open(cwd+'/'+'aaaaa.txt', 'w') # write a file
f.write('Hello\nWorld\nnew\n')
f.close()
output = cwd
















