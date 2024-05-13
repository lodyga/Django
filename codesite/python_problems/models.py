from django.db import models


class Difficulty(models.Model):
    name = models.CharField(max_length=16)

    class Meta:
        verbose_name_plural = "Difficulties"
        # ordering = ("name", )

    def __str__(self) -> str:
        return self.name


class Complexity(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "Complexities"

    def __str__(self) -> str:
        return self.name


class Problem(models.Model):
    tags = models.ManyToManyField("Tag")
    title = models.CharField(max_length=200)
    difficulty = models.ForeignKey(
        Difficulty, related_name="problems_difficulty", on_delete=models.DO_NOTHING)
    time_complexity = models.ForeignKey(
        Complexity, related_name="problems_time_complexity", on_delete=models.DO_NOTHING)
    space_complexity = models.ForeignKey(
        Complexity, related_name="problems_space_complexity", on_delete=models.DO_NOTHING)
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
