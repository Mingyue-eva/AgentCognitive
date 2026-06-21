The error:
When loading the fixture into the non-default database, Django fails while resolving the natural key for each Book. During deserialization it builds a Book instance and immediately calls its natural_key() method, which reaches out to the related Author via its own natural_key lookup on the “other” database. Since that Author record hasn’t been created yet in the secondary database, accessing book.author triggers an ORM lookup that cannot find a matching Author row and ultimately raises an Author.DoesNotExist exception.

the model:
from django.db import models
class AuthorManager(models.Manager):
	def get_by_natural_key(self, name):
		return self.get(name=name)
class Author(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=255, unique=True)
	objects = AuthorManager()
	def natural_key(self):
		return (self.name,)
	def __str__(self):
		return f"{self.id} {self.name}"
class BookManager(models.Manager):
	def get_by_natural_key(self, title, author):
		return self.get(title=title, author__name=author)
class Book(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=255)
	author = models.ForeignKey(Author, models.DO_NOTHING, related_name="books")
	objects = BookManager()
	def natural_key(self):
		return (self.title,) + self.author.natural_key()
	natural_key.dependencies = ["testbug.Author"]
	class Meta:
		unique_together = [["title", "author"]]
	def __str__(self):
		return f"{self.id}: '{self.title}' by {self.author}"

the data (generated with from django.core import serializers; from testbug.models import Book, Author; print(serializers.serialize("json", list(Author.objects.all()) + list(Book.objects.all()), indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True)) in the shell):
[
  {
    "model": "testbug.author",
    "fields": {
      "name": "JR Tolkien"
    }
  },
  {
    "model": "testbug.book",
    "fields": {
      "title": "The Ring",
      "author": [
        "JR Tolkien"
      ]
    }
  }
]