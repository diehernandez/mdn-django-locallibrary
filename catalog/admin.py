from django.contrib import admin

from .models import Author, Genre, Book, BookInstance, Language

admin.site.register(Genre)
admin.site.register(Language)

class BooksInstanceInline(admin.TabularInline):
    """
    Esta clase permite incluir las instancias de libros en distintas vistas
    ej. Mostrar las instancias de un libro en la pagina de libro.
    """
    model = BookInstance
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Esta clase permite mostrar los libros (no las instancias de los libros).
    """
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    """
    Esta clase permite mostrar las instancias de libros.
    """
    list_filter = ('status', 'due_back')
    list_display = ('book', 'status','borrower', 'due_back', 'id')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprent', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )

class BookAdminInline(admin.TabularInline):
    """
    Esta clase permite incluir los libros en distintas vistas
    ej. Mostrar los libro en la pagina del autor.
    """
    model = Book
    extra = 0

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Esta clase permite mostrar los autores.
    """
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookAdminInline]
