## Kolik – Secure Supermarket Price Comparison App

**Kolik** is a full-stack web application that helps users in the Czech Republic compare grocery prices across supermarkets, showing them the best deal for each item and their whole shopping basket.

---

## Project Overview

- **Backend**: Django + Django REST Framework  
- **Frontend**: Coming soon (React or HTML/CSS/JS)  
- **Admin Panel**: For entering real supermarket product data  
- **Multilingual**: Supports Czech + English   

---

## Features Implemented (Backend)

- [x] Secure Django backend setup using `.env` for secrets  
- [x] Product models: generic products vs. supermarket-specific variants  
- [x] Supermarket & category models  
- [x] Admin panel for product/image/price management  
- [x] REST API endpoints:
  - Best deal per product (by ID)
  - List of all product variants  
  - All categories
  - Products by category  
- [x] Czech + English internationalization  
- [x] Static and media file support  

---

## Tech Stack

| Part      | Stack                          |
|-----------|--------------------------------|
| Backend   | Python, Django, Django REST    |
| Frontend  | HTML/CSS/JS                    |
| Database  | SQLite (PostgreSQL later)      |
| Hosting   | Render.com (planned)           |

---

## Project Structure

```
Kolik/
├── backend/        # Django backend
│   ├── config/     # Main project settings & URLs
│   ├── core/       # Main app (models, views, API)
│   ├── db.sqlite3  # Local database (dev only)
│   ├── .env        # Local secrets file (not pushed)
│   ├── manage.py   # Django CLI entry point
│   └── requirements.txt  # Python dependencies
├── frontend/       # Frontend will be added later
├── README.md       # Main project overview
└── DEVLOG.md       # Daily progress log
```

---

##Local Setup Instructions (Backend)

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

| Endpoint | Description |
|----------|-------------|
| `/api/best-deal/<product_id>/` | Returns the cheapest product variant |
| `/api/all-variants/<product_id>/` | Lists all variants for a product |
| `/api/categories/` | Lists all product categories |
| `/api/products-by-category/<category_id>/` | Lists products in a specific category |
|`/api/basket/`: | POST basket data, returns total price per supermarket | 

> Test them in Postman or browser while the dev server is running.

---

## Team

- **Agáta Langová** – Backend development  
- **Dawid Piorkowski** – Frontend development  
- **Nokulunga Motsweni**  
- **Dren Krasniqi**  
- **Teo Bocev**

---

## Project Timeline

-  **Development**: April – May 2025  
-  **MVP Launch Goal**: June 2025  
