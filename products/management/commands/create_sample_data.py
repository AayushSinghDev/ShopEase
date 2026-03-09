from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'ShopEase ke liye sample/demo data create karo'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...\n')

        # ── SuperAdmin ──────────────────────────────────────────────────────
        from accounts.models import SuperAdmin, Seller, Customer
        admin, created = SuperAdmin.objects.get_or_create(
            email='admin@shopease.com',
            defaults={
                'username': 'admin',
                'password': make_password('admin123'),
            }
        )
        if created:
            self.stdout.write('  ✓ SuperAdmin created')
        else:
            self.stdout.write('  · SuperAdmin already exists')

        # ── Sellers (2) ─────────────────────────────────────────────────────
        seller1, _ = Seller.objects.get_or_create(
            email='techstore@shopease.com',
            defaults={
                'name': 'TechStore India',
                'phone': '9876543210',
                'password': make_password('seller123'),
                'is_approved': True,
            }
        )
        seller2, _ = Seller.objects.get_or_create(
            email='fashionhub@shopease.com',
            defaults={
                'name': 'Fashion Hub',
                'phone': '9876543211',
                'password': make_password('seller123'),
                'is_approved': True,
            }
        )
        self.stdout.write('  ✓ Sellers created')

        # ── Customers (3) ───────────────────────────────────────────────────
        customers_data = [
            ('Rahul Sharma',  'rahul@example.com',  '9111111111'),
            ('Priya Patel',   'priya@example.com',  '9222222222'),
            ('Amit Kumar',    'amit@example.com',   '9333333333'),
        ]
        for name, email, phone in customers_data:
            Customer.objects.get_or_create(
                email=email,
                defaults={
                    'name': name,
                    'phone': phone,
                    'password': make_password('customer123'),
                }
            )
        self.stdout.write('  ✓ Customers created')

        # ── Categories (5) ──────────────────────────────────────────────────
        from products.models import Category, Product, SpecialPrice
        categories = {}
        for cat_name in ['Electronics', 'Clothing', 'Books', 'Home & Kitchen', 'Sports']:
            cat, _ = Category.objects.get_or_create(name=cat_name)
            categories[cat_name] = cat
        self.stdout.write('  ✓ Categories created')

        # ── Products (10 — 2 per category) ──────────────────────────────────
        products_data = [
            ('Wireless Bluetooth Headphones', 'Premium quality wireless headphones with 30hr battery life, deep bass and noise cancellation.', 1999, 50, seller1, 'Electronics'),
            ('Smart Watch Pro',              'Fitness tracker with heart rate monitor, sleep tracking, and 7-day battery.', 2999, 30, seller1, 'Electronics'),
            ('Premium Cotton T-Shirt',       'Breathable 100% cotton t-shirt available in 8 colors. Machine washable.', 499, 100, seller2, 'Clothing'),
            ('Slim Fit Denim Jeans',         'Stretchable slim fit denim jeans for all-day comfort.', 1299, 75, seller2, 'Clothing'),
            ('Python Programming Bible',     'Complete Python guide from beginner to advanced with 500+ exercises.', 399, 200, seller1, 'Books'),
            ('Django Web Development',       'Full-stack web development with Django 5.0 — build real projects.', 499, 150, seller1, 'Books'),
            ('Automatic Coffee Maker',       'Drip coffee maker 1.5L with timer, warming plate, and auto shutoff.', 1499, 25, seller2, 'Home & Kitchen'),
            ('Non-stick Cookware Set',       'Premium 3-piece non-stick pan set with glass lids. Induction compatible.', 1999, 40, seller2, 'Home & Kitchen'),
            ('Yoga Mat Premium',             'Anti-slip 6mm thick eco-friendly yoga mat with carry strap.', 699, 80, seller1, 'Sports'),
            ('Cast Iron Dumbbell 5kg Pair',  'Premium cast iron dumbbell pair with rubber grip for home workouts.', 899, 60, seller1, 'Sports'),
        ]
        created_products = []
        for name, desc, price, stock, seller, cat_name in products_data:
            p, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    'description': desc,
                    'price': price,
                    'stock': stock,
                    'seller': seller,
                    'category': categories[cat_name],
                }
            )
            created_products.append(p)
        self.stdout.write(f'  ✓ {len(created_products)} Products created')

        # ── Sale Price on Headphones ─────────────────────────────────────────
        from django.utils import timezone
        from datetime import timedelta
        today = timezone.now().date()
        headphones = Product.objects.filter(name='Wireless Bluetooth Headphones').first()
        if headphones:
            SpecialPrice.objects.get_or_create(
                product=headphones,
                defaults={
                    'sale_price': 1499,
                    'start_date': today - timedelta(days=1),
                    'end_date': today + timedelta(days=30),
                }
            )
            self.stdout.write('  ✓ Sale price on Wireless Headphones')

        # ── Discount Codes ───────────────────────────────────────────────────
        from discounts.models import DiscountCode
        from datetime import date
        DiscountCode.objects.get_or_create(
            code='WELCOME10',
            defaults={
                'discount_type': 'percentage',
                'discount_value': 10,
                'minimum_order_value': 500,
                'expiry_date': date(2027, 12, 31),
                'usage_limit': 100,
                'created_by': seller1,
            }
        )
        DiscountCode.objects.get_or_create(
            code='FLAT100',
            defaults={
                'discount_type': 'flat',
                'discount_value': 100,
                'minimum_order_value': 999,
                'expiry_date': date(2027, 12, 31),
                'usage_limit': 50,
                'created_by': seller2,
            }
        )
        self.stdout.write('  ✓ Discount codes: WELCOME10, FLAT100')

        # ── Banner ───────────────────────────────────────────────────────────
        try:
            from dashboard.models import Banner
            Banner.objects.get_or_create(
                title='Welcome to ShopEase!',
                defaults={
                    'subtitle': 'India ka best online shopping destination. Great deals every day!',
                    'is_active': True,
                }
            )
            self.stdout.write('  ✓ Welcome Banner created')
        except Exception:
            pass  # Banner model mein extra fields ho sakti hain

        # ── Final Summary ────────────────────────────────────────────────────
        self.stdout.write(self.style.SUCCESS(
            '\n'
            '🎉 Sample data created successfully!\n'
            '─────────────────────────────────────\n'
            '  Admin:    admin@shopease.com     / admin123\n'
            '  Seller 1: techstore@shopease.com / seller123\n'
            '  Seller 2: fashionhub@shopease.com/ seller123\n'
            '  Customer: rahul@example.com      / customer123\n'
            '─────────────────────────────────────\n'
            '  Discount Codes: WELCOME10 (10% off), FLAT100 (₹100 off)\n'
            '─────────────────────────────────────\n'
        ))
