import csv
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Sum, Count, Q
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta

from accounts.models import Customer, Seller
from products.models import Product, Category
from orders.models import Order
from discounts.models import DiscountCode
from .models import Banner


# ─── Auth Helper ────────────────────────────────────────────────────────────

def admin_required(request):
    """Returns True if request is from admin session, else False."""
    return request.session.get('user_role') == 'admin'


# ─── 1. Admin Home / Dashboard ───────────────────────────────────────────────

def admin_home(request):
    if not admin_required(request):
        return redirect('/accounts/login/')

    # Stats
    total_customers = Customer.objects.count()
    total_sellers = Seller.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    pending_sellers = Seller.objects.filter(is_approved=False).count()

    # Revenue: sum of all delivered orders
    revenue_data = Order.objects.filter(status='delivered').aggregate(total=Sum('total'))
    total_revenue = revenue_data['total'] or 0

    # Recent 5 orders
    recent_orders = Order.objects.select_related('customer', 'address').prefetch_related('items').order_by('-created_at')[:5]

    from products.stock_utils import get_low_stock_products
    low_stock = get_low_stock_products()

    context = {
        'name': request.session.get('user_name'),
        'total_customers': total_customers,
        'total_sellers': total_sellers,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'pending_sellers': pending_sellers,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock[:10],
        'low_stock_count': low_stock.count(),
    }
    return render(request, 'dashboard/home.html', context)


# ─── 2. Manage Customers ────────────────────────────────────────────────────

def manage_customers(request):
    if not admin_required(request):
        return redirect('/accounts/login/')

    search = request.GET.get('search', '').strip()
    customers = Customer.objects.all().order_by('-id')

    if search:
        customers = customers.filter(
            Q(name__icontains=search) | Q(email__icontains=search)
        )

    context = {
        'name': request.session.get('user_name'),
        'customers': customers,
        'search': search,
    }
    return render(request, 'dashboard/customers.html', context)


@require_POST
def delete_customer(request, pk):
    if not admin_required(request):
        return redirect('/accounts/login/')

    customer = get_object_or_404(Customer, pk=pk)
    customer_name = customer.name
    customer.delete()
    messages.success(request, f'Customer "{customer_name}" deleted successfully.')
    return redirect('dashboard:customers')


# ─── 3. Manage Sellers ──────────────────────────────────────────────────────

def manage_sellers(request):
    if not admin_required(request):
        return redirect('/accounts/login/')

    sellers = Seller.objects.all().order_by('-id')
    context = {
        'name': request.session.get('user_name'),
        'sellers': sellers,
    }
    return render(request, 'dashboard/sellers.html', context)


@require_POST
def approve_seller(request, pk):
    if not admin_required(request):
        return redirect('/accounts/login/')

    seller = get_object_or_404(Seller, pk=pk)
    seller.is_approved = True
    seller.save()
    messages.success(request, f'Seller "{seller.name}" has been approved.')
    return redirect('dashboard:sellers')


@require_POST
def reject_seller(request, pk):
    if not admin_required(request):
        return redirect('/accounts/login/')

    seller = get_object_or_404(Seller, pk=pk)
    seller.is_approved = False
    seller.save()
    messages.warning(request, f'Seller "{seller.name}" has been rejected/suspended.')
    return redirect('dashboard:sellers')


@require_POST
def delete_seller(request, pk):
    if not admin_required(request):
        return redirect('/accounts/login/')

    seller = get_object_or_404(Seller, pk=pk)
    seller_name = seller.name
    seller.delete()
    messages.success(request, f'Seller "{seller_name}" deleted successfully.')
    return redirect('dashboard:sellers')


# ─── 4. Manage Products ─────────────────────────────────────────────────────

def manage_products(request):
    if not admin_required(request):
        return redirect('/accounts/login/')

    search = request.GET.get('search', '').strip()
    products = Product.objects.select_related('seller', 'category').order_by('-id')

    if search:
        products = products.filter(name__icontains=search)

    context = {
        'name': request.session.get('user_name'),
        'products': products,
        'search': search,
    }
    return render(request, 'dashboard/products.html', context)


@require_POST
def delete_product(request, pk):
    if not admin_required(request):
        return redirect('/accounts/login/')

    product = get_object_or_404(Product, pk=pk)
    product_name = product.name
    product.delete()
    messages.success(request, f'Product "{product_name}" deleted successfully.')
    return redirect('dashboard:products')


# ─── 5. Manage Orders ───────────────────────────────────────────────────────

def manage_orders(request):
    if not admin_required(request):
        return redirect('/accounts/login/')

    status_filter = request.GET.get('status', '').strip()
    orders = Order.objects.select_related('customer', 'address').prefetch_related('items').order_by('-created_at')

    if status_filter:
        orders = orders.filter(status=status_filter)

    status_choices = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']

    context = {
        'name': request.session.get('user_name'),
        'orders': orders,
        'status_filter': status_filter,
        'status_choices': status_choices,
    }
    return render(request, 'dashboard/orders.html', context)


@require_POST
def update_order_status(request, pk):
    if not admin_required(request):
        return redirect('/accounts/login/')

    order = get_object_or_404(Order, pk=pk)
    new_status = request.POST.get('new_status', '').strip()
    valid_statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']

    if new_status in valid_statuses:
        order.status = new_status
        order.save()
        messages.success(request, f'Order #{order.pk} status updated to "{new_status}".')
    else:
        messages.error(request, 'Invalid status selected.')

    return redirect('dashboard:orders')


# ─── 6. Manage Discounts ────────────────────────────────────────────────────

def manage_discounts(request):
    if not admin_required(request):
        return redirect('/accounts/login/')

    discounts = DiscountCode.objects.select_related('created_by').order_by('-created_at')
    context = {
        'name': request.session.get('user_name'),
        'discounts': discounts,
    }
    return render(request, 'dashboard/discounts.html', context)


@require_POST
def delete_discount(request, pk):
    if not admin_required(request):
        return redirect('/accounts/login/')

    discount = get_object_or_404(DiscountCode, pk=pk)
    code = discount.code
    discount.delete()
    messages.success(request, f'Discount code "{code}" deleted successfully.')
    return redirect('dashboard:discounts')


# ─── 7. Revenue Analytics ───────────────────────────────────────────────────

def revenue_analytics(request):
    if not admin_required(request):
        return redirect('/accounts/login/')

    # Last 6 months
    today = timezone.now()
    months_data = []
    months_labels = []
    revenue_values = []
    order_counts = []

    for i in range(5, -1, -1):
        # Go back i months from current month
        month_dt = today.replace(day=1) - timedelta(days=i * 30)
        month_num = month_dt.month
        year_num = month_dt.year
        label = month_dt.strftime('%b %Y')

        delivered = Order.objects.filter(
            created_at__year=year_num,
            created_at__month=month_num,
            status='delivered'
        )
        rev = delivered.aggregate(total=Sum('total'))['total'] or 0
        count = Order.objects.filter(
            created_at__year=year_num,
            created_at__month=month_num
        ).count()

        months_labels.append(label)
        revenue_values.append(float(rev))
        order_counts.append(count)

    # Top 5 products by orders count — via OrderItem
    from orders.models import OrderItem
    top_products_qs = (
        OrderItem.objects
        .values('product__name')
        .annotate(total_sold=Count('id'))
        .order_by('-total_sold')[:5]
    )
    top_product_labels = [p['product__name'] for p in top_products_qs]
    top_product_values = [p['total_sold'] for p in top_products_qs]

    # Overall summary
    total_revenue = Order.objects.filter(status='delivered').aggregate(
        total=Sum('total')
    )['total'] or 0
    total_orders = Order.objects.count()
    delivered_orders = Order.objects.filter(status='delivered').count()

    context = {
        'name': request.session.get('user_name'),
        'months_labels': json.dumps(months_labels),
        'revenue_values': json.dumps(revenue_values),
        'order_counts': json.dumps(order_counts),
        'top_product_labels': json.dumps(top_product_labels),
        'top_product_values': json.dumps(top_product_values),
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'delivered_orders': delivered_orders,
    }
    return render(request, 'dashboard/analytics.html', context)


# ─── 8. Manage Banners ──────────────────────────────────────────────────────

def manage_banners(request):
    if not admin_required(request):
        return redirect('/accounts/login/')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        link = request.POST.get('link', '').strip()
        order = request.POST.get('order', 0)
        is_active = request.POST.get('is_active') == 'on'
        image = request.FILES.get('image')

        if not title or not image:
            messages.error(request, 'Title and image are required.')
        else:
            Banner.objects.create(
                title=title,
                image=image,
                link=link or None,
                order=int(order) if order else 0,
                is_active=is_active,
            )
            messages.success(request, f'Banner "{title}" added successfully.')
        return redirect('dashboard:banners')

    banners = Banner.objects.all()
    context = {
        'name': request.session.get('user_name'),
        'banners': banners,
    }
    return render(request, 'dashboard/banners.html', context)


@require_POST
def delete_banner(request, pk):
    if not admin_required(request):
        return redirect('/accounts/login/')

    banner = get_object_or_404(Banner, pk=pk)
    title = banner.title
    banner.delete()
    messages.success(request, f'Banner "{title}" deleted successfully.')
    return redirect('dashboard:banners')


# ─── CSV Exports ──────────────────────────────────────────────────────────────

def export_orders_csv(request):
    if not admin_required(request):
        return redirect('/accounts/login/')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = (
        f'attachment; filename="shopease_orders_{timezone.now().strftime("%Y%m%d")}.csv"'
    )
    writer = csv.writer(response)
    writer.writerow([
        'Order ID', 'Customer Name', 'Customer Email',
        'Items', 'Subtotal', 'Discount', 'Shipping', 'Tax', 'Total',
        'Payment Method', 'Status', 'Date',
    ])
    orders = Order.objects.select_related('customer').prefetch_related('items').order_by('-created_at')
    for order in orders:
        items_str = ', '.join(f"{i.product_name}(x{i.quantity})" for i in order.items.all())
        writer.writerow([
            order.pk, order.customer.name, order.customer.email,
            items_str, order.subtotal, order.discount_amount,
            order.shipping, order.tax, order.total,
            order.get_payment_method_display(), order.status,
            order.created_at.strftime('%Y-%m-%d %H:%M'),
        ])
    return response


def export_products_csv(request):
    if not admin_required(request):
        return redirect('/accounts/login/')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = (
        f'attachment; filename="shopease_products_{timezone.now().strftime("%Y%m%d")}.csv"'
    )
    writer = csv.writer(response)
    writer.writerow(['Product ID', 'Name', 'Category', 'Seller', 'Price', 'Stock', 'Created'])
    for p in Product.objects.select_related('category', 'seller').order_by('-id'):
        writer.writerow([
            p.pk, p.name,
            p.category.name if p.category else 'N/A',
            p.seller.name, p.price, p.stock,
            p.created_at.strftime('%Y-%m-%d'),
        ])
    return response


def export_customers_csv(request):
    if not admin_required(request):
        return redirect('/accounts/login/')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = (
        f'attachment; filename="shopease_customers_{timezone.now().strftime("%Y%m%d")}.csv"'
    )
    writer = csv.writer(response)
    writer.writerow(['Customer ID', 'Name', 'Email', 'Phone', 'Total Orders', 'Total Spent'])
    customers = Customer.objects.annotate(
        order_count=Count('orders'),
        total_spent=Sum('orders__total'),
    ).order_by('-order_count')
    for c in customers:
        writer.writerow([
            c.pk, c.name, c.email, c.phone,
            c.order_count, round(c.total_spent or 0, 2),
        ])
    return response

