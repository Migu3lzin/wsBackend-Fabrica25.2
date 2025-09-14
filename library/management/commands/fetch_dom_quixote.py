from django.core.management.base import BaseCommand
import requests
from library.models import Author, Book

API_URL = 'https://openlibrary.org/search.json?title=Dom+Quixote'

class Command (BaseCommand):
    help = 'Busca no OpenLibrary por Dom Quixote e popula o banco (top 10 resultado)'

    def handle(self, *args, **options):
        resp = requests.get(API_URL)
        if resp.status_code != 200:
            self.stdout.write(self.style.ERROR('Falha ao chamar OpenLibrary: %s' % resp.status_code))
            return
        data = resp.json()
        docs = data.get('docs', [])[:10]
        created = 0
        for d in docs:
            key = d.get('key') or (d.get( 'edition_key') and d['editior_key'][0])
            title = d.get('title') or d.get('title_sugget')
            authors = d.get('author_name')or []
            year = d.get('first_publish_year')
            isbn = d.get('isbn', [None]) [0] if d.get('isbn') else None

            if not key or not title:
                continue
            # normaliza chave
            ol_key = str(key)
            if Book.objects.filter(openlibrary_key=ol_key).exists():
                continue
            book = Book.objects.create(title=title, openlibrary_key=ol_key, publish_year=year, isbn=isbn)
            for name in authors:
                author, _ = Author.objects.get_or_create(name=name)
                book.authors.add(author)
            created += 1
        self.stdout.write(self.style.SUCCESS (f'Criados {created} livros (top 10)'))


                

