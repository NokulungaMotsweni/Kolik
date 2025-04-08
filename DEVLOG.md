# Dev Log — Kolik Backend  
_Started April 7, 2025_

---

### 2025-04-07 — Project Kickoff (Agáta)

Set up backend from scratch:
- Created virtual environment, started Django project (`config`)
- Added `.env` for secure settings (SECRET_KEY, DEBUG, etc.)
- Configured `settings.py` with timezone, language, static/media, and internationalization (Czech/English support)

Models created:
- `Supermarket`: Tesco, Billa, Albert
- `Category`: e.g., Dairy, Bakery, Vegetables..
- `GenericProduct`: shared products like "Whole milk 1L"
- `ProductVariant`: specific brands with price, supermarket, image

Admin:
- Populated all MVP products for testing purposes
- Entered prices for Billa, Albert, Tesco

REST API (Django REST Framework): created 2 API endpoints
- `/api/best-deal/<product_id>/`: returns best-priced product variant
- `/api/all-variants/<product_id>/`: returns all variants for a product

GitHub:
- Repo initialized, first full commit & push complete

---

### 2025-04-08 — Backend Refinement & API Expansion (Agáta)

**Code cleanup & repo structure:**
- Added comments to `settings.py` 
- Cleaned `urls.py` in both `config` and `core` apps and added comments
- Confirmed `.gitignore` safely ignores `.env` and `db.sqlite3` (local only)

**API development:**
- Reorganized `api_views.py` and grouped endpoints:
  - `/api/categories/` – List of all categories
  - `/api/products-by-category/<category_id>/` – All generic products in one category
  - `/api/best-deal/<product_id>/` – Cheapest product variant for one generic product
  - `/api/all-variants/<product_id>/` – All variants for one generic product
  - Added new API endpoint /api/products/ to return all generic products (useful maybe for frontend to display full product list)

**Frontend collaboration support:**
- Planned shared document: `for_frontend_devs.md` to explain:
  - How to test API
  - Where to find `.env.example` and seed data script (I will create that) to preload MVP data
  - How to access product data


**Admin & DB work:**
- Confirmed image field works in admin panel
- Clarified product structure: generic product vs. supermarket-specific variant
- Verified everything still runs after migrations

**Readme & docs:**
- Finalized `README.md` — includes setup instructions, tech stack, and contributor list
- Ensured `.env` is excluded

---

**Tomorrow:**
- Create and commit `seed_data.py` with full MVP product dataset  
- Create `for_frontend_devs.md` with endpoint list and setup guide  
- Add basket total comparison endpoint (`/api/basket/`)  
- Discuss user accounts
