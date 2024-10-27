from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Product, Category

def product_list(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()

    # Filtros
    category_slug = request.GET.get('category')
    gender = request.GET.get('gender')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    rating = request.GET.get('rating')
    query = request.GET.get('q')
    sort = request.GET.get('sort', 'name')

    # Aplicar filtros
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    if gender:
        products = products.filter(gender=gender)
    
    if price_min:
        products = products.filter(price__gte=float(price_min))
    
    if price_max:
        products = products.filter(price__lte=float(price_max))
    
    if rating:
        products = products.filter(rating__gte=int(rating))
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(brand__icontains=query)
        )
    
    # Ordenação
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    elif sort == 'rating':
        products = products.order_by('-rating')
    
    # Paginação
    paginator = Paginator(products, 12)  # 12 produtos por página
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': category_slug,
        'current_gender': gender,
        'current_price_min': price_min,
        'current_price_max': price_max,
        'current_rating': rating,
        'current_query': query,
        'current_sort': sort
    }
    
    return render(request, 'products/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products
    }
    
    return render(request, 'products/product_detail.html', context)
