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




  

<span class="border rounded px-3 py-2 d-inline-block col-auto">
<div class="row justify-content-"
<div class="d-flex justify-content-"
start
center
end
around
between
evenly
">  

<div class="align-items-center"
<div class="col-auto">

pip install -r /path/to/requirements.txt


btn.classList.remove('btn-secondary');
btn.classList.add('btn-outline-secondary');
btn.classList.replace('btn-secondary', 'btn-outline-secondary');
descriptionToggle.setAttribute('aria-expanded', 'true');



prefetch_related("tags", "solution_set__language") → prefetch_related("tags", "solutions__language")
filter(solution__language_id=language_id) → filter(solutions__language_id=language_id)



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
py manage.py dumpdata > data.json
# restore
# To load data without load_db.py first delete ContentType after migrate
from django.contrib.contenttypes.models import ContentType
# Delete all content types
ContentType.objects.all().delete()
py manage.py loaddata data.json


# Worked for MySQL
python manage.py dumpdata \
  --natural-foreign \
  --natural-primary \
  --exclude contenttypes \
  --exclude sessions \
  --exclude auth.permission \
  > data.json

# Worked for PostqreSQL
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.permission > data.json

# Active database backend at runtime.
$ python manage.py shell
>> from django.db import connection
>> print(connection.vendor)
>> print(connection.settings_dict)








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




# same button
<a href="{% url 'python_problems:problem-index' %}" class="btn btn-secondary">Cancel</a>

<input type="button"
       class="btn btn-secondary"
       onclick="window.location='{% url 'python_problems:problem-index' %}'"
       value="Cancel" />

<a href="{{ next_url }}" class="btn btn-sm btn-outline-secondary">Cancel</a>
          
<input type="button"
       class="btn btn-sm btn-outline-secondary"
       onclick="window.location='{{ next_url }}'"
       value="Cancel" />



Error: That port is already in use.
lsof -i :8000
kill PID


# Replace next line indicator with next line.
echo \
'<text_here>' \
| sed 's/\\r\\n/\
/g' | 
sed 's/\\n/\
/g'



echo \
'import json\nfrom typing import Optional, List\nfrom collections import deque\nfrom typing import Optional, List  # Use types from typing\n\n\n"""\nUtility functions for binary tree operations in Python.\n\nProvides:\n- `TreeNode`: Basic binary tree node structure.\n- `build_binary_tree()`: Constructs a tree from a level-order traversal list.\n- `serialize_binary_tree()`: Returns tree values in level-order sequence.\n\nExample:\n    >>> root = build_binary_tree([1, 2, 3, None, 4])\n    >>> serialize_binary_tree(root)\n    [1, 2, 3, None, 4]\n"""\n\n\nclass TreeNode:\n    """\n    Definition for a binary tree node.\n    """\n    def __init__(self, val=None, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\n\ndef build_binary_tree(node_list: List[int], node_type: TreeNode = TreeNode, with_lookup: bool = False) -> TreeNode:\n    """\n    Build binary tree from level order traversal list.\n\n    If with_lookup=True, returns (root, lookup)\n    where lookup is node value to node map.\n    """\n    # if tree.Node from binarytree is used\n    # if node_type == tree.Node:\n    #     return tree.build2(node_list)\n\n    while node_list and node_list[-1] is None:\n        node_list.pop()\n\n    if not node_list:\n        return None\n    elif type(node_list) not in (list, tuple):\n        raise TypeError(\n            "Expected a list, got " + str(type(node_list).__name__)\n        )\n\n    root = node_type(node_list[0])\n    queue = deque([root])\n    index = 1\n    lookup = {root.val: root} if with_lookup else None\n\n    while index < len(node_list):\n        node = queue.popleft()\n\n        # Assign the left child if available\n        if (\n            index < len(node_list) and\n            node_list[index] is not None\n        ):\n            node.left = node_type(node_list[index])\n            queue.append(node.left)\n            if with_lookup:\n                lookup[node.left.val] = node.left\n        index += 1\n\n        # Assign the right child if available\n        if (\n            index < len(node_list) and\n            node_list[index] is not None\n        ):\n            node.right = node_type(node_list[index])\n            queue.append(node.right)\n            if with_lookup:\n                lookup[node.right.val] = node.right\n        index += 1\n\n    return (root, lookup) if with_lookup else root\n\n\ndef serialize_binary_tree(root: TreeNode) -> List[int]:\n    """\n    Return tree node values in level order traversal format.\n    """\n    if not root:\n        return []\n    elif type(root) not in (TreeNode, ):\n        raise TypeError("Expected tree node, got " + str(type(root).__name__))\n    elif root.val == root.left == root.right == None:\n        return []\n\n    values = []\n    queue = deque([root])\n\n    while any(queue):\n        queue_for_level = deque()\n        while queue:\n            node = queue.popleft()\n            values.append(node.val if node else None)\n            queue_for_level.append(node.left if node else None)\n            queue_for_level.append(node.right if node else None)\n        queue = queue_for_level\n\n    while values[-1] is None:\n        values.pop()\n    return values\n\n\ndef is_same_tree(root1: TreeNode, root2: TreeNode) -> bool:\n    """\n    Time complexity: O(n)\n    Auxiliary space complexity: O(n)\n    Tags: binary tree, dfs, recursion\n    """\n    def dfs(node1, node2):\n        if node1 is None and node2 is None:\n            return True\n        elif node1 is None or node2 is None:\n            return False\n\n        if node1.val != node2.val:\n            return False\n\n        left = dfs(node1.left, node2.left)\n        right = dfs(node1.right, node2.right)\n        return left and right\n\n    return dfs(root1, root2)\n\n# class TreeNode:\r\n#     """\r\n#     Definition for a binary tree node.\r\n#     """\r\n#     def __init__(self, val=None, left=None, right=None):\r\n#         self.val = val\r\n#         self.left = left\r\n#         self.right = right\r\n\r\n\r\nclass Solution:\r\n    def invertTree(self, root: TreeNode) -> TreeNode:\r\n        """\r\n        Time complexity: O(n)\r\n        Auxiliary space complexity: O(n)\r\n        Tags:\r\n            DS: binary tree\r\n            A: dfs, recursion, pre-order traversal\r\n        """\r\n        def dfs(node):\r\n            if node is None:\r\n                return \r\n\r\n            node.left, node.right = node.right, node.left\r\n            dfs(node.right)\r\n            dfs(node.left)\r\n        \r\n        dfs(root)\r\n        return root\nsolution = Solution()\nprint(json.dumps(serialize_binary_tree(solution.invertTree(build_binary_tree([4, 2, 7, 1, 3, 6, 9])))))\nprint(json.dumps(serialize_binary_tree(solution.invertTree(build_binary_tree([2, 1, 3])))))\nprint(json.dumps(serialize_binary_tree(solution.invertTree(build_binary_tree([])))))\nprint(json.dumps(serialize_binary_tree(solution.invertTree(build_binary_tree([7, 3, 15, None, None, 9, 20])))))\n'\
| sed 's/\\r\\n/\
/g' | 
sed 's/\\n/\
/g'
