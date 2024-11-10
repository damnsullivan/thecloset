from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from .models import CartItem
from products.models import Product

def view_cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart_items = CartItem.objects.filter(session_id=session_key)

    total = cart_items.aggregate(
        total=Sum(F('product__price') * F('quantity'))
    )['total'] or 0

    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'cart/cart.html', context)

def add_to_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart_item, created = CartItem.objects.get_or_create(session_id=session_key, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    # Atualizar a contagem do carrinho na sessão
    request.session['cart_count'] = CartItem.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0 if request.user.is_authenticated else CartItem.objects.filter(session_id=session_key).aggregate(total=Sum('quantity'))['total'] or 0
    
    return redirect('view_cart')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if request.user.is_authenticated:
        if cart_item.user == request.user:
            cart_item.delete()
    else:
        session_key = request.session.session_key
        if cart_item.session_id == session_key:
            cart_item.delete()
    
    # Atualizar a contagem do carrinho na sessão
    request.session['cart_count'] = CartItem.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0 if request.user.is_authenticated else CartItem.objects.filter(session_id=session_key).aggregate(total=Sum('quantity'))['total'] or 0
    
    return redirect('view_cart')

def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    # Atualizar a contagem do carrinho na sessão
    if request.user.is_authenticated:
        request.session['cart_count'] = CartItem.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
    else:
        session_key = request.session.session_key
        request.session['cart_count'] = CartItem.objects.filter(session_id=session_key).aggregate(total=Sum('quantity'))['total'] or 0
    
    return redirect('view_cart')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = cart_items.aggregate(
        total=Sum(F('product__price') * F('quantity'))
    )['total'] or 0

    if request.method == 'POST':
        cart_items.delete()  
        request.session['cart_count'] = 0  
        return redirect('order_confirmation')  

    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'cart/checkout.html', context)

def order_confirmation(request):
    return render(request, 'cart/order_confirmation.html')
