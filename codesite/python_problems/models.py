from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=20)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name


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


class NonStrippingTextField(models.TextField):
    """
    A TextField that does not strip whitespace at the beginning/end of
    it's value. Might be important for markup/code.
    """
    def formfield(self, **kwargs):
        kwargs['strip'] = False
        return super().formfield(**kwargs)


class Language(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Problem(models.Model):
    title = models.CharField(unique=True, max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    tags = models.ManyToManyField("Tag")
    difficulty = models.ForeignKey(
        Difficulty,
        related_name="problems_difficulty",
        on_delete=models.DO_NOTHING)
    url = models.URLField()
    description = NonStrippingTextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("python_problems:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class Solution(models.Model):
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE)
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    source_code = models.TextField(blank=True, null=True)
    test_cases = models.TextField(
        blank=True,
        null=True,
        help_text='Format test cases as `([class.?]function(args), expected_result)`, one per line. Example: (reverse_string("hello"), "olleh")')
    time_complexity = models.ForeignKey(
        "Complexity",
        related_name="solution_time_complexity",
        on_delete=models.DO_NOTHING)
    space_complexity = models.ForeignKey(
        "Complexity",
        related_name="solution_space_complexity",
        on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('problem', 'language', 'owner'),
                name='unique_user_solution_per_problem_and_language')
        ]

    def __str__(self):
        return f"{self.problem.title} ({self.language.name}) by {self.owner}"
