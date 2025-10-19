# store/context_processors.py
def cart_item_count(request):
    cart = request.session.get('cart', {})
    total_items = sum(cart.values()) if isinstance(cart, dict) else 0
    return {'cart_item_count': total_items}
