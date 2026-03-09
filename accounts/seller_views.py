from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product, Category, ProductImage, SpecialPrice
from orders.models import Order, OrderItem
from accounts.models import Seller
import os


def seller_required(request):
    return request.session.get('user_role') == 'seller'


def seller_dashboard(request):
    if not seller_required(request):
        messages.error(request, 'Please login as a seller.')
        return redirect('/accounts/login/')

    seller = Seller.objects.get(id=request.session['user_id'])
    products = Product.objects.filter(seller=seller)

    # FIX: Order now has items, not direct product FK — use items__product__seller
    orders = Order.objects.filter(
        items__product__seller=seller
    ).distinct()

    total_products = products.count()
    total_orders = orders.count()
    total_earnings = sum(o.total for o in orders if o.status != 'cancelled')

    recent_orders = orders.order_by('-created_at')[:5]

    return render(request, 'seller/dashboard.html', {
        'seller': seller,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_earnings': total_earnings,
        'recent_orders': recent_orders,
        'products': products[:4],
    })


def seller_products(request):
    if not seller_required(request):
        return redirect('/accounts/login/')

    seller = Seller.objects.get(id=request.session['user_id'])
    products = Product.objects.filter(seller=seller).select_related('category').order_by('-id')

    return render(request, 'seller/products.html', {
        'seller': seller,
        'products': products,
    })


def add_product(request):
    if not seller_required(request):
        return redirect('/accounts/login/')

    seller = Seller.objects.get(id=request.session['user_id'])
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')

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
            name=name, description=description, price=price,
            stock=stock, category=category, seller=seller, image=image,
        )

        # Multiple images
        extra_images = request.FILES.getlist('images')
        for i, img in enumerate(extra_images[:5]):
            ProductImage.objects.create(product=product, image=img, is_primary=(i == 0), order=i)

        # Special / sale price
        sale_price = request.POST.get('sale_price', '').strip()
        sale_start = request.POST.get('sale_start', '').strip()
        sale_end = request.POST.get('sale_end', '').strip()
        if sale_price and sale_start and sale_end:
            SpecialPrice.objects.update_or_create(
                product=product,
                defaults={'sale_price': sale_price, 'start_date': sale_start, 'end_date': sale_end}
            )

        messages.success(request, f'Product "{product.name}" added successfully!')
        return redirect('/seller/products/')

    return render(request, 'seller/add_product.html', {
        'categories': categories, 'seller': seller,
    })


def edit_product(request, pk):
    if not seller_required(request):
        return redirect('/accounts/login/')

    seller = Seller.objects.get(id=request.session['user_id'])
    product = get_object_or_404(Product, pk=pk, seller=seller)
    categories = Category.objects.all()

    if request.method == 'POST':
        product.name = request.POST.get('name', '').strip()
        product.description = request.POST.get('description', '').strip()
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')

        if category_id:
            try:
                product.category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                product.category = None

        if image:
            product.image = image

        product.save()

        # Special / sale price update
        sale_price = request.POST.get('sale_price', '').strip()
        sale_start = request.POST.get('sale_start', '').strip()
        sale_end = request.POST.get('sale_end', '').strip()
        if sale_price and sale_start and sale_end:
            SpecialPrice.objects.update_or_create(
                product=product,
                defaults={'sale_price': sale_price, 'start_date': sale_start, 'end_date': sale_end}
            )
        elif not sale_price:
            SpecialPrice.objects.filter(product=product).delete()

        messages.success(request, f'Product "{product.name}" updated!')
        return redirect('/seller/products/')

    return render(request, 'seller/edit_product.html', {
        'product': product, 'categories': categories, 'seller': seller,
    })


def delete_product(request, pk):
    if not seller_required(request):
        return redirect('/accounts/login/')

    seller = Seller.objects.get(id=request.session['user_id'])
    product = get_object_or_404(Product, pk=pk, seller=seller)
    name = product.name
    product.delete()
    messages.success(request, f'Product "{name}" deleted.')
    return redirect('/seller/products/')


def seller_orders(request):
    if not seller_required(request):
        return redirect('/accounts/login/')

    seller = Seller.objects.get(id=request.session['user_id'])

    # FIX: Use items__product__seller instead of product__seller
    orders = Order.objects.filter(
        items__product__seller=seller
    ).select_related('customer', 'address').prefetch_related('items__product').distinct().order_by('-created_at')

    return render(request, 'seller/orders.html', {
        'seller': seller,
        'orders': orders,
    })


def update_order_status(request, pk):
    if not seller_required(request):
        return redirect('/accounts/login/')

    seller = Seller.objects.get(id=request.session['user_id'])
    # FIX: query via items__product__seller
    order = get_object_or_404(
        Order, pk=pk, items__product__seller=seller
    )

    if request.method == 'POST':
        new_status = request.POST.get('status')
        valid_statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
        if new_status in valid_statuses:
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.pk} status updated to {new_status}.')

    return redirect('/seller/orders/')


def seller_discounts(request):
    if not seller_required(request):
        return redirect('/accounts/login/')

    from discounts.models import DiscountCode
    seller = Seller.objects.get(id=request.session['user_id'])
    codes = DiscountCode.objects.filter(created_by=seller).order_by('-created_at')

    return render(request, 'seller/discounts.html', {
        'seller': seller,
        'codes': codes,
    })
