# Dev Log — Kolik Backend
_Started April 7, 2025_

---

###  2025-04-07 — Project Kickoff (Agáta)

Set up backend from scratch:
- Created virtual environment, started Django project (`config`)
- Added `.env` for secure settings (SECRET_KEY, DEBUG, etc.)
- Configured `settings.py` with timezone, language, static/media, and internationalization (Czech/English support)

Models created:
- `Supermarket`: Tesco, Billa, Albert
- `Category`: e.g., Dairy, Bakery
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


Tomorrow:
- Start `/api/basket/` logic (compare total price across supermarkets)
- Add `/api/products/` list endpoint
- Add filtering or search options if time allows
