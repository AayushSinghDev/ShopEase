from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product, Category
from orders.models import Order, OrderItem
from accounts.models import Seller
import os


def seller_required(request):
    return request.session.get('user_role') == 'seller'


# ── SELLER DASHBOARD ──────────────────────────────────────────
def seller_dashboard(request):
    if not seller_required(request):
        messages.error(request, 'Please login as a seller.')
        return redirect('/accounts/login/')

    seller  = Seller.objects.get(id=request.session['user_id'])
    products = Product.objects.filter(seller=seller)

    # Orders that contain seller's products (via OrderItem)
    order_items = OrderItem.objects.filter(
        product__seller=seller
    ).select_related('order', 'product')

    # Unique orders
    order_ids      = order_items.values_list('order_id', flat=True).distinct()
    orders         = Order.objects.filter(id__in=order_ids)

    total_products = products.count()
    total_orders   = orders.count()
    total_earnings = sum(
        o.total for o in orders if o.status != 'cancelled'
    )
    recent_orders  = orders.order_by('-created_at')[:5]

    return render(request, 'seller/dashboard.html', {
        'seller':          seller,
        'total_products':  total_products,
        'total_orders':    total_orders,
        'total_earnings':  total_earnings,
        'recent_orders':   recent_orders,
        'products':        products[:4],
    })


# ── SELLER PRODUCTS ───────────────────────────────────────────
def seller_products(request):
    if not seller_required(request):
        return redirect('/accounts/login/')

    seller   = Seller.objects.get(id=request.session['user_id'])
    products = Product.objects.filter(seller=seller).select_related('category').order_by('-id')

    return render(request, 'seller/products.html', {
        'seller':   seller,
        'products': products,
    })


# ── ADD PRODUCT ───────────────────────────────────────────────
def add_product(request):
    if not seller_required(request):
        return redirect('/accounts/login/')

    seller     = Seller.objects.get(id=request.session['user_id'])
    categories = Category.objects.all()

    if request.method == 'POST':
        name        = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        price       = request.POST.get('price')
        stock       = request.POST.get('stock')
        category_id = request.POST.get('category')
        image       = request.FILES.get('image')

        if not name or not price or not stock:
            messages.error(request, 'Name, price and stock are required.')
            return render(request, 'seller/add_product.html', {
                'categories': categories, 'seller': seller
            })

        category = None
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                pass

        product = Product.objects.create(
            name=name, description=description,
            price=price, stock=stock,
            category=category, seller=seller, image=image,
        )
        messages.success(request, f'Product "{product.name}" added successfully!')
        return redirect('/seller/products/')

    return render(request, 'seller/add_product.html', {
        'categories': categories,
        'seller':     seller,
    })


# ── EDIT PRODUCT ──────────────────────────────────────────────
def edit_product(request, pk):
    if not seller_required(request):
        return redirect('/accounts/login/')

    seller     = Seller.objects.get(id=request.session['user_id'])
    product    = get_object_or_404(Product, pk=pk, seller=seller)
    categories = Category.objects.all()

    if request.method == 'POST':
        product.name        = request.POST.get('name', '').strip()
        product.description = request.POST.get('description', '').strip()
        product.price       = request.POST.get('price')
        product.stock       = request.POST.get('stock')
        category_id         = request.POST.get('category')
        image               = request.FILES.get('image')

        if category_id:
            try:
                product.category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                product.category = None
        if image:
            product.image = image

        product.save()
        messages.success(request, f'Product "{product.name}" updated!')
        return redirect('/seller/products/')

    return render(request, 'seller/edit_product.html', {
        'product':    product,
        'categories': categories,
        'seller':     seller,
    })


# ── DELETE PRODUCT ────────────────────────────────────────────
def delete_product(request, pk):
    if not seller_required(request):
        return redirect('/accounts/login/')

    seller  = Seller.objects.get(id=request.session['user_id'])
    product = get_object_or_404(Product, pk=pk, seller=seller)
    name    = product.name
    product.delete()
    messages.success(request, f'Product "{name}" deleted.')
    return redirect('/seller/products/')


# ── SELLER ORDERS ─────────────────────────────────────────────
def seller_orders(request):
    if not seller_required(request):
        return redirect('/accounts/login/')

    seller = Seller.objects.get(id=request.session['user_id'])

    # Get order items that belong to this seller's products
    order_items = OrderItem.objects.filter(
        product__seller=seller
    ).select_related('order', 'product', 'order__customer', 'order__address').order_by('-order__created_at')

    return render(request, 'seller/orders.html', {
        'seller':      seller,
        'order_items': order_items,
    })


# ── UPDATE ORDER STATUS ───────────────────────────────────────
def update_order_status(request, pk):
    if not seller_required(request):
        return redirect('/accounts/login/')

    seller = Seller.objects.get(id=request.session['user_id'])

    # Find order that has items from this seller
    order = get_object_or_404(Order, pk=pk)
    # Verify this seller owns at least one item in this order
    if not OrderItem.objects.filter(order=order, product__seller=seller).exists():
        messages.error(request, 'You do not have permission to update this order.')
        return redirect('/seller/orders/')

    if request.method == 'POST':
        new_status    = request.POST.get('status')
        valid_statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
        if new_status in valid_statuses:
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.pk} updated to "{new_status}".')

    return redirect('/seller/orders/')


# ── SELLER DISCOUNTS ──────────────────────────────────────────
def seller_discounts(request):
    if not seller_required(request):
        return redirect('/accounts/login/')

    from discounts.models import DiscountCode
    seller = Seller.objects.get(id=request.session['user_id'])
    codes  = DiscountCode.objects.filter(created_by=seller).order_by('-created_at')

    return render(request, 'seller/discounts.html', {
        'seller': seller,
        'codes':  codes,
    })