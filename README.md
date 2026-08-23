# Secure Login & File Access System

## Overview

This project implements a secure authentication and file-access system using
two separate approaches:

1. **Custom Django REST Framework Backend**
   - JWT authentication
   - User registration and login
   - Logout with refresh-token blacklisting
   - Login rate limiting
   - User-specific file access

2. **Appwrite Implementation**
   - Appwrite Authentication
   - Appwrite Sessions
   - Appwrite Database
   - Appwrite Storage
   - Appwrite Permissions

The frontend test client allows both implementations to be tested.

---

# Project Structure

```text
secure_login/
│
├── README.md
├── .gitignore
│
├── custom-backend/
│   ├── accounts/
│   ├── files/
│   ├── config/
│   ├── manage.py
│   ├── requirements.txt
│   └── .env.example
│
├── appwrite-backend/
│   └── README.md
│
├── frontend/
│   ├── index.html
│   └── appwrite-adapter.js
│
└── postman/