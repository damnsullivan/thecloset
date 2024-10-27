from django.shortcuts import render
from django.db.models import Q
from products.models import Product  # Certifique-se de que este import está correto

def home(request):
    products = Product.objects.all()
    return render(request, 'core/home.html', {'products': products})

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


