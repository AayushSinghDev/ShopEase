from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Customer, Seller
from products.models import Product
from orders.models import Order


def check_admin(request):
    return request.session.get('user_role') == 'admin'


# ── SELLERS ───────────────────────────────────────────────────

def admin_sellers(request):
    if not check_admin(request):
        messages.error(request, 'Admin access required.')
        return redirect('/accounts/login/')

    if request.method == 'POST':
        action    = request.POST.get('action')
        seller_id = request.POST.get('seller_id')
        seller    = get_object_or_404(Seller, id=seller_id)

        if action == 'approve':
            seller.is_approved = True
            seller.save()
            messages.success(request, f'Seller "{seller.name}" approved!')
        elif action == 'reject':
            seller.is_approved = False
            seller.save()
            messages.warning(request, f'Seller "{seller.name}" approval revoked.')
        elif action == 'delete':
            name = seller.name
            seller.delete()
            messages.success(request, f'Seller "{name}" deleted.')

        return redirect('/admin-panel/sellers/')

    sellers = Seller.objects.all().order_by('-id')
    return render(request, 'admin_panel/sellers.html', {
        'sellers':       sellers,
        'pending_count': sellers.filter(is_approved=False).count(),
        'approved_count': sellers.filter(is_approved=True).count(),
    })


# ── CUSTOMERS ─────────────────────────────────────────────────

def admin_customers(request):
    if not check_admin(request):
        return redirect('/accounts/login/')

    if request.method == 'POST':
        customer = get_object_or_404(Customer, id=request.POST.get('customer_id'))
        name     = customer.name
        customer.delete()
        messages.success(request, f'Customer "{name}" deleted.')
        return redirect('/admin-panel/customers/')

    customers = Customer.objects.all().order_by('-id')
    return render(request, 'admin_panel/customers.html', {
        'customers': customers,
    })


# ── PRODUCTS ──────────────────────────────────────────────────

def admin_products(request):
    if not check_admin(request):
        return redirect('/accounts/login/')

    if request.method == 'POST':
        product = get_object_or_404(Product, id=request.POST.get('product_id'))
        name    = product.name
        product.delete()
        messages.success(request, f'Product "{name}" deleted.')
        return redirect('/admin-panel/products/')

    products = Product.objects.all().select_related('seller', 'category').order_by('-id')
    return render(request, 'admin_panel/products.html', {
        'products': products,
    })


# ── ORDERS ────────────────────────────────────────────────────

def admin_orders(request):
    if not check_admin(request):
        return redirect('/accounts/login/')

    if request.method == 'POST':
        order      = get_object_or_404(Order, id=request.POST.get('order_id'))
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        messages.success(request, f'Order #{order.pk} updated to "{new_status}".')
        return redirect('/admin-panel/orders/')

    orders = Order.objects.all().select_related('customer', 'address').prefetch_related('items').order_by('-created_at')
    return render(request, 'admin_panel/orders.html', {
        'orders': orders,
    })