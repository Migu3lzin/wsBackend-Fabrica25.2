from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=500)
    openlibrary_key = models.CharField(max_length=200, blank=True, null=True, unique=True)
    published_year = models.IntegerField(blank=True, null=True)
    isbn = models.CharField(max_length=50, blank=True, null=True)
    author = models.ManyToManyField(Author, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
   
