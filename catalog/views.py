from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, ListView, \
    DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.models import Product, Contact, Blog


class IndexView(TemplateView):
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Product.objects.all()
        return context_data

# def index(request):
#     # Convert QuerySet to List
#     # list_products = list(Product.objects.all())
#     # Print last five records
#     # if len(list_products) >= 5:
#     #     for product in list_products[-5:]:
#     #         print(product)
#     # else:
#     #     for product in list_products:
#     #         print(product)
#
#     # Get all products from catalog
#     products = Product.objects.all()
#
#     context = {
#         'object_list': products,
#     }
#
#     return render(request, 'catalog/index.html', context)

def contacts(request):
    data = Contact.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} ({email}): {message}')
    return render(request, 'catalog/contacts.html',{"contacts": data})


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'content', 'date_created', 'preview', 'is_published')
    success_url = reverse_lazy('catalog:blog_list')

    def form_valid(self, form):
        if form.is_valid:
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'content', 'date_created', 'preview', 'is_published')

    def form_valid(self, form):
        if form.is_valid:
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:blog_view', args=[self.kwargs.get('pk')])


class BlogListView(ListView):
    model = Blog


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')


def hidden_blog(request):
    context = {
        'object_list': Blog.objects.all(),
    }
    return render(request, 'catalog/blog_hidden.html', context)