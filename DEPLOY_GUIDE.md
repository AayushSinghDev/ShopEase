# 🚀 ShopEase — PythonAnywhere Deployment Guide
# Domain: shopease-aks.pythonanywhere.com

---

## ⏱️ Total Time: ~20 minutes

---

## 📋 STEP 1 — PythonAnywhere Account Banao

1. pythonanywhere.com → Sign Up → **Free Beginner Account**
2. Username: `shopease-aks`
3. Email confirm karo

---

## 📋 STEP 2 — Files Upload Karo

**Dashboard → Files tab → Upload**

1. Is zip file ko upload karo: `ShopEase_PythonAnywhere.zip`
2. Upload hone ke baad **Bash Console** kholo (Dashboard → New Console → Bash)
3. Console mein yeh commands run karo:

```bash
cd ~
unzip ShopEase_PythonAnywhere.zip
ls shopease_final/    # files dikhni chahiye
```

---

## 📋 STEP 3 — Virtual Environment Banao + Dependencies Install Karo

Bash console mein:

```bash
# Virtual environment banao
python3.11 -m venv ~/venv

# Activate karo
source ~/venv/bin/activate

# Dependencies install karo
pip install -r ~/shopease_final/requirements.txt
```

---

## 📋 STEP 4 — MySQL Database Setup

1. PythonAnywhere **Dashboard → Databases tab**
2. MySQL password set karo (yaad rakhna!)
3. Database name type karo: `shopease` → **Create**
4. Note karo:
   - Database name: `shopease-aks$shopease`
   - Username: `shopease-aks`
   - Host: `shopease-aks.mysql.pythonanywhere-services.com`
   - Password: jo tune set kiya

5. **`settings.py` mein update karo** (Files tab se):
   - Path: `/home/shopease-aks/shopease_final/ShopEase/settings.py`
   - `DB_PASSWORD` wali line mein apna MySQL password daalo:
   ```python
   'PASSWORD': os.environ.get('DB_PASSWORD', 'YAHAN_APNA_MYSQL_PASSWORD_DAALO'),
   ```

---

## 📋 STEP 5 — Email Setup (Gmail)

`settings.py` mein yeh 3 lines update karo:

```python
EMAIL_HOST_USER     = 'tumhara-email@gmail.com'
EMAIL_HOST_PASSWORD = 'xxxx xxxx xxxx xxxx'   # 16-char App Password
DEFAULT_FROM_EMAIL  = 'ShopEase <tumhara-email@gmail.com>'
```

**Gmail App Password kaise banate hain:**
1. myaccount.google.com → Security
2. 2-Step Verification → ON karo
3. "App Passwords" search karo
4. Select App: Mail → Device: Other → Name: ShopEase → Generate
5. 16-char password copy karo

---

## 📋 STEP 6 — Web App Configure Karo

1. Dashboard → **Web tab** → Add a new web app
2. **Manual Configuration** select karo (Django nahi)
3. Python version: **Python 3.11**
4. Click Next

### WSGI File Set Karo:
- Web tab mein **WSGI configuration file** link pe click karo
- Poora content delete karo
- Yeh paste karo:

```python
import os
import sys

path = '/home/shopease-aks/shopease_final'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'ShopEase.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

- Save karo

### Virtual Environment Set Karo:
- Web tab → **Virtualenv** section
- Path daalo: `/home/shopease-aks/venv`
- Tick/confirm karo

### Static Files Set Karo:
- Web tab → **Static files** section → mein yeh 2 entries add karo:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/shopease-aks/shopease_final/staticfiles` |
| `/media/` | `/home/shopease-aks/shopease_final/media` |

---

## 📋 STEP 7 — Migrate + Sample Data

Bash console mein (venv active karke):

```bash
source ~/venv/bin/activate
cd ~/shopease_final

# Database tables banao
python manage.py migrate

# Static files collect karo
python manage.py collectstatic --noinput

# Sample data load karo (admin, sellers, customers, products)
python manage.py create_sample_data
```

---

## 📋 STEP 8 — Reload aur Test Karo

1. **Web tab → Reload** button dabao (green button)
2. Browser mein jao: `https://shopease-aks.pythonanywhere.com`

---

## ✅ Test Login Credentials

| Role     | Email                        | Password     |
|----------|------------------------------|--------------|
| Admin    | admin@shopease.com           | admin123     |
| Seller   | techstore@shopease.com       | seller123    |
| Customer | rahul@example.com            | customer123  |

**Discount Codes:** `WELCOME10` (10% off), `FLAT100` (₹100 flat)

---

## ⚠️ 3 Cheezein Jo Baad Mein Dalni Hain (Optional)

### 1. Razorpay Keys (Payment ke liye)
- razorpay.com → Free account → Settings → API Keys → Test Keys copy karo
- `settings.py` mein update karo:
```python
RAZORPAY_KEY_ID     = 'rzp_test_...'
RAZORPAY_KEY_SECRET = '...'
```

### 2. Anthropic Key (AI Chatbot ke liye)
- console.anthropic.com → API Keys → Create
- `settings.py` mein:
```python
ANTHROPIC_API_KEY = 'sk-ant-...'
```

### 3. Custom Domain (Optional, baad mein)
- PythonAnywhere paid plan pe custom domain milti hai
- Free plan mein: `shopease-aks.pythonanywhere.com`

---

## 🔧 Agar Koi Error Aaye

**500 Error:**
- Web tab → **Error log** dekho
- Usually settings.py mein koi typo hota hai

**Static files nahi aa rahe (CSS broken):**
```bash
source ~/venv/bin/activate
cd ~/shopease_final
python manage.py collectstatic --noinput
```
Phir Web tab → Reload

**Database error:**
- settings.py mein DB_PASSWORD sahi hai?
- Database tab mein database create kiya?

**Email nahi ja raha:**
- Gmail App Password 16 characters ka hona chahiye (spaces ke saath)
- 2FA Gmail pe ON hona chahiye
- `settings.py` mein EMAIL_HOST_USER aur EMAIL_HOST_PASSWORD dono check karo

---

## 📁 Final File Structure on PythonAnywhere

```
/home/shopease-aks/
├── venv/                    ← virtual environment
└── shopease_final/          ← project
    ├── ShopEase/
    │   ├── settings.py      ← ✏️ tumne edit kiya
    │   ├── urls.py
    │   └── wsgi.py
    ├── accounts/
    ├── products/
    ├── orders/
    ├── discounts/
    ├── dashboard/
    ├── chatbot/
    ├── templates/
    ├── static/
    ├── staticfiles/         ← collectstatic ke baad banta hai
    ├── media/               ← uploaded images
    └── manage.py
```
