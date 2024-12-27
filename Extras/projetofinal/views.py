from django.shortcuts import render
from products.models import Product  
from django.core.files.storage import default_storage
from django.contrib.staticfiles.storage import staticfiles_storage


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def search_results(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)  
    else:
        products = Product.objects.none()
    return render(request, 'search_results.html', {'products': products, 'query': query})


       











