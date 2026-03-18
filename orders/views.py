from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .models import Order, OrderItem, Address
from accounts.models import Customer
from decimal import Decimal


# ── CART HELPERS ──────────────────────────────────────────────

def get_cart(request):
    return request.session.get('cart', {})


def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def get_cart_totals(request):
    cart       = get_cart(request)
    cart_items = []
    cart_total = Decimal('0')

    for product_id, quantity in cart.items():
        try:
            product  = Product.objects.get(id=int(product_id))
            subtotal = product.price * quantity
            cart_total += subtotal
            cart_items.append({
                'product':  product,
                'quantity': quantity,
                'subtotal': round(subtotal, 2),
            })
        except Product.DoesNotExist:
            pass

    discount_amount  = Decimal(str(request.session.get('discount_amount', 0)))
    discounted_total = max(cart_total - discount_amount, Decimal('0'))
    shipping         = Decimal('0') if discounted_total >= 499 else (Decimal('49') if cart_items else Decimal('0'))
    tax              = round(discounted_total * Decimal('0.05'), 2)
    grand_total      = round(discounted_total + shipping + tax, 2)

    return {
        'cart_items':       cart_items,
        'cart_total':       round(cart_total, 2),
        'discount_amount':  round(discount_amount, 2),
        'discounted_total': round(discounted_total, 2),
        'tax':              tax,
        'shipping':         shipping,
        'grand_total':      grand_total,
        'discount_code':    request.session.get('discount_code', ''),
    }


# ── CART VIEWS ────────────────────────────────────────────────

def cart_view(request):
    data = get_cart_totals(request)
    return render(request, 'orders/cart.html', data)


def add_to_cart(request, product_id):
    if request.method == 'POST':
        product  = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        cart     = get_cart(request)
        pid      = str(product_id)

        if pid in cart:
            cart[pid] = min(cart[pid] + quantity, product.stock)
        else:
            cart[pid] = min(quantity, product.stock)

        save_cart(request, cart)
        messages.success(request, f'"{product.name}" added to cart!')

    return redirect(request.META.get('HTTP_REFERER', '/products/'))


def increase_quantity(request, product_id):
    cart = get_cart(request)
    pid  = str(product_id)
    if pid in cart:
        product = get_object_or_404(Product, id=product_id)
        if cart[pid] < product.stock:
            cart[pid] += 1
            save_cart(request, cart)
    return redirect('/cart/')


def decrease_quantity(request, product_id):
    cart = get_cart(request)
    pid  = str(product_id)
    if pid in cart:
        if cart[pid] > 1:
            cart[pid] -= 1
        else:
            del cart[pid]
        save_cart(request, cart)
    return redirect('/cart/')


def remove_from_cart(request, product_id):
    cart = get_cart(request)
    pid  = str(product_id)
    if pid in cart:
        del cart[pid]
        save_cart(request, cart)
        messages.success(request, 'Item removed from cart.')
    return redirect('/cart/')


def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True
    messages.success(request, 'Cart cleared.')
    return redirect('/cart/')


# ── CHECKOUT ──────────────────────────────────────────────────

def checkout(request):
    if not request.session.get('user_id'):
        messages.warning(request, 'Please login to continue.')
        return redirect('/accounts/login/')
    if request.session.get('user_role') != 'customer':
        messages.error(request, 'Only customers can place orders.')
        return redirect('/cart/')

    cart = get_cart(request)
    if not cart:
        messages.warning(request, 'Your cart is empty.')
        return redirect('/cart/')

    customer        = get_object_or_404(Customer, id=request.session['user_id'])
    totals          = get_cart_totals(request)
    saved_addresses = Address.objects.filter(customer=customer)

    if request.method == 'POST':
        saved_addr_id = request.POST.get('use_saved_address', '').strip()

        if saved_addr_id:
            address = get_object_or_404(Address, id=saved_addr_id, customer=customer)
        else:
            name    = request.POST.get('name',    '').strip() or customer.name
            phone   = request.POST.get('phone',   '').strip()
            house   = request.POST.get('house',   '').strip()
            city    = request.POST.get('city',    '').strip()
            state   = request.POST.get('state',   '').strip()
            pincode = request.POST.get('pincode', '').strip()

            if not house or not city or not state or not pincode:
                messages.error(request, 'Please fill all address fields.')
                return render(request, 'orders/checkout.html', {
                    **totals,
                    'saved_addresses': saved_addresses,
                    'customer':        customer,
                })

            address = Address.objects.create(
                customer=customer, name=name, full_name=name,
                phone=phone, house=house, city=city,
                state=state, pincode=pincode,
            )

        # Create ONE order with multiple OrderItems
        order = Order.objects.create(
            customer        = customer,
            address         = address,
            payment_method  = 'cod',
            discount_code   = totals['discount_code'] or '',
            discount_amount = totals['discount_amount'],
            subtotal        = totals['cart_total'],
            shipping        = totals['shipping'],
            tax             = totals['tax'],
            total           = totals['grand_total'],
        )

        # Create order items
        for pid, qty in cart.items():
            try:
                product = Product.objects.get(id=int(pid))
                OrderItem.objects.create(
                    order         = order,
                    product       = product,
                    product_name  = product.name,
                    product_price = product.price,
                    quantity      = qty,
                    subtotal      = round(float(product.price) * qty, 2),
                )
            except Product.DoesNotExist:
                pass

        # Clear session
        request.session.pop('cart',            None)
        request.session.pop('discount_code',   None)
        request.session.pop('discount_amount', None)
        request.session['last_order_id']    = order.id
        request.session['last_grand_total'] = float(totals['grand_total'])
        request.session.modified = True

        messages.success(request, 'Order placed successfully!')
        return redirect('/cart/confirmation/')

    return render(request, 'orders/checkout.html', {
        **totals,
        'saved_addresses': saved_addresses,
        'customer':        customer,
    })


# ── CONFIRMATION ──────────────────────────────────────────────

def confirmation(request):
    if request.session.get('user_role') != 'customer':
        return redirect('/accounts/login/')

    order_id    = request.session.get('last_order_id')
    grand_total = request.session.get('last_grand_total', 0)

    if not order_id:
        return redirect('/')

    order   = get_object_or_404(Order, id=order_id)
    items   = order.items.select_related('product')
    address = order.address

    return render(request, 'orders/confirmation.html', {
        'order':       order,
        'items':       items,
        'grand_total': grand_total,
        'address':     address,
    })


# ── MY ORDERS ─────────────────────────────────────────────────

def my_orders(request):
    if request.session.get('user_role') != 'customer':
        messages.warning(request, 'Please login to view your orders.')
        return redirect('/accounts/login/')

    customer = get_object_or_404(Customer, id=request.session['user_id'])
    status   = request.GET.get('status', '')
    orders   = Order.objects.filter(customer=customer).prefetch_related('items__product').order_by('-created_at')

    if status:
        orders = orders.filter(status=status)

    return render(request, 'orders/my_orders.html', {
        'orders':          orders,
        'customer':        customer,
        'selected_status': status,
    })


# ── ORDER DETAIL ──────────────────────────────────────────────

def order_detail(request, pk):
    if request.session.get('user_role') != 'customer':
        return redirect('/accounts/login/')
    order = get_object_or_404(Order, pk=pk, customer_id=request.session['user_id'])
    items = order.items.select_related('product')
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'items': items,
    })