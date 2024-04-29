from django.db import models


class Difficulty(models.Model):
    name = models.CharField(max_length=10)

    # class Meta:
    #     ordering = ("name", )

    def __str__(self) -> str:
        return self.name


class Problem(models.Model):
    tags = models.ManyToManyField("Tag")
    title = models.CharField(max_length=200)
    difficulty = models.ForeignKey(Difficulty, related_name="co_to", on_delete=models.DO_NOTHING)
    url = models.CharField(max_length=200)
    description = models.TextField(blank=False, null=False)
    is_solved = models.BooleanField(default=False)
    solution = models.TextField(blank=True, null=True)
    testcase = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name
