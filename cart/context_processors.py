from django.db.models import Sum
from .models import CartItem

def cart_count(request):
    if request.user.is_authenticated:
        count = CartItem.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
    else:
        session_key = request.session.session_key
        if not session_key:
            count = 0
        else:
            count = CartItem.objects.filter(session_id=session_key).aggregate(total=Sum('quantity'))['total'] or 0
    return {'cart_count': count}
