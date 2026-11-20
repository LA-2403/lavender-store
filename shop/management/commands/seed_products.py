
from django.core.management.base import BaseCommand
from shop.models import Product


class Command(BaseCommand):
    help = "Add sample products to the Lavender Store database"

    def handle(self, *args, **options):
        products = [
            {
                "name": "Lavender Body Lotion",
                "description": "A gentle everyday body lotion.",
                "price": "299.00",
                "stock": 20,
                "is_available": True,
            },
            {
                "name": "Lavender Scented Candle",
                "description": "A relaxing scented candle.",
                "price": "199.00",
                "stock": 15,
                "is_available": True,
            },
            {
                "name": "Lavender Gift Set",
                "description": "A lovely gift set for someone special.",
                "price": "499.00",
                "stock": 10,
                "is_available": True,
            },
        ]

        for data in products:
            product, created = Product.objects.get_or_create(
                name=data["name"],
                defaults=data,
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Added: {product.name}"
                    )
                )
            else:
                self.stdout.write(
                    f"Already exists: {product.name}"
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Finished adding sample products!"
            )
        )
