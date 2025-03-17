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
response.content.decode()
    decode utf-8; get rid of b
content = html.unescape(response.content.decode())
    &#x27; -> \'
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













