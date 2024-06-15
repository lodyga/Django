from django.db import models
from django.utils.text import slugify
from django.urls import reverse


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
    title = models.CharField(unique=True, max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    tags = models.ManyToManyField("Tag")
    # is_solved = models.BooleanField(default=False)
    difficulty = models.ForeignKey(
        Difficulty, related_name="problems_difficulty", on_delete=models.DO_NOTHING)
    url = models.CharField(max_length=200)
    description = NonStrippingTextField(blank=False, null=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    
    # language relateg attributes
    solution = NonStrippingTextField(blank=True, null=True)
    testcase = models.TextField(blank=True, null=True)
    time_complexity = models.ForeignKey(
        Complexity, related_name="problems_time_complexity", on_delete=models.DO_NOTHING)
    space_complexity = models.ForeignKey(
        Complexity, related_name="problems_space_complexity", on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("python_problems:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=20)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name
