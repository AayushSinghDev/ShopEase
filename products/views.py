# from django.shortcuts import render
# from .models import Product, Category


# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'products/product_list.html', {'products': products})


# def product_detail(request, pk):
#     product = Product.objects.get(pk=pk)
#     return render(request, 'products/product_detail.html', {'product': product})


# def add_product(request):
#     return render(request, 'products/add_product.html')


# def category_list(request):
#     categories = Category.objects.all()
#     return render(request, 'products/category_list.html', {'categories': categories})


from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from accounts.models import Customer, Seller


def home(request):
    products = Product.objects.all().select_related('category', 'seller')[:8]
    categories = Category.objects.all()
    total_products = Product.objects.count()
    total_sellers = Seller.objects.filter(is_approved=True).count()
    total_customers = Customer.objects.count()

    return render(request, 'products/home.html', {
        'products': products,
        'categories': categories,
        'total_products': total_products,
        'total_sellers': total_sellers,
        'total_customers': total_customers,
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
    return render(request, 'products/detail.html', {'product': product})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})