import uuid

from django.db import models
from django.utils.text import slugify
from model_utils.models import TimeStampedModel


class UUIDModelMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class SlugModelMixin(models.Model):
    slug = models.SlugField(max_length=500, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Author(UUIDModelMixin, SlugModelMixin, TimeStampedModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    @property
    def number_of_books(self):
        return self.book_set.count()


class Book(UUIDModelMixin, SlugModelMixin, TimeStampedModel):
    name = models.CharField(max_length=128)
    author = models.ForeignKey("library.Author", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
