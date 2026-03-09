# 🛒 ShopEase — Full-Stack E-Commerce Web App

**Live URL:** https://aks000.pythonanywhere.com  
**GitHub:** https://github.com/AayushSinghDev/ShopEase  
**Tech Stack:** Django (Python 3.11) + HTML/CSS/JS + MySQL (local) / SQLite (server)

---

## 🚀 Quick Start — Local Setup (Localhost)

### Step 1 — MySQL Database Setup
Open MySQL / XAMPP and run:
```sql
CREATE DATABASE shopease_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Step 2 — Edit MySQL Password
Open `ShopEase/settings_local.py` and set your MySQL password:
```python
'PASSWORD': 'your_mysql_password',   # line 30
```

### Step 3 — Install Dependencies
```bash
cd ShopEase
pip install -r requirements.txt
```

### Step 4 — Run Migrations
```bash
python manage.py migrate
```

### Step 5 — Create Sample Data
```bash
python manage.py create_sample_data
```

### Step 6 — Run Server
```bash
python manage.py runserver
```

Open: **http://127.0.0.1:8000**

---

## 🔑 Login Credentials

| Role | Email | Password |
|------|-------|----------|
| Super Admin | admin@shopease.com | admin123 |
| Seller 1 | techstore@shopease.com | seller123 |
| Seller 2 | fashionhub@shopease.com | seller123 |
| Customer | rahul@example.com | customer123 |

---

## ⚙️ Configure Features (Optional)

### Email Notifications
Edit `ShopEase/settings_local.py`:
```python
EMAIL_HOST_USER = 'your-gmail@gmail.com'
EMAIL_HOST_PASSWORD = 'your-16-char-app-password'  # Gmail App Password
```
Get App Password: myaccount.google.com → Security → 2-Step Verification → App Passwords

### AI Chatbot
Edit `ShopEase/settings_local.py`:
```python
ANTHROPIC_API_KEY = 'sk-ant-api03-your-key'
```
Get key: https://console.anthropic.com ($5 free credits)

### Razorpay Payments
Edit `ShopEase/settings_local.py`:
```python
RAZORPAY_KEY_ID = 'rzp_test_your_key'
RAZORPAY_KEY_SECRET = 'your_secret'
```
Get keys: https://dashboard.razorpay.com

---

## 🌐 PythonAnywhere Deployment (Live Server)

```bash
# In PythonAnywhere Bash console:
source ~/venv/bin/activate
cd ~/ShopEase
git pull origin main
python manage.py migrate
python manage.py create_sample_data
python manage.py collectstatic --noinput
# Then: Web tab → Reload
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

## 📁 Project Structure

```
ShopEase/
├── ShopEase/           # Django project config
│   ├── settings.py         # Points to settings_local (default)
│   ├── settings_local.py   # Local dev (MySQL)
│   ├── settings_production.py  # PythonAnywhere (SQLite)
│   └── urls.py
├── accounts/           # Auth: Customer, Seller, SuperAdmin + Face Login
├── products/           # Products, Categories, Reviews, Wishlist
├── orders/             # Cart, Checkout, Orders, Addresses
├── discounts/          # Discount Codes
├── dashboard/          # Super Admin Panel
├── chatbot/            # AI Chatbot (Claude API)
├── templates/          # All HTML templates
├── static/             # CSS, JS, Images
└── manage.py
```

---

## 🛠️ Bugs Fixed (This Version)

- ✅ Login: Email field now retained after failed login
- ✅ Registration: Form data retained on password mismatch / email exists error
- ✅ Role selector: Correct role highlighted on error
- ✅ Separate settings for local (MySQL) and production (SQLite)

