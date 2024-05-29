import os
import django
from django.core.management import call_command

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codesite.settings')
django.setup()

from django.contrib.contenttypes.models import ContentType
from python_problems.models import Tag, Problem  # Import your models

# Apply migrations
call_command('migrate')

# Optional: Clear specific application tables to avoid duplicates
Tag.objects.all().delete()
Problem.objects.all().delete()

# Clear the content types to avoid unique constraint issues
ContentType.objects.all().delete()

# Load the data from the fixture
try:
    call_command('loaddata', 'fixtures/db_data.json')
    print("Database restored.")
except Exception as e:
    print(f"Error loading data: {e}")
