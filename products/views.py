from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Avg
from .models import Product, Category, Review, WishList, SpecialPrice
from accounts.models import Customer, Seller


# ─────────────────────────────────────────────
# EXISTING VIEWS (unchanged)
# ─────────────────────────────────────────────

def home(request):
    from dashboard.models import Banner
    from django.utils import timezone
    today = timezone.now().date()

    banners = Banner.objects.filter(is_active=True).order_by('order')
    categories = Category.objects.all()

    sale_product_ids = SpecialPrice.objects.filter(
        start_date__lte=today, end_date__gte=today
    ).values_list('product_id', flat=True)
    sale_products = Product.objects.filter(id__in=sale_product_ids).select_related('category', 'seller')[:8]

    featured_products = Product.objects.all().select_related('category', 'seller').order_by('-created_at')[:8]

    return render(request, 'products/home.html', {
        'banners': banners,
        'categories': categories,
        'sale_products': sale_products,
        'featured_products': featured_products,
    })


def shop(request):
    products = Product.objects.all().select_related('category', 'seller')
    categories = Category.objects.all()

    search_query = request.GET.get('search', '').strip()
    selected_category = request.GET.get('category', '')
    selected_category_name = ''

    if search_query:
        products = products.filter(name__icontains=search_query)

    if selected_category:
        try:
            cat = Category.objects.get(id=selected_category)
            selected_category_name = cat.name
            products = products.filter(category=cat)
        except Category.DoesNotExist:
            pass

    return render(request, 'products/shop.html', {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': selected_category,
        'selected_category_name': selected_category_name,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.select_related('customer')

    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    avg_rating = round(avg_rating, 1)

    rating_breakdown = {}
    for i in range(1, 6):
        rating_breakdown[i] = reviews.filter(rating=i).count()

    user_review = None
    in_wishlist = False
    if request.session.get('user_role') == 'customer':
        try:
            user_review = reviews.get(customer_id=request.session['user_id'])
        except Review.DoesNotExist:
            pass
        in_wishlist = WishList.objects.filter(
            customer_id=request.session['user_id'], product=product
        ).exists()

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(pk=pk)[:4]

    # Sale price check
    effective_price = product.price
    sale_active = False
    try:
        sp = product.special_price
        if sp.is_active():
            effective_price = sp.sale_price
            sale_active = True
    except Exception:
        pass

    product_images = product.images.all()

    return render(request, 'products/detail.html', {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'rating_breakdown': rating_breakdown,
        'user_review': user_review,
        'in_wishlist': in_wishlist,
        'related_products': related_products,
        'compare_list': request.session.get('compare', []),
        'product_images': product_images,
        'effective_price': effective_price,
        'sale_active': sale_active,
        'original_price': product.price,
    })


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})


# ─────────────────────────────────────────────
# WISHLIST VIEWS
# ─────────────────────────────────────────────

def add_to_wishlist(request, product_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    if request.session.get('user_role') != 'customer':
        return JsonResponse({'success': False, 'message': 'Login required'}, status=401)

    product = get_object_or_404(Product, pk=product_id)
    customer = get_object_or_404(Customer, pk=request.session['user_id'])
    obj, created = WishList.objects.get_or_create(customer=customer, product=product)

    if created:
        return JsonResponse({'success': True, 'message': 'Added to wishlist', 'in_wishlist': True})
    else:
        return JsonResponse({'success': False, 'message': 'Already in wishlist', 'in_wishlist': True})


def remove_from_wishlist(request, product_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    if request.session.get('user_role') != 'customer':
        return JsonResponse({'success': False, 'message': 'Login required'}, status=401)

    WishList.objects.filter(
        customer_id=request.session['user_id'],
        product_id=product_id
    ).delete()
    return JsonResponse({'success': True, 'message': 'Removed from wishlist', 'in_wishlist': False})


def wishlist_view(request):
    if request.session.get('user_role') != 'customer':
        return redirect('/accounts/login/')

    customer = get_object_or_404(Customer, pk=request.session['user_id'])
    wishlist_items = WishList.objects.filter(customer=customer).select_related('product', 'product__category')

    return render(request, 'products/wishlist.html', {
        'wishlist_items': wishlist_items,
    })


# ─────────────────────────────────────────────
# REVIEW VIEWS
# ─────────────────────────────────────────────

def add_review(request, product_id):
    if request.method != 'POST':
        return redirect('products:product_detail', pk=product_id)
    if request.session.get('user_role') != 'customer':
        return redirect('/accounts/login/')

    product = get_object_or_404(Product, pk=product_id)
    customer = get_object_or_404(Customer, pk=request.session['user_id'])

    try:
        rating = int(request.POST.get('rating', 0))
    except (ValueError, TypeError):
        rating = 0

    comment = request.POST.get('comment', '').strip()

    if not (1 <= rating <= 5) or not comment:
        return redirect('products:product_detail', pk=product_id)

    Review.objects.update_or_create(
        product=product,
        customer=customer,
        defaults={'rating': rating, 'comment': comment}
    )
    return redirect('products:product_detail', pk=product_id)


def delete_review(request, review_id):
    if request.method != 'POST':
        return redirect('products:shop')
    if request.session.get('user_role') != 'customer':
        return redirect('/accounts/login/')

    review = get_object_or_404(Review, pk=review_id, customer_id=request.session['user_id'])
    product_id = review.product_id
    review.delete()
    return redirect('products:product_detail', pk=product_id)


# ─────────────────────────────────────────────
# COMPARISON VIEWS
# ─────────────────────────────────────────────

def compare_add(request, product_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

    compare = request.session.get('compare', [])
    pid = str(product_id)

    if pid in compare:
        return JsonResponse({'success': False, 'message': 'Already in comparison', 'count': len(compare)})
    if len(compare) >= 3:
        return JsonResponse({'success': False, 'message': 'Max 3 products allowed', 'count': len(compare)})

    compare.append(pid)
    request.session['compare'] = compare
    return JsonResponse({'success': True, 'message': 'Added to comparison', 'count': len(compare)})


def compare_remove(request, product_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

    compare = request.session.get('compare', [])
    pid = str(product_id)
    if pid in compare:
        compare.remove(pid)
        request.session['compare'] = compare

    return JsonResponse({'success': True, 'count': len(compare)})


def compare_view(request):
    compare_ids = request.session.get('compare', [])
    products = Product.objects.filter(pk__in=compare_ids).select_related('category')

    products_with_ratings = []
    for p in products:
        avg = p.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        products_with_ratings.append({
            'product': p,
            'avg_rating': round(avg, 1),
        })

    return render(request, 'products/compare.html', {
        'products_with_ratings': products_with_ratings,
        'compare_ids': compare_ids,
    })


def compare_clear(request):
    request.session['compare'] = []
    return redirect('products:compare')
