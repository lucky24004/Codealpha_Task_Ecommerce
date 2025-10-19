from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User


# ==============================
# PRODUCT VIEWS
# ==============================

from .models import Product, Order

def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'store/product_list.html', {'products': products})



def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})


# ==============================
# CART VIEWS
# ==============================

def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart = request.session.get('cart', {})
    key = str(product.id)
    qty = int(request.GET.get('qty', 1))

    if key in cart:
        cart[key] += qty
    else:
        cart[key] = qty

    request.session['cart'] = cart
    messages.success(request, f"Added {product.name} (×{qty}) to cart.")
    return redirect('cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    key = str(product_id)
    if key in cart:
        del cart[key]
        request.session['cart'] = cart
        messages.success(request, "Item removed from cart.")
    return redirect('cart')


def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = Decimal('0.00')

    if cart:
        product_ids = [int(pid) for pid in cart.keys()]
        products = Product.objects.filter(id__in=product_ids)
        product_map = {p.id: p for p in products}

        for pid_str, qty in cart.items():
            pid = int(pid_str)
            product = product_map.get(pid)
            if not product:
                continue
            item_total = product.price * qty
            total += item_total
            items.append({'product': product, 'quantity': qty, 'item_total': item_total})

    return render(request, 'store/cart.html', {'items': items, 'total': total})


# ==============================
# CHECKOUT
# ==============================

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('product_list')

    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.filter(id__in=product_ids)
    product_map = {p.id: p for p in products}

    order = Order.objects.create(user=request.user)
    order_total = Decimal('0.00')

    for pid_str, qty in cart.items():
        pid = int(pid_str)
        product = product_map.get(pid)
        if not product:
            continue
        price = product.price
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=qty,
            price_at_purchase=price
        )
        order_total += price * qty

    order.total = order_total
    order.status = 'PAID'  # Demo assumption
    order.save()

    request.session['cart'] = {}  # clear cart
    messages.success(request, f"Order #{order.id} placed successfully! Total: ₹{order.total}")
    return render(request, 'store/checkout.html', {'order': order})


# ==============================
# AUTHENTICATION
# ==============================


from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect("login")  # ✅ redirect to login after signup
        else:
            messages.error(request, "Signup failed. Please correct the errors.")
    else:
        form = SignUpForm()
    return render(request, "store/signup.html", {"form": form})


from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("product_list")
        else:
            messages.error(request, "Invalid email or password")
    return render(request, "store/login.html")




def user_logout(request):
    """Custom logout page"""
    logout(request)  # clear session
    messages.info(request, "You have been logged out.")
    return redirect("login")  # go back to login page

from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)  # this clears the session
    return redirect('login')  # redirect back to login page after logout

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/my_orders.html', {'orders': orders})


@login_required
def cancel_order(request, order_id):
    order = Order.objects.filter(id=order_id, user=request.user).first()
    if not order:
        messages.error(request, "Order not found.")
        return redirect('my_orders')

    if order.status == 'PAID':
        order.status = 'CANCELLED'
        order.save()
        messages.success(request, f"Order #{order.id} cancelled successfully.")
    else:
        messages.warning(request, "This order cannot be cancelled.")

    return redirect('my_orders')
