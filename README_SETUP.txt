===========================================
  ShopEase — Final Project Setup Guide
===========================================

STEP 1 — MySQL Database banao
------------------------------
MySQL Workbench ya Command Line mein:
  CREATE DATABASE shopease_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

STEP 2 — settings.py update karo
----------------------------------
File: ShopEase/settings.py

  DATABASES → USER, PASSWORD apna MySQL username/password daalo
  RAZORPAY_KEY_ID     = 'rzp_test_...'     (razorpay.com se)
  RAZORPAY_KEY_SECRET = '...'
  ANTHROPIC_API_KEY   = 'sk-ant-...'       (console.anthropic.com se)
  EMAIL_HOST_USER     = 'tera@gmail.com'
  EMAIL_HOST_PASSWORD = 'xxxx xxxx xxxx'   (Gmail App Password)

STEP 3 — Dependencies install karo
------------------------------------
  pip install -r requirements.txt

STEP 4 — Migrations run karo
------------------------------
  python manage.py migrate

STEP 5 — Sample data load karo (optional)
------------------------------------------
  python manage.py create_sample_data

STEP 6 — Server chalao
------------------------
  python manage.py runserver

===========================================
  Test Login Credentials (after Step 5)
===========================================
  Admin:    admin@shopease.com    / admin123
  Seller:   techstore@shopease.com / seller123
  Customer: rahul@example.com     / customer123

===========================================
  Important URLs
===========================================
  Home:        http://127.0.0.1:8000/
  Login:       http://127.0.0.1:8000/accounts/login/
  SuperAdmin:  http://127.0.0.1:8000/superadmin/
  Seller:      http://127.0.0.1:8000/seller/dashboard/

===========================================
  Modules Included
===========================================
  Module 1  — Facial Recognition Login
  Module 2  — Super Admin Panel
  Module 3  — Checkout + Razorpay
  Module 4  — Wishlist + Reviews + Compare
  Module 5  — AI Chatbot (Claude API)
  Module 6  — My Account + Addresses
  Module 7  — Banners + Images + Sale Price
  Module 8  — Email + PDF Invoice + Stock Alerts + CSV Export
