# login on render
# fetch from judge0 Python 3.8.1
# docker on vsc button
# judge0
# ?move to 'show solution' from the view
# ask AI
# reverse search for order by, difficulty
# Edit/info/settings tab
# dev opts for update|delete
# search bar AND OR
# chanege python to code_problems...
# refactor; Filter Users Using Reverse Relationship; filter().values_list("language", flat=True))
# selenium for testing darkmode
# Language.objects.all().delete() fix Python, JS, in migrations; UNIQUE constraint failed: python_problems_language.name




import socket
def is_localhost(self):
    localhost_list = ["127.0.0.1", "127.0.1.1", "::1"]
    hostname = socket.gethostname()
    host_ip = socket.gethostbyname(hostname)
    return host_ip in localhost_list


print(socket.gethostname())
print(socket.gethostbyname(socket.gethostname()))