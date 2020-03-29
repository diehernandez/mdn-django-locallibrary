import datetime

from django.shortcuts import get_object_or_404, render
from django.views import generic
#from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse


from .models import Book, Author, BookInstance, Genre
from .forms import RenewBookForm

def ejemplos(request):
    return render(request,'ejemplos.html')

def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genre = Genre.objects.count()
    num_books_start_with_a = Book.objects.filter(title__istartswith='c').count()
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_books_start_with_a': num_books_start_with_a,
        'num_visits': num_visits
    }
    return render(request,'catalog/index.html',context)



class BookListView(generic.ListView):
    model = Book

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksListView(PermissionRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan.
    """
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst =get_object_or_404(BookInstance, pk = pk)

     # If this is a POST request then process the Form data
    if request.method == 'POST':
         # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

         # Check if the form is valid:
        if form.is_valid():
              # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
              book_inst.due_back = form.cleaned_data['renewal_date']
              book_inst.save()
              # redirect to a new URL:
              return HttpResponseRedirect(reverse('all-borrowed') )
    # If this is a GET (or any other method) create the default form.
    else:
        proposal_renewed_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposal_renewed_date,})

    return render( request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})
