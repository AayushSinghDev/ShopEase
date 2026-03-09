from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Customer, Seller, SuperAdmin


# ─── Existing Auth Views ────────────────────────────────────────────────────

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
            user = Customer.objects.create(
                name=name, email=email,
                password=make_password(password), phone=phone
            )
            # Store new user info in session for optional face registration
            request.session['new_user_id'] = user.id
            request.session['new_user_role'] = 'customer'
            messages.success(request, 'Customer account created! Please login.')
            return redirect('accounts:login')

        elif role == 'seller':
            if Seller.objects.filter(email=email).exists():
                messages.error(request, 'A seller with this email already exists.')
                return redirect('accounts:register')
            user = Seller.objects.create(
                name=name, email=email,
                password=make_password(password), phone=phone
            )
            # Store new user info in session for optional face registration
            request.session['new_user_id'] = user.id
            request.session['new_user_role'] = 'seller'
            messages.success(request, 'Seller account created! Awaiting admin approval.')
            return redirect('accounts:login')

    return render(request, 'accounts/register.html')


def logout_view(request):
    request.session.flush()
    messages.success(request, 'Logged out successfully.')
    return redirect('accounts:login')


def my_account(request):
    if request.session.get('user_role') != 'customer':
        return redirect('accounts:login')

    customer = Customer.objects.get(id=request.session['user_id'])

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_profile':
            name = request.POST.get('name', '').strip()
            phone = request.POST.get('phone', '').strip()
            if name:
                customer.name = name
                customer.phone = phone
                customer.save()
                request.session['user_name'] = name
                messages.success(request, 'Profile updated successfully!')
            else:
                messages.error(request, 'Name cannot be empty.')

        elif action == 'change_password':
            current = request.POST.get('current_password', '')
            new_pass = request.POST.get('new_password', '')
            confirm = request.POST.get('confirm_password', '')

            if not check_password(current, customer.password):
                messages.error(request, 'Current password is incorrect.')
            elif new_pass != confirm:
                messages.error(request, 'New passwords do not match.')
            elif len(new_pass) < 6:
                messages.error(request, 'Password must be at least 6 characters.')
            else:
                customer.password = make_password(new_pass)
                customer.save()
                messages.success(request, 'Password changed successfully!')

        return redirect('/accounts/my-account/')

    from orders.models import Order, Address
    from products.models import WishList

    addresses = Address.objects.filter(customer=customer).order_by('-is_default', '-id')
    total_orders = Order.objects.filter(customer=customer).count()
    delivered = Order.objects.filter(customer=customer, status='delivered').count()
    wishlist_count = WishList.objects.filter(customer=customer).count()

    return render(request, 'accounts/my_account.html', {
        'customer': customer,
        'addresses': addresses,
        'total_orders': total_orders,
        'delivered': delivered,
        'wishlist_count': wishlist_count,
    })


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
    # Redirect to the full Super Admin Panel (dashboard app)
    return redirect('/superadmin/')


# ─── Facial Recognition Views ───────────────────────────────────────────────

@require_POST
def face_register(request):
    """
    POST /accounts/face-register/
    Captures 30 face images via webcam, trains the LBPH model, and
    saves the face_data path to the Customer or Seller record.
    Only works when ENABLE_FACE_RECOGNITION=True in settings.
    """
    from django.conf import settings as django_settings
    if not getattr(django_settings, 'ENABLE_FACE_RECOGNITION', False):
        return JsonResponse({
            'success': False,
            'message': 'Face recognition is disabled on this server. Please use password login.'
        }, status=503)

    try:
        from . import face_utils

        role = request.POST.get('role') or request.session.get('new_user_role')
        user_id = request.POST.get('user_id') or request.session.get('new_user_id')

        if not role or not user_id:
            return JsonResponse({
                'success': False,
                'message': 'Role and user_id are required. Please register your account first.'
            }, status=400)

        if role not in ('customer', 'seller'):
            return JsonResponse({
                'success': False,
                'message': 'Face login is only available for Customer and Seller accounts.'
            }, status=400)

        user_id = int(user_id)

        # Step 1: Capture face images from webcam (server-side OpenCV)
        folder_path = face_utils.capture_face_images(user_id, role)

        # Step 2: Train/update LBPH model for this role
        face_utils.train_face_model(role)

        # Step 3: Save face_data path to user record
        if role == 'customer':
            Customer.objects.filter(id=user_id).update(face_data=folder_path)
        elif role == 'seller':
            Seller.objects.filter(id=user_id).update(face_data=folder_path)

        return JsonResponse({
            'success': True,
            'message': 'Face registered successfully! You can now use Face Login.'
        })

    except RuntimeError as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'An unexpected error occurred: {str(e)}'
        }, status=500)


@require_POST
def face_login(request):
    """
    POST /accounts/face-login/
    Opens webcam, detects & recognizes the face using trained LBPH model.
    Only works when ENABLE_FACE_RECOGNITION=True in settings.
    """
    from django.conf import settings as django_settings
    if not getattr(django_settings, 'ENABLE_FACE_RECOGNITION', False):
        return JsonResponse({
            'success': False,
            'message': 'Face recognition is disabled on this server. Please use password login.'
        }, status=503)

    try:
        from . import face_utils

        role = request.POST.get('role')

        if not role:
            return JsonResponse({
                'success': False,
                'message': 'Please select your role (Customer or Seller) before using Face Login.'
            }, status=400)

        if role not in ('customer', 'seller'):
            return JsonResponse({
                'success': False,
                'message': 'Face login is only available for Customer and Seller accounts.'
            }, status=400)

        # Attempt face recognition
        user_id = face_utils.recognize_face(role)

        if user_id is None:
            return JsonResponse({
                'success': False,
                'message': 'Face not recognized. Please ensure good lighting and try again, or use password login.'
            })

        # Fetch user from DB and verify they exist
        if role == 'customer':
            try:
                user = Customer.objects.get(id=user_id)
            except Customer.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Recognized face does not match any active account.'
                })
            request.session['user_id'] = user.id
            request.session['user_role'] = 'customer'
            request.session['user_name'] = user.name
            redirect_url = '/accounts/dashboard/customer/'

        elif role == 'seller':
            try:
                user = Seller.objects.get(id=user_id)
            except Seller.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Recognized face does not match any active account.'
                })
            if not user.is_approved:
                return JsonResponse({
                    'success': False,
                    'message': 'Your seller account is pending admin approval.'
                })
            request.session['user_id'] = user.id
            request.session['user_role'] = 'seller'
            request.session['user_name'] = user.name
            redirect_url = '/accounts/dashboard/seller/'

        return JsonResponse({
            'success': True,
            'message': f'Welcome back, {user.name}!',
            'redirect_url': redirect_url
        })

    except RuntimeError as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'An unexpected error occurred: {str(e)}'
        }, status=500)
