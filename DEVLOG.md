# Dev Log — Kolik 
_Started April 7, 2025_

---

### 2025-04-07 — Project Kickoff (Agáta)

Set up backend from scratch:
- Created virtual environment, started Django project (`config`)
- Added `.env` for secure settings (SECRET_KEY, DEBUG, etc.)
- Configured `settings.py` with timezone, language, static/media, and internationalization (Czech/English support)

Models created:
- Credit: Structure based on design by Nokulunga Motsweni
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
### 2025-04-08 — Basket Logic & Admin Cleanup (Agáta)

**Cheapest basket logic:**
- Implemented `/api/basket/` endpoint:
  → Calculates total price for user's basket per supermarket.
  → Logic uses **cheapest available variant** in each store.
  → Example GET request included.

- Fixed price miscalculation bug: now correctly handles carton quantities (e.g., eggs 10pcs).

- Final testing, pushed all working changes to GitHub.

### 2025-04-10 - Backend Progress (User Accounts, Refactors, Data Seeding)

### Planning & Structure
- Created `models/products.py` and `models/users.py` for better modularity.
- Updated `core/models/__init__.py` to import models cleanly.
- Linked everything in `AUTH_USER_MODEL` as `core.CustomUser`.

### Custom User Model Setup
- Credit: Structure based on design by Nokulunga Motsweni
- Created `CustomUser` model with the following fields:
  - UUID primary key (`id`)
  - Unique `email` (used for login)
  - `phone_number`
  - Flags: `is_email_verified`, `is_phone_verified`
  - Consent timestamps: `terms_accepted_at`, `privacy_policy_accepted_at`
  - Standard fields: `is_active`, `is_staff`, `date_joined`
- Created `CustomUserManager` to handle user creation and superuser logic.

### User Auth & Migration Flow
- Set up `AUTH_USER_MODEL` in `settings.py`.
- Removed default DB and flushed tables to apply UUID changes.
- Ran `makemigrations` and `migrate` successfully.
- Created a new superuser to confirm functionality with UUIDs.

### Data Seeding
- Cleaned old data.
- Successfully ran `core/seed_data.py` to import MVP product variants.
- Script tested and confirmed working without duplicates.

### Git & Branch Management
- Pushed initial model refactor and user structure to `user-auth-setup` branch.
- Merged changes back into `main` after testing.
- Removed working branch post-merge.
- Cleaned commit history by committing only tested updates to `main`.

### 2025-04-11 — Admin Panel & Verification Testing (Agáta)

- Implemented and registered the CustomUser model in the Django admin panel
- Verified admin panel shows all user data cleanly (email, phone, verification status)
- Fixed `add_fieldsets` bug to allow user creation via admin
- Confirmed UUID login and permissions working as expected
---


