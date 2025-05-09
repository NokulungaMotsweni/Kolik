## Kolik – Secure Supermarket Price Comparison App

**Kolik** is a full-stack web application that helps users in the Czech Republic compare grocery prices across supermarkets, showing them the best deal for each item and their whole shopping basket.

---

## Project Overview

- **Backend**: Django + Django REST Framework  
- **Frontend**: React.js (in progress)
- **Database**: PostgreSQL (planned)
- **Multilingual**: Supports Czech + English   

---

## Features Implemented (Backend)

- [x] Secure Django backend setup using .env for secrets 
- [x] Custom UUID-based user model (email login, name) 
- [x] Secure user registration with password validation 
- [x] Email verification (required to activate account) — currently using token-based verification; will integrate email sending with SendGrid later.
- [x] Mandatory MFA (Authenticator app) for all users
- [x] Login protected by MFA  
- [x] Secure logout and session management
- [X] Password reset flow — currently token-based; will integrate email sending later
- [x] Product catalog management (products, variants, categories)
- [x] Admin panel for product and user management
- [x] REST API for product browsing and basket price comparison
- [x] Internationalization (English + Czech)
- [x] Static/media file management
- [x] Full audit logging (login attempts, verifications, MFA setup, etc.)    

---

## Tech Stack

| Part      | Stack                          |
|-----------|--------------------------------|
| Backend   | Python, Django, Django REST    |
| Frontend  | React.js (Vite)                |
| Database  | SQLite (PostgreSQL later)      |
| Hosting   | Render.com (planned)           |

---

## Project Structure

```
Kolik/
├── backend/              # Django backend
│   ├── config/           # Main project settings and URLs
│   ├── users/            # User authentication, registration, MFA
│   ├── products/         # Product catalog and supermarket variants
│   ├── shopping_cart/    # Shopping basket price calculation
│   ├── db.sqlite3        # Local development database
│   ├── .env              # Environment variables (not pushed to GitHub)
│   ├── manage.py         # Django management commands
│   └── requirements.txt  # Backend Python dependencies
├── frontend/             # React frontend (in progress)
├── README.md             # Main project overview
└── DEVLOG.md             # Daily development log
```

---

## Local Setup Instructions (Backend)

### 1. Clone the repository

```bash
git clone https://github.com/agatalangova17/Kolik.git
cd Kolik/backend
```

### 2. Create & activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up `.env` in `backend/`

Create a file called `.env` and paste in:

```env
SECRET_KEY=your-secret-key
DEBUG=True
```

>  Never commit real secrets — this file is in `.gitignore`.

### 5. Run migrations & start server

```bash
python manage.py migrate
python manage.py runserver
```

### 6. Access the admin panel

Visit:  
[http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

Log in using your superuser credentials.

---

## Available API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/api/auth/register/` | User registration |
| POST    | `/api/auth/verify/` | Email verification |
| POST   | `/api/auth/login/` | First step login (after email verification) |
| GET    | `/api/auth/mfa/setup/` | Get MFA QR code for setup |
| POST    | `/api/auth/verify-mfa/` | Confirm MFA code |
| POST   | `/api/auth/mfa-login/` | Complete login with MFA code |
| POST   | `/api/auth/logout/` | Logout and delete session |
| POST    | `/api/auth/password-reset/request/` | Request password reset token |
| POST   | `/api/auth/password-reset/confirm/` | Reset password with token |
| GET   | `/api/products/` | List all generic products |
| GET   | `/api/categories/` | List all product categories |
| GET   | `/api/products-by-category/<category_id>/` | Products by category |
| GET   | `/api/best-deal/<product_id>/` | Cheapest variant for a product |
| GET   | `/api/all-variants/<product_id>/` | All supermarket variants |
| POST   | `/api/basket/` | Calculate total basket price per supermarket |
|GET    | `/api/shopping-list/view/` | View the current user's shopping list|
| POST   | `/api/shopping-list/add/` | Add an item to the shopping list |
| DELETE | `/api/shopping-list/remove/`| Remove an item from the shopping list|
| DELETE | `/api/shopping-list/clear/`| Clear all items from the shopping list|
| GET    | `/api/shopping-list/compare/`| Compare total prices of the saved list across supermarkets|
| GET    | `/api/shopping-list/mixed-basket/`| Get the cheapest mixed basket using the best-priced variant from any store |
| POST   | `/api/shopping-list/supermarket-breakdown/`| Get itemized pricing breakdown for a specific supermarket|
| POST   | `/api/shopping-list/basket/`| Calculate basket total using a stateless basket input|

> Test them in browser while the dev server is running.

## Authentication Flow

- User registers with email, name, and password.
- User verifies email through a token link.
- User logs in with email and password (session is created).
- If MFA is not set up, the user is prompted to scan the QR code and verify their 6-digit code.
- User is forced to complete MFA setup (authenticator app).
- User submits the MFA code.
- Future logins require both password and MFA code.
- Full session security and logout functionality.
  

---

## Team

- **Agáta Langová** – Backend development  
- **Dawid Piorkowski** – Frontend development  
- **Nokulunga Motsweni**  - Database Development
- **Dren Krasniqi** - Design, Testing 
- **Teo Bocev** - 3rd Party Services, Logo

---

## Project Timeline

-  **Development**: April – May 2025  
-  **MVP Launch Goal**: June 2025  
