
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Product
from .cart import get_cart


def product_list(request):
    products = Product.objects.filter(
        is_available=True,
        stock__gt=0
    )

    return render(
        request,
        "shop/product_list.html",
        {"products": products}
    )


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True
    )

    if product.stock < 1:
        return redirect("shop:product_list")

    cart = request.session.get("shopping_cart", {})
    key = str(product.id)
    current_quantity = int(cart.get(key, 0))

    if current_quantity < product.stock:
        cart[key] = current_quantity + 1

    request.session["shopping_cart"] = cart

    return redirect("shop:product_list")


def cart_detail(request):
    items, total = get_cart(request)

    return render(
        request,
        "shop/cart_detail.html",
        {
            "items": items,
            "total": total,
        }
    )


@require_POST
def cart_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get("shopping_cart", {})
    key = str(product.id)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    if quantity <= 0 or not product.is_available:
        cart.pop(key, None)
    else:
        cart[key] = min(quantity, product.stock)

    request.session["shopping_cart"] = cart

    return redirect("shop:cart_detail")


@require_POST
def cart_remove(request, product_id):
    cart = request.session.get("shopping_cart", {})
    cart.pop(str(product_id), None)

    request.session["shopping_cart"] = cart

    return redirect("shop:cart_detail")
