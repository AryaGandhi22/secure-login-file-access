
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
````

---

# 1. Custom Django Backend Setup

## Requirements

* Python 3.10+
* PostgreSQL
* pip

## Step 1 — Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd secure_login
```

## Step 2 — Open the Custom Backend

```bash
cd custom-backend
```

## Step 3 — Create a virtual environment

```bash
python -m venv venv
```

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### Windows CMD

```cmd
venv\Scripts\activate
```

## Step 4 — Install dependencies

```bash
pip install -r requirements.txt
```

## Step 5 — Configure environment variables

A template is provided:

```text
custom-backend/.env.example
```

Create your local `.env` file.

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

Open `.env` and configure:

```env
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database>
DJANGO_SECRET_KEY=<your-secret-key>
```

The `.env` file contains sensitive configuration and is excluded from Git
using `.gitignore`.

**Never commit `.env`, database credentials, API keys, or other secrets.**

## Step 6 — Apply database migrations

```bash
python manage.py migrate
```

## Step 7 — Create the demo users and files

The project includes a Django management command that creates three demo
users and a sample file for each user.

```bash
python manage.py seed_demo_data
```

This creates:

| Email                                         | Password     | File              |
| --------------------------------------------- | ------------ | ----------------- |
| [alice@example.com](mailto:alice@example.com) | Password123! | demo_document.txt |
| [bob@example.com](mailto:bob@example.com)     | Password123! | demo_document.txt |
| [carol@example.com](mailto:carol@example.com) | Password123! | demo_document.txt |

These are dedicated demo accounts for testing.

## Step 8 — Start the server

```bash
python manage.py runserver
```

The Custom Backend will be available at:

```text
http://127.0.0.1:8000/
```

---

# 2. Testing the Custom Backend

The Postman collection is available under:

```text
postman/collections/Secure Login/
```

The main authentication flow is:

```text
Register
   ↓
Login
   ↓
Receive Access + Refresh Tokens
   ↓
Access Protected Endpoints
   ↓
Upload / View Files
   ↓
Logout
```

## Registration

```text
POST /register
```

Example request:

```json
{
    "first_name": "Alice",
    "last_name": "Demo",
    "username": "alice@example.com",
    "email": "alice@example.com",
    "password": "Password123!"
}
```

## Login

```text
POST /login
```

The response provides an access token and refresh token.

Use the access token for protected requests:

```text
Authorization: Bearer <access-token>
```

## Current User

```text
GET /me
```

Returns the currently authenticated user.

## File Operations

The authenticated user can:

* Upload a file
* List their files
* View file details
* Download their files

## User Isolation Test

The application enforces ownership of files.

For example:

```text
Alice → Alice's file → Allowed
Bob   → Alice's file → Denied / 404
```

A user cannot access another user's file simply by knowing its file ID.

---

# 3. Logout Implementation

## Custom Backend

The Custom Backend uses JWT authentication with access and refresh tokens.

During logout, the refresh token is sent to the backend.

The backend blacklists the refresh token:

```python
token = RefreshToken(refresh_token)
token.blacklist()
```

This prevents the refresh token from being reused to obtain new access tokens.

The frontend also clears the locally stored authentication tokens.

An already-issued access token is not immediately revoked and remains valid
until its configured expiry.

## Appwrite

Appwrite manages the authentication session.

Logout removes the current Appwrite session.

---

# 4. JWT vs Session-Based Authentication

The Custom Backend uses JWT authentication because it is well suited to REST
APIs and allows the client to authenticate requests using an access token.

JWT also provides direct control over token handling and expiration. However,
JWT revocation requires additional implementation because an issued access
token normally remains valid until it expires.

Appwrite uses managed sessions. Appwrite handles session creation,
maintenance, and deletion, reducing the amount of authentication
infrastructure that needs to be implemented manually.

Therefore:

* **JWT:** More direct control over authentication and token handling.
* **Appwrite Sessions:** Less authentication infrastructure to build and
  maintain manually.

---

# 5. User Data Isolation

## Custom Backend

Every uploaded file is associated with the authenticated Django user.

File listing is restricted to the current user.

Conceptually:

```python
UserFile.objects.filter(owner=request.user)
```

Individual file access also checks ownership:

```python
UserFile.objects.get(
    id=pk,
    owner=request.user
)
```

Therefore, knowing another user's file ID is not sufficient to access the
file.

Example:

```text
User A → User A file → Access allowed

User B → User A file → 404 / Access denied
```

## Appwrite

Appwrite database and storage permissions are configured to restrict access
to the appropriate authenticated user.

Each file is associated with its user, and permissions prevent another user
from accessing that file.

---

# 6. What Appwrite Handles Automatically

Appwrite provides managed functionality for:

* User registration
* User authentication
* Password authentication
* Session management
* Current-user information
* Session deletion
* Database infrastructure
* Storage infrastructure
* File operations
* Permission enforcement

---

# 7. What Was Configured Manually

The following Appwrite resources and settings were configured for this
application:

* Appwrite project
* Authentication configuration
* Database
* Files collection
* Collection attributes
* Storage bucket
* Database permissions
* Storage permissions
* User-to-file relationships
* Frontend Appwrite integration

The Appwrite frontend integration is implemented in:

```text
frontend/appwrite-adapter.js
```

Additional Appwrite implementation documentation is available in:

```text
appwrite-backend/README.md
```

---

# 8. Appwrite Setup

The Appwrite implementation requires an Appwrite project.

## Step 1 — Create an Appwrite Project

Create an Appwrite project and configure the project information required by
the frontend.

Do not commit Appwrite API keys or server secrets to the repository.

## Step 2 — Configure Authentication

Enable the authentication method required by the application.

Create the following demo users:

| Email                                         | Password     |
| --------------------------------------------- | ------------ |
| [alice@example.com](mailto:alice@example.com) | Password123! |
| [bob@example.com](mailto:bob@example.com)     | Password123! |
| [carol@example.com](mailto:carol@example.com) | Password123! |

## Step 3 — Configure the Database

Create the database used by the application.

Create the required files collection and configure the required attributes.

## Step 4 — Configure Storage

Create the Storage bucket used for uploaded documents.

## Step 5 — Configure Permissions

Configure database and storage permissions so authenticated users can access
only their own files.

## Step 6 — Create Test Files

Create one test document for each demo user.

Example:

```text
Alice → alice_demo.txt
Bob   → bob_demo.txt
Carol → carol_demo.txt
```

Each file should be associated with its corresponding user.

## Step 7 — Test the Appwrite Flow

Test:

```text
Register
   ↓
Login
   ↓
Current User
   ↓
Upload File
   ↓
List Files
   ↓
Download File
   ↓
Logout
```

## Step 8 — Test User Isolation

Login as another user and verify that the first user's files cannot be
accessed.

---

# 9. Rate Limiting

The Custom Backend applies rate limiting to the login endpoint.

The configured login throttle limits repeated anonymous login attempts.

When the limit is exceeded, the API returns:

```text
429 Too Many Requests
```

This reduces the risk of repeated brute-force login attempts.

---

# 10. Security Considerations

The project uses several security controls:

### Password Hashing

Django's user management system hashes passwords rather than storing them as
plain text.

### JWT Authentication

Protected API endpoints require a valid JWT access token.

### Refresh Token Blacklisting

Refresh tokens are blacklisted during Custom Backend logout.

### Rate Limiting

Repeated login attempts are throttled.

### User-Level Authorization

Users can access only files belonging to their own account.

### Appwrite Permissions

Appwrite database and storage permissions are used to enforce user-level
access control.

### Secret Management

Sensitive values are stored in environment variables.

The repository intentionally excludes:

```text
.env
database credentials
API keys
Appwrite server secrets
private certificates
uploaded personal documents
```

A safe configuration template is provided as:

```text
custom-backend/.env.example
```

---

# 11. Postman Testing

The Postman collection used for API testing is available at:

```text
postman/collections/Secure Login/
```

It can be used to test:

* Registration
* Login
* Current user
* File upload
* File listing
* File details
* File download
* Logout
* Authentication and authorization behavior

---

# 12. Test Users

## Custom Backend

Run:

```bash
python manage.py seed_demo_data
```

The following users will be created:

| Email                                         | Password     |
| --------------------------------------------- | ------------ |
| [alice@example.com](mailto:alice@example.com) | Password123! |
| [bob@example.com](mailto:bob@example.com)     | Password123! |
| [carol@example.com](mailto:carol@example.com) | Password123! |

Each user receives a sample file.

## Appwrite

Create the same three demo accounts in the configured Appwrite project.

Use:

```text
alice@example.com
bob@example.com
carol@example.com
```

with:

```text
Password123!
```

Create a test file for each account.

---

# 13. What I Would Improve Given More Time

Given additional development time, I would improve the project by:

* Adding comprehensive unit and integration tests
* Adding stronger file type and MIME-type validation
* Adding file-size restrictions
* Improving brute-force protection
* Adding audit logging for authentication and file access
* Improving JWT revocation mechanisms
* Improving frontend error handling
* Adding CI/CD automation
* Adding production HTTPS configuration
* Using centralized production secret management
* Adding stronger monitoring and security logging

---

# 14. Conclusion

This project demonstrates two approaches to implementing secure authentication
and file access.

The Custom Backend provides direct control over JWT authentication, logout,
rate limiting, authorization, and file ownership.

The Appwrite implementation provides managed authentication, sessions,
database, storage, and permissions.

Both implementations enforce user-level access control so that users can
access their own files without being able to access files belonging to other
users.
