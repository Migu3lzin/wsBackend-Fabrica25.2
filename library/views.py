from rest_framework import viewsets, permissions
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from django.shortcuts import render

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('-id')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-id')
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

# views para templates (index.html está sendo servida diretamente via TemplateView do projeto)
