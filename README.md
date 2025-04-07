# Kolik – Secure Supermarket Price Comparison App

Kolik is a full-stack web application that allows users in the Czech Republic to compare grocery prices across supermarkets, helping them find the best deal for each item and their whole shopping basket.

---

## Project Overview

- **Backend**: Django + Django REST Framework  
- **Frontend**: Will be added soon   
- **Admin Panel**: Used for entering real product data  
- **Multilingual**: Czech + English support  

---

## Features Implemented (Backend )

- [x] Secure Django backend setup with `.env`  
- [x] Product models: generic products vs. supermarket-specific variants  
- [x] Supermarket & category models  
- [x] Admin panel to manage prices and images  
- [x] REST API endpoints:
  - Best deal per product
  - All product variants
- [x] Czech + English internationalization  
- [x] Static + media file support  

---

## Tech Stack

| Part      | Stack                          |
|-----------|--------------------------------|
| Backend   | Python, Django, Django REST    |
| Frontend  | Coming soon (React or HTML)    |
| Database  | SQLite (PostgreSQL later)      |
| Hosting   | Render.com (planned)           |

---

##  Project Structure

Kolik/  
├── backend/        # Django backend  
│   ├── config/  
│   ├── core/  
│   └── ...  
├── frontend/       # Frontend will go here later  
├── README.md       # Main project overview  
└── DEVLOG.md       # Daily development log  

---

## 🛠Local Setup (Backend)

### Step 1: Clone the repository

```bash
git clone https://github.com/agatalangova17/Kolik.git
cd Kolik/backend
```

### Step 2: Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set up `.env` file in `/backend/` with:

```env
SECRET_KEY=your-secret-key
DEBUG=True
```

### Step 5: Run migrations and start the server

```bash
python manage.py migrate
python manage.py runserver
```

### Step 6: Access the admin panel

Open [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) in your browser and log in.

---

##  Team

- **Agáta Langová** – Backend development  
- **Dawid Piorkowski**
- **Nokulunga Motsweni**
- **Dren Krasniqi**
- **Teo Bocev**

---

## Project Timeline

- Development: April – May 2025  
- MVP Launch Goal: June 2025  


