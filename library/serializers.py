from rest_framework import serializers
from .models import Author, Book

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name')

class BookSerializer(serializers.ModelSerializer):
    #escrita recebe lista de nomes; leitura expõe lista detalhada
    authors = serializers.ListField(child=serializers.CharField(), write_only=True)
    authors_detail = AuthorSerializer(source='authors', many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'openlibrary_key', 'published_year', 'isbn', 'authors', 'authors_detail')
    
    def create(self,validated_data):
        authors_data = validated_data.pop('authors', [])
        book = Book.objects.create(**validated_data)
        for name in authors_data:
            author, _ = Author.objects.get_or_create(name=name)
            book.authors.add(author)
        return book
    
    def update(self, instance, validated_data):
        authors_data = validated_data.pop('authors', [])
        book = Book.objects.create(**validated_data)
        for name in authors_data:
            author, _ = Author.objects.get_or_create(name=name)
            book.authors.add(author)
        return book
    
    def update(self, instance, validated_data):
        authors_data = validated_data.pop('authors', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if authors_data is not None:
            instance.authors.clear()
            for name in authors_data:
                author, _ = Author.objects.get_or_create(name=name)
                instance.authors.add(author)
        return instance


