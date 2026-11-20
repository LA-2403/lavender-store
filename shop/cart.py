
from decimal import Decimal
from .models import Product


def get_cart(request):
    cart_data = request.session.get("shopping_cart", {})

    products = Product.objects.filter(
        id__in=cart_data.keys(),
        is_available=True
    )

    items = []
    total = Decimal("0.00")

    for product in products:
        quantity = min(
            int(cart_data.get(str(product.id), 0)),
            product.stock
        )

        if quantity < 1:
            continue

        line_total = product.price * quantity

        items.append({
            "product": product,
            "quantity": quantity,
            "line_total": line_total,
        })

        total += line_total

    return items, total


def get_cart_count(request):
    cart = request.session.get("shopping_cart", {})
    return sum(int(quantity) for quantity in cart.values())
