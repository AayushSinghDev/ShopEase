# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth.hashers import check_password
# from .models import Customer, Seller, SuperAdmin
# from django.contrib.auth.hashers import check_password, make_password


# def home(request):
#     return redirect('accounts:login')


# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         role = request.POST.get('role')

#         if role == 'customer':
#             try:
#                 user = Customer.objects.get(email=email)
#                 if check_password(password, user.password):
#                     request.session['user_id'] = user.id
#                     request.session['user_role'] = 'customer'
#                     request.session['user_name'] = user.name
#                     return redirect('accounts:customer_dashboard')
#                 else:
#                     messages.error(request, 'Invalid password.')
#             except Customer.DoesNotExist:
#                 messages.error(request, 'No customer account found with this email.')

#         elif role == 'seller':
#             try:
#                 user = Seller.objects.get(email=email)
#                 if check_password(password, user.password):
#                     if not user.is_approved:
#                         messages.warning(request, 'Your seller account is pending admin approval.')
#                         return redirect('accounts:login')
#                     request.session['user_id'] = user.id
#                     request.session['user_role'] = 'seller'
#                     request.session['user_name'] = user.name
#                     return redirect('accounts:seller_dashboard')
#                 else:
#                     messages.error(request, 'Invalid password.')
#             except Seller.DoesNotExist:
#                 messages.error(request, 'No seller account found with this email.')

#         elif role == 'admin':
#             try:
#                 user = SuperAdmin.objects.get(email=email)
#                 if check_password(password, user.password):
#                     request.session['user_id'] = user.id
#                     request.session['user_role'] = 'admin'
#                     request.session['user_name'] = user.username
#                     return redirect('accounts:admin_dashboard')
#                 else:
#                     messages.error(request, 'Invalid password.')
#             except SuperAdmin.DoesNotExist:
#                 messages.error(request, 'No admin account found with this email.')

#     return render(request, 'accounts/login.html')


# def register_view(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')
#         role = request.POST.get('role')

#         if password != confirm_password:
#             messages.error(request, 'Passwords do not match.')
#             return redirect('accounts:register')

#         if role == 'customer':
#             if Customer.objects.filter(email=email).exists():
#                 messages.error(request, 'A customer with this email already exists.')
#                 return redirect('accounts:register')
#             Customer.objects.create(name=name, email=email, password=make_password(password), phone=phone)
#             messages.success(request, 'Customer account created! Please login.')
#             return redirect('accounts:login')

#         elif role == 'seller':
#             if Seller.objects.filter(email=email).exists():
#                 messages.error(request, 'A seller with this email already exists.')
#                 return redirect('accounts:register')
#             Seller.objects.create(name=name, email=email, password=make_password(password), phone=phone)
#             messages.success(request, 'Seller account created! Awaiting admin approval.')
#             return redirect('accounts:login')

#     return render(request, 'accounts/register.html')


# def logout_view(request):
#     request.session.flush()
#     messages.success(request, 'Logged out successfully.')
#     return redirect('accounts:login')


# def customer_dashboard(request):
#     if request.session.get('user_role') != 'customer':
#         return redirect('accounts:login')
#     return render(request, 'accounts/customer_dashboard.html', {'name': request.session.get('user_name')})


# def seller_dashboard(request):
#     if request.session.get('user_role') != 'seller':
#         return redirect('accounts:login')
#     return render(request, 'accounts/seller_dashboard.html', {'name': request.session.get('user_name')})


# def admin_dashboard(request):
#     if request.session.get('user_role') != 'admin':
#         return redirect('accounts:login')
#     return render(request, 'accounts/admin_dashboard.html', {'name': request.session.get('user_name')})



from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from .models import Customer, Seller, SuperAdmin
from django.contrib.auth.hashers import check_password, make_password


def home(request):
    return redirect('accounts:login')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if role == 'customer':
            try:
                user = Customer.objects.get(email=email)
                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    request.session['user_role'] = 'customer'
                    request.session['user_name'] = user.name
                    return redirect('accounts:customer_dashboard')
                else:
                    messages.error(request, 'Invalid password.')
            except Customer.DoesNotExist:
                messages.error(request, 'No customer account found with this email.')

        elif role == 'seller':
            try:
                user = Seller.objects.get(email=email)
                if check_password(password, user.password):
                    if not user.is_approved:
                        messages.warning(request, 'Your seller account is pending admin approval.')
                        return redirect('accounts:login')
                    request.session['user_id'] = user.id
                    request.session['user_role'] = 'seller'
                    request.session['user_name'] = user.name
                    return redirect('accounts:seller_dashboard')
                else:
                    messages.error(request, 'Invalid password.')
            except Seller.DoesNotExist:
                messages.error(request, 'No seller account found with this email.')

        elif role == 'admin':
            try:
                user = SuperAdmin.objects.get(email=email)
                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    request.session['user_role'] = 'admin'
                    request.session['user_name'] = user.username
                    return redirect('accounts:admin_dashboard')
                else:
                    messages.error(request, 'Invalid password.')
            except SuperAdmin.DoesNotExist:
                messages.error(request, 'No admin account found with this email.')

    return render(request, 'accounts/login.html')


def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('accounts:register')

        if role == 'customer':
            if Customer.objects.filter(email=email).exists():
                messages.error(request, 'A customer with this email already exists.')
                return redirect('accounts:register')
            Customer.objects.create(
                name=name, email=email,
                password=make_password(password), phone=phone
            )
            messages.success(request, 'Customer account created! Please login.')
            return redirect('accounts:login')

        elif role == 'seller':
            if Seller.objects.filter(email=email).exists():
                messages.error(request, 'A seller with this email already exists.')
                return redirect('accounts:register')
            Seller.objects.create(
                name=name, email=email,
                password=make_password(password), phone=phone
            )
            messages.success(request, 'Seller account created! Awaiting admin approval.')
            return redirect('accounts:login')

    return render(request, 'accounts/register.html')


def logout_view(request):
    request.session.flush()
    messages.success(request, 'Logged out successfully.')
    return redirect('accounts:login')


def customer_dashboard(request):
    if request.session.get('user_role') != 'customer':
        return redirect('accounts:login')
    return render(request, 'accounts/customer_dashboard.html', {
        'name': request.session.get('user_name')
    })


def seller_dashboard(request):
    if request.session.get('user_role') != 'seller':
        return redirect('accounts:login')
    return render(request, 'accounts/seller_dashboard.html', {
        'name': request.session.get('user_name')
    })


def admin_dashboard(request):
    if request.session.get('user_role') != 'admin':
        return redirect('accounts:login')

    from products.models import Product, Category
    from orders.models import Order

    context = {
        'name': request.session.get('user_name'),
        'total_customers': Customer.objects.count(),
        'total_sellers': Seller.objects.count(),
        'total_products': Product.objects.count(),
        'total_orders': Order.objects.count(),
        'total_categories': Category.objects.count(),
        'pending_sellers': Seller.objects.filter(is_approved=False).count(),
        'all_customers': Customer.objects.all(),
        'all_sellers': Seller.objects.all(),
    }
    return render(request, 'accounts/admin_dashboard.html', context)