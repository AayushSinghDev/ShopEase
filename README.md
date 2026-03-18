# 🛒 ShopEase — Full-Stack E-Commerce Web App

![Python](https://img.shields.io/badge/Python-3.13.2-blue?logo=python)
![Django](https://img.shields.io/badge/Django-6.0.1-green?logo=django)
![MySQL](https://img.shields.io/badge/Database-MySQL%208.x-orange?logo=mysql)
![Bootstrap](https://img.shields.io/badge/UI-Bootstrap%205.3-purple?logo=bootstrap)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

> A full-stack e-commerce platform built with Django, featuring multi-role authentication, product management, order processing, discount codes, and an AI chatbot — developed as an MCA Semester IV project at Ahmedabad Institute of Technology (GTU Affiliated).

**🔗 Live Demo:** [https://aks000.pythonanywhere.com](https://aks000.pythonanywhere.com)  
**📁 GitHub:** [https://github.com/AayushSinghDev/ShopEase](https://github.com/AayushSinghDev/ShopEase)

---

## 👨‍💻 Project Info

| Field       | Details                                   |
| ----------- | ----------------------------------------- |
| **College** | Ahmedabad Institute of Technology (AIT)   |
| **Course**  | MCA Semester IV — GTU Affiliated          |
| **Guide**   | Asst. Prof. Niki Patel                    |
| **Team**    | Singh Aayush Vedpraksh (245850694048)     |
|             | Vegada Sangita Babubhai (245850694052)    |
|             | Chauhan Bhumika Kishorbhai (245850694004) |

---

## 🎯 Features

### ✅ Completed

- **3-Role Authentication** — Customer, Seller, Super Admin with tab-based login/register UI
- **Session-based Auth** — Secure login using SHA-256 password hashing + CSRF protection
- **Home Page** — Hero banner, stats counter, category grid, featured products
- **Shop Page** — Product listing with search and category filter
- **Product Detail** — Image, price, quantity selector, Add to Cart
- **Session Cart** — Add, remove, increase/decrease quantity, clear cart
- **Discount Codes** — Percentage & flat discounts with expiry date and usage limits
- **Pricing Engine** — Real-time subtotal + 5% GST + free shipping on orders above ₹499
- **Checkout** — Address form, saved addresses, Cash on Delivery (COD)
- **Order Confirmation** — Order timeline, items list, address summary, grand total
- **My Orders** — Filter by status, order table with status badges
- **Seller Dashboard** — Stats for products, orders, and total earnings
- **Seller Products** — List, add, edit, delete with image upload
- **Seller Orders** — View and update order status
- **Seller Discounts** — Create, toggle, and delete discount codes
- **Admin Dashboard** — Platform-wide stats overview
- **Admin: Manage Sellers** — Approve or delete sellers
- **Admin: Manage Customers** — View or delete customers
- **Admin: Manage Products** — View or delete products
- **Admin: Manage Orders** — View and update order status
- **Responsive UI** — Bootstrap 5.3 with Navy Blue (`#0d1b3e`) + Orange (`#f5a623`) theme
- **Security** — Django ORM (SQL injection prevention) + CSRF tokens on all forms

### 🔄 Planned / In Progress

- Face Recognition Login (OpenCV + dlib)
- AI Chatbot (Claude API Integration)
- Payment Gateway (Razorpay)
- Real-time Notifications
- Cloud Deployment Enhancements

---

## 🛠️ Tech Stack

| Layer              | Technology                             |
| ------------------ | -------------------------------------- |
| **Backend**        | Python 3.13.2, Django 6.0.1            |
| **Database**       | MySQL 8.x (local), SQLite (server)     |
| **Frontend**       | HTML5, CSS3, JavaScript, Bootstrap 5.3 |
| **Image Handling** | Pillow 11.3.0                          |
| **DB Connector**   | mysqlclient                            |
| **Icons**          | Bootstrap Icons                        |
| **Deployment**     | PythonAnywhere                         |

---

## 📁 Project Structure

```
ShopEase/
├── manage.py
├── requirements.txt
├── ShopEase/                    # Django project config
│   ├── settings.py              # Points to settings_local (default)
│   ├── settings_local.py        # Local dev (MySQL)
│   ├── settings_production.py   # PythonAnywhere (SQLite)
│   └── urls.py
├── accounts/                    # Auth: Customer, Seller, SuperAdmin
│   ├── models.py
│   ├── views.py                 # Login / Register
│   ├── seller_views.py          # Seller panel views
│   ├── admin_views.py           # Admin management views
│   └── urls.py
├── products/                    # Products, Categories
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── orders/                      # Cart, Checkout, Orders, Addresses
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── discounts/                   # Discount Codes
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── templates/                   # All HTML templates
│   ├── base.html
│   ├── accounts/
│   ├── products/
│   ├── orders/
│   ├── seller/
│   └── admin_panel/
├── static/                      # CSS, JS, Images
└── media/                       # Uploaded product/category images
```

---

## 🚀 Local Setup (Localhost)

### Prerequisites

- Python 3.10+
- MySQL / XAMPP
- pip

### Step 1 — Clone the Repository

```bash
git clone https://github.com/AayushSinghDev/ShopEase.git
cd ShopEase
```

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — MySQL Database Setup

Open MySQL / XAMPP and run:

```sql
CREATE DATABASE shopease_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Step 4 — Configure MySQL Password

Open `ShopEase/settings_local.py` and set your MySQL root password:

```python
'PASSWORD': 'your_mysql_password',   # line ~30
```

### Step 5 — Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6 — Create Django Superuser (for `/admin/` panel)

```bash
python manage.py createsuperuser
# Username: shopAdmin
# Password: shop1234
```

### Step 7 — Create SuperAdmin (for ShopEase admin panel)

```bash
python manage.py shell
```

```python
from accounts.models import SuperAdmin
from django.contrib.auth.hashers import make_password

SuperAdmin.objects.create(
    username='admin',
    email='admin@shopease.com',
    password=make_password('admin123')
)
exit()
```

### Step 8 — Add Sample Categories

```bash
python manage.py shell
```

```python
from products.models import Category
for name in ['Bikes', 'Electronics', 'Clothing', 'Mobile Phones', 'Home & Kitchen']:
    Category.objects.create(name=name)
exit()
```

### Step 9 — Run Server

```bash
python manage.py runserver
```

Open: **http://127.0.0.1:8000**

---

## 🔑 Login Credentials

| Role         | Email                              | Password |
| ------------ | ---------------------------------- | -------- |
| Super Admin  | admin@shopease.com                 | admin123 |
| Seller       | aayushsingh.9291@gmail.com         | ayush123 |
| Django Admin | shopAdmin _(username)_             | shop1234 |
| Customer     | Register via `/accounts/register/` | —        |

---

## 🌐 URL Reference

| URL                             | Page                                     |
| ------------------------------- | ---------------------------------------- |
| `/`                             | Home (hero + categories + products)      |
| `/accounts/login/`              | Login (3-tab: Customer / Seller / Admin) |
| `/accounts/register/`           | Register (Customer or Seller)            |
| `/accounts/logout/`             | Logout                                   |
| `/accounts/dashboard/admin/`    | Admin Dashboard                          |
| `/accounts/dashboard/seller/`   | Seller Dashboard                         |
| `/accounts/dashboard/customer/` | Customer Dashboard                       |
| `/products/`                    | Shop page (search + filter)              |
| `/products/detail/<id>/`        | Product Detail                           |
| `/cart/`                        | Cart                                     |
| `/cart/add/<id>/`               | Add to Cart                              |
| `/cart/remove/<id>/`            | Remove from Cart                         |
| `/orders/checkout/`             | Checkout                                 |
| `/orders/confirmation/`         | Order Confirmation                       |
| `/orders/my-orders/`            | My Orders                                |
| `/seller/dashboard/`            | Seller Full Dashboard                    |
| `/seller/products/`             | Seller Products List                     |
| `/seller/product/add/`          | Add Product                              |
| `/seller/product/edit/<id>/`    | Edit Product                             |
| `/seller/orders/`               | Seller Orders                            |
| `/seller/discounts/`            | Discount Code Manager                    |
| `/admin-panel/sellers/`         | Admin: Manage Sellers                    |
| `/admin-panel/customers/`       | Admin: Manage Customers                  |
| `/admin-panel/products/`        | Admin: Manage Products                   |
| `/admin-panel/orders/`          | Admin: Manage Orders                     |
| `/discount/apply/`              | Apply Discount Code                      |
| `/admin/`                       | Django Admin Panel                       |

---

## ⚙️ Optional Features Configuration

### Email Notifications

Edit `ShopEase/settings_local.py`:

```python
EMAIL_HOST_USER = 'your-gmail@gmail.com'
EMAIL_HOST_PASSWORD = 'your-16-char-app-password'
```

> Get App Password: Google Account → Security → 2-Step Verification → App Passwords

### AI Chatbot (Claude API)

```python
ANTHROPIC_API_KEY = 'sk-ant-api03-your-key'
```

> Get key at: [https://console.anthropic.com](https://console.anthropic.com)

### Razorpay Payments

```python
RAZORPAY_KEY_ID = 'rzp_test_your_key'
RAZORPAY_KEY_SECRET = 'your_secret'
```

> Get keys at: [https://dashboard.razorpay.com](https://dashboard.razorpay.com)

---

## 🌐 PythonAnywhere Deployment

```bash
# In PythonAnywhere Bash console:
source ~/venv/bin/activate
cd ~/ShopEase
git pull origin main
python manage.py migrate
python manage.py collectstatic --noinput
# Web tab → Reload
```

**WSGI Config** (`/var/www/aks000_pythonanywhere_com_wsgi.py`):

```python
import sys, os
sys.path.insert(0, '/home/aks000/ShopEase')
os.environ['DJANGO_SETTINGS_MODULE'] = 'ShopEase.settings_production'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

---

## 🐛 Known Bugs Fixed

| #   | Bug                                                        | Fix                                                                      |
| --- | ---------------------------------------------------------- | ------------------------------------------------------------------------ |
| 1   | `TemplateSyntaxError` — Prettier broke Django `{% %}` tags | Add `.vscode/settings.json` to disable `formatOnSave` for HTML           |
| 2   | Seller login failing (wrong password)                      | Double hashing during register — reset via shell with `make_password()`  |
| 3   | `TypeError: Decimal * int` in cart                         | Wrap price with `float()`: `float(product.price) * qty`                  |
| 4   | Login email field not retained on failed login             | Fixed in latest version                                                  |
| 5   | Register form data cleared on password mismatch            | Fixed — form data now retained                                           |
| 6   | Cart URL namespace conflict                                | Removed duplicate `orders.urls` include, removed `app_name`              |
| 7   | Admin login: "No admin found" with correct credentials     | `SuperAdmin` was created without hashed password — use `make_password()` |
| 8   | `address_id` reference error at checkout                   | Added `name` and `phone` fields to `Address` model + re-migrated         |

---

## 💡 VS Code Tip

To prevent Prettier from breaking Django template syntax, add this to `.vscode/settings.json`:

```json
{
  "[html]": {
    "editor.formatOnSave": false
  },
  "[django-html]": {
    "editor.formatOnSave": false
  }
}
```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

<p align="center">Made with ❤️ by Team ShopEase — AIT, Ahmedabad</p>
