import json
import hmac
import hashlib
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.conf import settings
from django.db.models import F

from products.models import Product
from .models import Order, OrderItem, Address
from accounts.models import Customer
from discounts.models import DiscountCode


# ─── Cart Helpers ───────────────────────────────────────────────────────────

def get_cart(request):
    """Returns cart dict from session: {product_id: quantity}"""
    return request.session.get('cart', {})


def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def _build_cart_totals(request, cart):
    """
    Shared cart calculation: returns (cart_items, subtotal, discount_amount, tax, shipping, grand_total)
    """
    cart_items = []
    subtotal = Decimal('0')

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            item_subtotal = product.price * quantity
            subtotal += item_subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': round(item_subtotal, 2),
            })
        except Product.DoesNotExist:
            pass

    discount_amount = Decimal(str(request.session.get('discount_amount', 0)))
    discounted = max(subtotal - discount_amount, Decimal('0'))
    shipping = Decimal('0') if discounted >= 499 else (Decimal('49') if cart_items else Decimal('0'))
    tax = round(discounted * Decimal('0.05'), 2)
    grand_total = round(discounted + shipping + tax, 2)

    return cart_items, round(subtotal, 2), round(discount_amount, 2), tax, shipping, grand_total


# ─── Cart Views ─────────────────────────────────────────────────────────────

def cart_view(request):
    cart = get_cart(request)
    cart_items, subtotal, discount_amount, tax, shipping, grand_total = _build_cart_totals(request, cart)

    return render(request, 'orders/cart.html', {
        'cart_items': cart_items,
        'cart_total': subtotal,
        'discount_amount': discount_amount,
        'discounted_total': round(max(subtotal - discount_amount, Decimal('0')), 2),
        'tax': tax,
        'shipping': shipping,
        'grand_total': grand_total,
    })


def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        cart = get_cart(request)
        pid = str(product_id)
        cart[pid] = min(cart.get(pid, 0) + quantity, product.stock)
        save_cart(request, cart)
        messages.success(request, f'"{product.name}" added to cart!')
    return redirect(request.META.get('HTTP_REFERER', '/products/'))


def increase_quantity(request, product_id):
    cart = get_cart(request)
    pid = str(product_id)
    if pid in cart:
        product = get_object_or_404(Product, id=product_id)
        if cart[pid] < product.stock:
            cart[pid] += 1
            save_cart(request, cart)
    return redirect('/orders/cart/')


def decrease_quantity(request, product_id):
    cart = get_cart(request)
    pid = str(product_id)
    if pid in cart:
        if cart[pid] > 1:
            cart[pid] -= 1
        else:
            del cart[pid]
        save_cart(request, cart)
    return redirect('/orders/cart/')


def remove_from_cart(request, product_id):
    cart = get_cart(request)
    pid = str(product_id)
    if pid in cart:
        del cart[pid]
        save_cart(request, cart)
        messages.success(request, 'Item removed from cart.')
    return redirect('/orders/cart/')


def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True
    messages.success(request, 'Cart cleared.')
    return redirect('/orders/cart/')


# ─── Checkout ────────────────────────────────────────────────────────────────

def checkout(request):
    if not request.session.get('user_id'):
        messages.warning(request, 'Please login to proceed to checkout.')
        return redirect('/accounts/login/')
    if request.session.get('user_role') != 'customer':
        messages.error(request, 'Only customers can place orders.')
        return redirect('/orders/cart/')

    cart = get_cart(request)
    if not cart:
        messages.warning(request, 'Your cart is empty.')
        return redirect('/orders/cart/')

    customer = get_object_or_404(Customer, id=request.session['user_id'])
    addresses = Address.objects.filter(customer=customer).order_by('-is_default', '-id')
    cart_items, subtotal, discount_amount, tax, shipping, grand_total = _build_cart_totals(request, cart)
    discount_code_str = request.session.get('discount_code', '')

    context = {
        'customer': customer,
        'addresses': addresses,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'discount_amount': discount_amount,
        'discount_code': discount_code_str,
        'tax': tax,
        'shipping': shipping,
        'grand_total': grand_total,
        'razorpay_key': getattr(settings, 'RAZORPAY_KEY_ID', 'rzp_test_YOUR_KEY_HERE'),
    }
    return render(request, 'orders/checkout.html', context)


@require_POST
def place_order(request):
    """
    COD → create Order + redirect to confirmation.
    Online → create Razorpay order → return JSON for frontend.
    """
    if not request.session.get('user_id'):
        return JsonResponse({'error': 'Not logged in'}, status=401)

    customer = get_object_or_404(Customer, id=request.session['user_id'])
    cart = get_cart(request)

    if not cart:
        messages.error(request, 'Your cart is empty.')
        return redirect('/orders/cart/')

    address_id = request.POST.get('address_id')
    payment_method = request.POST.get('payment_method', 'cod')

    if not address_id:
        messages.error(request, 'Please select a delivery address.')
        return redirect('/orders/checkout/')

    address = get_object_or_404(Address, id=address_id, customer=customer)
    cart_items, subtotal, discount_amount, tax, shipping, grand_total = _build_cart_totals(request, cart)
    discount_code_str = request.session.get('discount_code', '')

    if payment_method == 'cod':
        order = _create_order(
            customer=customer, address=address, cart_items=cart_items,
            subtotal=subtotal, discount_amount=discount_amount,
            discount_code_str=discount_code_str, tax=tax, shipping=shipping,
            grand_total=grand_total, payment_method='cod', payment_id=None,
        )
        _post_order_cleanup(request, discount_code_str)
        messages.success(request, f'Order #{order.pk} placed successfully!')
        return redirect('orders:confirmation', pk=order.pk)

    elif payment_method == 'online':
        try:
            import razorpay
            rz_client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )
            razorpay_order = rz_client.order.create({
                'amount': int(grand_total * 100),
                'currency': 'INR',
                'payment_capture': 1,
            })
            # Store pending order context in session
            request.session['pending_order'] = {
                'address_id': str(address_id),
                'discount_code': discount_code_str,
                'subtotal': str(subtotal),
                'discount_amount': str(discount_amount),
                'tax': str(tax),
                'shipping': str(shipping),
                'grand_total': str(grand_total),
                'razorpay_order_id': razorpay_order['id'],
            }
            return JsonResponse({
                'razorpay_order_id': razorpay_order['id'],
                'amount': int(grand_total * 100),
                'currency': 'INR',
                'key_id': settings.RAZORPAY_KEY_ID,
            })
        except Exception as e:
            return JsonResponse({'error': f'Payment init failed: {str(e)}'}, status=500)

    messages.error(request, 'Invalid payment method.')
    return redirect('/orders/checkout/')


@require_POST
def razorpay_callback(request):
    """Verify Razorpay signature, create order, return JSON."""
    razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
    razorpay_order_id   = request.POST.get('razorpay_order_id', '')
    razorpay_signature  = request.POST.get('razorpay_signature', '')

    # Signature verification using HMAC SHA256
    secret = getattr(settings, 'RAZORPAY_KEY_SECRET', '')
    generated = hmac.new(
        secret.encode(),
        f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
        hashlib.sha256
    ).hexdigest()

    if generated != razorpay_signature:
        return JsonResponse({'success': False, 'message': 'Payment verification failed.'}, status=400)

    pending = request.session.get('pending_order', {})
    if not pending or pending.get('razorpay_order_id') != razorpay_order_id:
        return JsonResponse({'success': False, 'message': 'Invalid session. Please try again.'}, status=400)

    customer = get_object_or_404(Customer, id=request.session['user_id'])
    address  = get_object_or_404(Address, id=pending['address_id'], customer=customer)

    # Rebuild cart items for order creation
    cart = get_cart(request)
    cart_items, _, _, _, _, _ = _build_cart_totals(request, cart)
    discount_code_str = pending.get('discount_code', '')

    order = _create_order(
        customer=customer, address=address, cart_items=cart_items,
        subtotal=Decimal(pending['subtotal']),
        discount_amount=Decimal(pending['discount_amount']),
        discount_code_str=discount_code_str,
        tax=Decimal(pending['tax']),
        shipping=Decimal(pending['shipping']),
        grand_total=Decimal(pending['grand_total']),
        payment_method='online',
        payment_id=razorpay_payment_id,
    )
    _post_order_cleanup(request, discount_code_str)
    if 'pending_order' in request.session:
        del request.session['pending_order']

    return JsonResponse({'success': True, 'order_id': order.pk})


def _create_order(*, customer, address, cart_items, subtotal, discount_amount,
                  discount_code_str, tax, shipping, grand_total, payment_method, payment_id):
    """Create Order + OrderItems + reduce stock."""
    order = Order.objects.create(
        customer=customer,
        address=address,
        payment_method=payment_method,
        payment_id=payment_id,
        discount_code=discount_code_str or None,
        discount_amount=discount_amount,
        subtotal=subtotal,
        shipping=shipping,
        tax=tax,
        total=grand_total,
    )
    for item in cart_items:
        product = item['product']
        qty     = item['quantity']
        OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            product_price=product.price,
            quantity=qty,
            subtotal=item['subtotal'],
        )
        product.stock = max(0, product.stock - qty)
        product.save()
    return order


def _post_order_cleanup(request, discount_code_str):
    """Increment discount used_count, clear cart + discount from session."""
    if discount_code_str:
        DiscountCode.objects.filter(code=discount_code_str).update(
            used_count=F('used_count') + 1
        )
    request.session['cart'] = {}
    request.session['discount_code'] = ''
    request.session['discount_amount'] = 0
    request.session.modified = True


# ─── Order Views ────────────────────────────────────────────────────────────

def order_confirmation(request, pk):
    order = get_object_or_404(Order, pk=pk, customer_id=request.session.get('user_id'))
    items = order.items.select_related('product')
    return render(request, 'orders/confirmation.html', {'order': order, 'items': items})


def order_list(request):
    if request.session.get('user_role') != 'customer':
        return redirect('/accounts/login/')
    orders = Order.objects.filter(
        customer_id=request.session['user_id']
    ).prefetch_related('items').order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


def order_detail(request, pk):
    if request.session.get('user_role') != 'customer':
        return redirect('/accounts/login/')
    order = get_object_or_404(Order, pk=pk, customer_id=request.session['user_id'])
    items = order.items.select_related('product')

    # Build timeline steps
    status_steps = ['pending', 'confirmed', 'shipped', 'delivered']
    current_idx = status_steps.index(order.status) if order.status in status_steps else -1

    return render(request, 'orders/order_detail.html', {
        'order': order,
        'items': items,
        'status_steps': status_steps,
        'current_step': current_idx,
    })


# ─── Address Views ───────────────────────────────────────────────────────────

@require_POST
def add_address(request):
    if not request.session.get('user_id'):
        return redirect('/accounts/login/')

    customer  = get_object_or_404(Customer, id=request.session['user_id'])
    full_name = request.POST.get('full_name', '').strip()
    phone     = request.POST.get('phone', '').strip()
    house     = request.POST.get('house', '').strip()
    city      = request.POST.get('city', '').strip()
    state     = request.POST.get('state', '').strip()
    pincode   = request.POST.get('pincode', '').strip()
    country   = request.POST.get('country', 'India').strip()

    if not all([full_name, phone, house, city, state, pincode]):
        messages.error(request, 'All address fields are required.')
        return redirect('/orders/checkout/')

    Address.objects.create(
        customer=customer, full_name=full_name, phone=phone,
        house=house, city=city, state=state, pincode=pincode, country=country,
    )
    messages.success(request, 'Address added successfully.')
    next_url = request.POST.get('next', '/orders/checkout/')
    return redirect(next_url)


@require_POST
def delete_address(request, pk):
    if not request.session.get('user_id'):
        return redirect('/accounts/login/')
    address = get_object_or_404(Address, pk=pk, customer_id=request.session['user_id'])
    address.delete()
    messages.success(request, 'Address removed.')
    next_url = request.POST.get('next', '/orders/checkout/')
    return redirect(next_url)
