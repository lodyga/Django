from django.db import models
from django.utils.text import slugify


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
    """A TextField that does not strip whitespace at the beginning/end of
    it's value.  Might be important for markup/code."""

    def formfield(self, **kwargs):
        kwargs['strip'] = False
        return super(NonStrippingTextField, self).formfield(**kwargs)


class Problem(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    tags = models.ManyToManyField("Tag")
    difficulty = models.ForeignKey(
        Difficulty, related_name="problems_difficulty", on_delete=models.DO_NOTHING)
    time_complexity = models.ForeignKey(
        Complexity, related_name="problems_time_complexity", on_delete=models.DO_NOTHING)
    space_complexity = models.ForeignKey(
        Complexity, related_name="problems_space_complexity", on_delete=models.DO_NOTHING)
    url = models.CharField(max_length=200)
    description = NonStrippingTextField(blank=False, null=False)
    is_solved = models.BooleanField(default=False)
    solution = NonStrippingTextField(blank=True, null=True)
    testcase = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name
