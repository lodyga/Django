import csv  # https://docs.python.org/3/library/csv.html

# https://django-extensions.readthedocs.io/en/latest/runscript.html

# python3 manage.py runscript cats_load


# def run():
#     fhand = open('cats/meow.csv')
#     reader = csv.reader(fhand)
#     next(reader)  # Advance past the header
#
#     Cat.objects.all().delete()
#     Breed.objects.all().delete()
#
#     # Name,Breed,Weight
#     # Abby,Sphinx,6.4
#     # Annie,Burmese,7.6
#     # Ash,Manx,7.8
#     # Athena,Manx,8.9
#     # Baby,Tabby,6.9
#
#     for row in reader:
#         print(row)
#
#         b, created = Breed.objects.get_or_create(name=row[1])
#
#         c = Cat(nickname=row[0], breed=b, weight=row[2])
#         c.save()

# def run():
#     with open("cats/meow.csv") as file:
#         reader = csv.DictReader(file)
#
#         next(reader)
#
#         Cat.objects.all().delete()
#         Breed.objects.all().delete()
#
#         for cat in reader:
#
#             print(cat)
#
#             b, _ = Breed.objects.get_or_create(name=cat["Breed"])
#             Cat.objects.create(nickname=cat["Name"], breed=b, weight=cat["Weight"])

from cats.models import Cat, Breed
import pandas as pd


def run():
    cats = pd.read_csv("cats/meow.csv")

    Cat.objects.all().delete()
    Breed.objects.all().delete()

    for _, cat in cats.iterrows():
        print(cat)
        b, created = Breed.objects.get_or_create(name=cat["Breed"])
        Cat.objects.create(nickname=cat["Name"], breed=b, weight=cat["Weight"])
