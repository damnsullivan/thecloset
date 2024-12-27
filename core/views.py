from django.shortcuts import render
from django.db.models import Q
from products.models import Product
import random

def home(request):
    if 'random_products' not in request.session:
        all_products = list(Product.objects.filter(available=True))
        random_products = random.sample(all_products, min(4, len(all_products)))
        request.session['random_products'] = [product.id for product in random_products]
    else:
        product_ids = request.session['random_products']
        random_products = Product.objects.filter(id__in=product_ids)

    context = {
        'products': random_products
    }
    return render(request, 'core/home.html', context)

def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query),
            available=True
        )
    
    context = {
        'query': query,
        'results': results
    }
    return render(request, 'core/search_results.html', context)

def faq(request):
    return render(request, 'core/faq.html')
