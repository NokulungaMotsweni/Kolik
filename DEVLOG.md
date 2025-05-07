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

### 2025-04-13 (Agáta)
### Refactoring & Structure
- Modularized views:
  - Moved all product-related logic to `product_views.py`
  - Moved authentication logic to `auth_views.py`
- Cleaned up imports and separated logic for better maintainability

### Registration Feature
- Created `RegisterView` using DRF’s `CreateAPIView`
- Built `RegisterSerializer` with:
  - Strong password validation (length, uppercase, digit, special character)
  - Confirm password match
  - User created as inactive by default
- Logged user consent (terms and privacy)

### Product Views Refactor
- Replaced manual responses with serializers:
  - `CategorySerializer`, `GenericProductSerializer`, `ProductVariantSerializer`
- Updated views:
  - `list_all_products`
  - `products_by_category`
  - `best_deal_by_id`
  - `all_variants_by_product`

### Basket Price Calculation
- Refactored `calculate_basket` to use helper function `calculate_total_per_supermarket`
- POST returns cheapest supermarket and totals
- GET provides usage example
- Added TODOs:
  - Add BasketSerializer for input validation
  - Optional: caching or saving basket results for logged-in users

### Login Feature (Phase 1)
- Added `LoginView` (email + password only)
- Implemented `LoginSerializer`:
  - Validates credentials
  - Ensures user is active
- Session/token logic planned in next steps

## Date: April 16, 2025  (Agáta)
### Branches: `refactor-app-structure`, `fix-login-flow`  
 
- Refactored Django backend into modular apps:
  - `users` – registration, login, logout, and user model
  - `products` – categories, generic products, product variants
  - `shopping_cart` – basket calculation and supermarket comparison
- Deleted deprecated `core` app after successful migration.
- Moved business logic into `services.py` for better separation and scalability.
- Replaced two-step login flow with **one-step email + password authentication**.
- Implemented secure logout with CSRF and session handling.
- Created `BasketSerializer` to validate shopping cart structure.
- Fixed logout handling (only allows POST + session-based requests).

---

## Date: 19th April 2025 (Noki)
### Branch(es): Noki-User-1
#### User Verification Flow

* **UserVerification** Model Created:
  * Token Hashing, Expiry (`expires_at`), attempt_tracking and Single use control.
  * The token is stored has, the raw token is generated and sent separately. 
    * This is currently just printed out, email API needs to most likely get integrated here.
  * Token integrated into **RegisterSerializer.Create()**
    * Expiration set to 20 Minutes (Team discussion needed to finalise duration).
    * Token printed (will be replaced by email later)
* Added **VerifyUserView** for the validation of tokens and active users.
  * When token is valid, `is_email_verified` + `is_active` is updated.
  * Full safety checks included (duplicate, expired, already-used)

#### VerificationType
* Created **VerificationType** model with:
  * Custom 'verification_type_id' PK
  * Expiry config per type (via `DurationField`)
  * `requires_token` flag

## Date: 20th April 2025 (Noki)
### Branch(es): Noki-User-1
#### Integrated **VerificationType** into **RegistrationFlow**
* `RegistrationSerializer.create()` updated to;
  * Lookup or create a **VerificationType** instance (Email).
    * Temporarily a get_or_create for Dev and Testing purposes, once in production should probably switch to `.get()`.
    * `expires_on` value is used to calculate `expires_at` dynamically.
    * Hardcoded `timedelta(minutes=20)` value is eliminated.
* This makes the system easily expandable (e.g., phone vs email with different expiry times).

#### Add **LoginAttempt** Model for Tracking Login Activity
Introduced a new model called LoginAttempt to log and audit all user login attempts, successful or failed.
##### Details:
* Created **LoginAttempt** in users/models.py to store metadata about each login try.
* Captures:
    * email_entered: The email input provided by the user.
    * success: Boolean indicating whether the login was successful.
    * failure_reason: Descriptive reason for failure (e.g., invalid credentials, inactive account).
    * ip_address: IP address of the request.
    * device: Device/User-Agent string.
    * timestamp: When the attempt occurred (this is autofilled).
* Helps with:
    * Security auditing
    * Suspicious login detection
    * Future rate limiting or lockout features (as per the TODO list)

#### Capture Attempts in LoginSerializer Enhanced the Login Process to Track All User Login Attempts Directly Within the LoginSerializer.
##### Details:
* Inside `LoginSerializer.validate()`, we now capture each login attempt and store metadata including:
    * Entered email.
    * Whether the attempt was successful (boolean value so true or false)
    * Failure reason (missing credentials/invalid credentials/inactive account) (logic to be added in enum.py to store better reasons in the DB).
    * IP address.
    * Device/User-Agent. (Still to decide which info we want to extract and save for this).
* The request context is passed into the serializer from **LoginView**, allowing access to request headers for logging.
* This improves visibility into authentication activity and lays the foundation for features like suspicious login detection and rate-limiting.
##### Files Updated:
* serializers.py
* views.py (LoginView)

#### Implement Audit Logging & Login Attempt Tracking
Added a centralized logging system to capture the user actions and detailed login attempts for an improved authentication visibility and auditing.
##### Details:
* Added two models:
    * *AuditLog* — logs all the general user actions like login, logout and verification (has room for expansion if needed).
    * *LoginAttempts* — tracks login-specific data including:
        * Entered email (whether it is an active user or not).
        * Success status (boolean).
        * Failure reason (normalized using enums.py).
        * IP address.
        * Device/User-Agent.
* Introduced `log_login()` to log both *LoginAttempts* and a general audit record in one call.
* Created `log_action()` for an all-purpose audit logging across the board.
* Added enums (**AuditAction**, **AuditStatus**, **LoginFailureReason**) to maintain consistent action names and failure reason codes.
* Updated the **LoginView**, and **VerifyUserView** to use the new logging functions.
Files Updated:
* models.py
* enums.py
* utils/audit.py
* views.py (LoginView, LogoutView, VerifyUserView)


## Date: 21st April 2025 (Noki)
#### Branch(es): Noki-Users-1
##### Improve Django Admin Configuration for User Management & Auditing


##### UserVerificationAdmin Cleanup
* Enhanced docstring for consistency and clarity.

##### LoginAttemptsAdmin Fixes
* Fixed unresolved references caused by mismatched field names in `list_display` and `search_fields`.
    * Verified model fields exist and adjusted search logic accordingly.
    * Used `user__email` only if user is a ForeignKey.
* Added `date_hierarchy = 'timestamp’` for better navigation.
* Bettered `search_fields` and filters for better audit and review capabilities.


#### Add **Logout Logging** via **AuditLog** for Enhanced Traceability
Logging of user logout activity to the **AuditLog** model for better traceability and security auditing.

##### Details:
* Updated the **LogoutView** in **views.py** to capture and log each logout action.
* On successful logout:
    * Calls log_action() with "logout" as the action.
    * Logs status as "SUCCESS".
* On failure:
    * Haven’t implemented.
* Captured metadata includes:
    * Authenticated user (if any).
    * IP address (with fallback to REMOTE_ADDR).
    * Device/User-Agent string.
    * Path of the logout request.
    * Timestamp (auto-filled by the model).
* This helps with:
    * Tracking user session ends.
    * Investigating unauthorized or suspicious logout behavior.
    * Creating a full login/logout activity trail per user.

#### Enhance **AuditLog** to Store IP Address
Extended the **AuditLog** model to include IP address information for more accurate request context.
##### Details:
* Added a new field:`ip_address = models.GenericIPAddressField(null=True, blank=True)` in **AuditLog**.
* Ensure IP is captured in:
    * Login attempts
    * Email verifications
    * Logout events
    * Any future action using log_action
* Helps with:
    * Audit trail accuracy
Files Updated:
* models.py (AuditLog model)
* utils/audit.py (log_action() )
* views.py (LogoutView updated)


### 2025-04-23 — MFA & Password Reset Enhancements (Agáta)  
**Branch:** `mfa`

#### MFA flow finalized
- Enforced **mandatory MFA setup** after successful login.
- Added **QR code generation** using `pyotp` and `qrcode` for Google Authenticator.
- Created views:
  - `MFASetupView` — generates QR and secret
  - `VerifyMFAView` — verifies user's 6-digit code
  - `MFALoginView` — completes MFA-protected login
- Logged MFA actions:
  - `mfa_setup_started`
  - `mfa_verified`
  - `mfa_login`
- Used `log_action()` to store logs in **AuditLog**.
- No new models — all MFA info stored on the user model.

#### Password reset flow implemented
- Reused **UserVerification** and **VerificationType** models — no new DB fields.
- Views added:
  - `PasswordResetRequestView` — prints reset token to terminal
  - `PasswordResetConfirmView` — validates token and resets password
- Token expiration (30 min) handled via `VerificationType`.
- **No logging or rate limiting yet** 

#### Cleanup and refactor
- Moved `/verify/` endpoint from `config/urls.py` to `users/urls.py` for clarity.
- Fixed serializer typo: `expires_on` → `expires_at` to fix token expiry issue.
- Moved `.idea/` and backend `.gitignore` entries to **root `.gitignore`** for a cleaner repo (removes IDE clutter).

### 2025-04-25 — Authentication refactor (Agáta)  
- Refactored full registration, email verification, login, MFA setup, MFA login, and logout flows.
- Users become is_active after email verification.
- Forced MFA setup after first login if MFA is not configured yet.
- If MFA is missing → login allowed only for MFA setup.
- If MFA is enabled → proceed to MFA code verification.
- Added name field to CustomUser model.
- Manually tested full secure authentication flow end-to-end
- Confirmed session cookies are properly created and deleted.


## Date: 27st April 2025 (Noki)
### Branch(es): Noki-Users-1
#### Implement Full Cookie Consent Tracking and Storage (Mandatory Only vs Mandatory + Analytics)

##### Add Cookie Model for Tracking:
  * Created new **Cookie** and **CookieConsent** models to track the user cookies and their consent events.
    * **Cookie** nodel tracks:
      * cookie name
      * cookie_value
      * cookie_type
      * lined to the user
    * **CookieConsent** models tracks:
      * Whether the user has given consent
      * Which cookie policy version they have agreed to
      * Consent Type: Mandatory Only or Mandatory + Analytics
    * Enforced ForeignKey and One-to-One relations properly for traceability.

##### Add Enums for Cookie Types and Consent Types:
* Added CookieType Enums in enum.py:
  * `mandatory`
  * `analytics`
* Added CookieConsentType Enums in enum.py:
  * `mandatory_only`
  * `mandatory_and_analytics`

##### Add Cookie Type Mapping:
* Created `COOKIE_TYPE_MAP` dictionary to classify cookies from browser automatically.
  * Known cookies mapped to their typed.
  * Cookies mapped:
    * csrftoken
    * sessionid
    * ga
    * gid
* Only the cookies listed are saved in the mapping for performance and security purposes.

##### Create CookieConsent Views:
* Added two views:
  * `accept_mandatory_only`
  * `accept_mandatory_and_analytics`
* Users are allowed to choose between accepting only essential cookies versus analytical tracking.
* **Added a mechanism that the frontend can use with two buttons in the cookie banner.**

##### Update the URL for Consent Choices:
* Added two new paths:
  * `/accept-mandatory/`
  * `/accept-mandatory-analytics`

##### Update Cookie Tracking Logic:
* Used `.filter().first()` for safer lookup of user consent record.
* Skips analytics cookies automatically if user refused them.

##### Integrate AuditLog for Consent Events
* Extended AuditLog to add cookie consent views.
  * Logs:
    * `action="cookie_consent"`
    * `status="SUCCESS`
  * Captures device info, IP address, path, and timestamp automatically.
* Ensures full traceability of user choices for legal compliance.

#### Files Created / Updated:
* `models.py`
  * **Cookie** 
  * **CookieConsent**
* `enums.py`
  * **CookieType**
  * **CookieConsentType**
* `views.py`: Consent and Tracking views.
* urls: New routing for consent actions
* utiles/audit.py: Used existing log_action for consent events.
* Cookie banner template (updated to offer Accept Mandatory vs Accept All)

## Date: 2nd May 2025 (Noki)
### Branches: Noki-Users-1
#### Implement Signup Attempt Logging and Audit Trail for User Registration

##### Add **SignupAttempt** Model to Logging Flow:
* Centralised the logging of the signup attempts. Failed and successful.
* Recorded Metadata
  * `email_entered`: Email
  * `success`: Flag
  * `failure_reason`: Enum
* Successful login logged in create() after user created and verification started.
* Uses log_action for consistency

##### Ensure Unit Test Coverage for Signup Validation:
* Added direct unit test for `RegisterSerializer` (API endpoint could be added to replace).
* Used `APIRequestFactory` to simulate `request` context for logging.
* Verified that weak passwords trigger the correct validation errors.
* Confirmed logging behavior for failed signup attempts functions as expected.

#### Files Created/Updated:
* `models.py`
  * Integrated **SignUpAttempts** into serialiser logic.
* `enums.py`
  * Added **SignupFailureReason**
  * Added `AuditAction.SIGNUP_SUCCESSFUL`
* `serializers.py`
  * Updated **RegisterSerializer** `.validate()` and `.create()`
* `tests.py`
  * Added serializer test for password rejection/acceptance.

### April 27 – Disposable Email Protection (Agáta)

**Implemented protection** against disposable email addresses during user registration.
- Created a custom `disposable_domains.py` file containing the full list of known disposable domains, sourced from the GitHub repo: [`disposable-email-domains`](https://github.com/disposable-email-domains/disposable-email-domains).
- Integrated the domain check directly in the `RegisterSerializer` by extracting the domain from the submitted email and comparing it against the loaded list.
- Registration is rejected with a clear validation error message if the user attempts to sign up with a temporary email service.

## April 28, 2025 – Profile Management (Agáta)

#### Built secure profile management functionality:

- Created `ProfileView` with `GET` and `PATCH` methods to allow users to **view and update their name**. The response also includes `email` and `mfa_enabled` status.
- Implemented a **secure password change endpoint** (`ChangePasswordView`) requiring:
  - Current password
  - Strong new password (validated for length, uppercase, lowercase, digit, and special character)
  - MFA code verification
- Developed the **email change request flow** (`RequestEmailChangeView`):
  - Requires current password, new email, and MFA verification.
  - Saves the new address as `pending_email` and sends a token-based confirmation link to the user.
- Added `ConfirmEmailChangeView` to complete the email change process **after token verification**.
- All views are protected using `IsAuthenticated`, strict `request.user` ownership validation, and **MFA checks** where applicable.

## May 1, 2025 – Geolocation + Email Flow Fix (Agáta)

### Implemented geolocation and VPN detection middleware to control access:

- First attempts **country lookup via IPInfo API** (token-based).
- If IPInfo fails, falls back to **local MaxMind GeoLite2 database** using `geoip2`.
- Integrated **VPN/proxy detection via proxycheck.io API**, which evaluates risk level and proxy status.
- Middleware **caches results in the user’s session** using flags:
  - `geo_checked`
  - `geo_country`
  - `geo_proxy`
- Access is **blocked** if:
  - The IP’s country is **not `CZ`** → redirects to `REDIRECT_URL`
  - A VPN/proxy is detected **within CZ** → returns a JSON warning (`451`) prompting the user to disable the VPN
- Added `DEBUG_IP_OVERRIDE` from `.env` to simulate custom IPs during local development.

### Fixed email change flow:
- Corrected logic to ensure that **`pending_email` is stored**, and no change occurs until the user confirms via token.
- Improved verification handling and validation in `ConfirmEmailChangeView`.

## Date: 3 & 4th May 2025 (Noki)
### Branches: Noki-Users-1
#### Implement Core Backend Logic for Supermarket Cart Comparison and Pricing Flow

##### Models & Seed Data Foundation:
* Confirmed and validated models for:
  * `Category`, `GenericProduct`, `ProductVariant`, `Supermarket`.
  * `ShoppingCart`, `CartItem` with `locked` variant support.
* Reviewed sample seed data script covering real product and variant entries across Tesco, Billa, Albert.
* Implemented the `locked` logic in `CartItem`:
  * If `locked=True`, user wants exact variant.
  * If `False`, variant can be swapped.
* Added the unit support anf naming conventions for product comparisons.

##### Services Layer Re-Architecture:
* Replaced `calculate_total_per_supermarket()` with `analyze_basket_pricing(basket)`.
  * Returns:
    * `products`
    * `supermarket_totals`
    * `best_mixed_basket`
    * `warnings`
  * Automatically removes duplicates `product_id` entries and combines quantities.
* Implemented optional warnings for missing products/variants without breaking structure.
* Added:
  * `compare_supermarkets(basket)`
  * `get_mixed_basket(basket)`
  * `find_cheapest_supermarket(...)`
  * `find_cheapest_supermarket_name(...)` removed after consolidating output.
  * `get_breakdown_for_supermarket(...)` store-specific pricing + missing items
* Final output returns:
  * `products`
  * `supermarket_totals`
  * `best_mixed_basket`
  * `warnings` 

##### Cart Management Service Logic:
* Cleaned up:
  * `add_to_cart(user, product_id, variant_id, quantity, locked=True)`
    * Uses `update_or_create` on `(cart, variant)` for consistent behaviour with `unique_together.`
  * `remove_from_cart(user, product_id)` [under review]
* Added:
  * `get_user_cart_items(user)` → raw product and quantity input for analysis.
  * `get_user_cart_summary(user)` → frontend-friendly summary with variant and lock state

##### Pricing Logic Features:
* Mixed basket: best variant per product from any store.
* Per-supermarket breakdown: what’s available + itemized cost.
* Cheapest supermarket: full-stock only store with the lowest price.
* Removal of repeated/duplicated product entries to prevent inflated totals.
##### API Views & Endpoint Structure:
* Structured the following cart endpoints:
  *` GET /cart/view/` → calls `get_user_cart_summary()` 
  * `GET /cart/compare/` → calls `compare_supermarkets() `on user items.
  * `GET /cart/cheapest-supermarket/` → finds store with the lowest total (currently only returns the one with all
  items.
  * `GET /cart/mixed-basket/` → returns cheapest variant per product.
  * `POST /cart/add/` → adds item to cart with variant + locked flag.
  * `DELETE /cart/remov`e/ → removes product from cart (variant-aware logic pending).
* All views are guarded with `IsAuthenticated`.
* Ensured views rely solely on the service layer for logic (thin views).

#### Files Created/Updated:
* `products/models.py`, `shopping_cart/models.py`
  * Clarified `locked` behavior, related names, and relationships.
* `shopping_cart/services.py`
  * Pricing logic, cart management, supermarket breakdown.
* `shopping_cart/views.py`
  * Cart endpoints + robust fallback handling for empty/missing cart.
* `shopping_cart/serializers.py`
  * `CartAddSerializer`, `CartRemoveSerializer`, `BasketSerializer`.
* `shopping_cart/urls.py`
  * Added full route map for all 7 cart endpoints.


## May 4, 2025 – Unverified User Cleanup (Agáta)

**Implemented a custom Django management command** to automatically clean up unverified accounts:

- Deletes user accounts that remain **unverified for more than 24 hours** after registration.
- Designed to be scheduled via a **cron job** for routine cleanup.
- Helps reduce database clutter and enforce account lifecycle security policies.

## Date: 5th May 2025 (Noki)
### Branches: Noki-Users-1
#### Shopping Cart Breakdown & Pricing Comparison – Stability & Accuracy Fixes

##### Fix Breakdown View to Reflect Actual Items and Totals
* Updated `get_breakdown_for_supermarket()`:
  * Recalculates total from matched items only instead of using precomputed basket totals.
  * Rewrites `meta.supermarket_totals` to reflect corrected per-store totals.
  * Ensures `unavailable_items` are correctly listed per supermarket.
  * Prevent `NoneType` errors when converting `price` or `total` using `float()`.

#### Files Updated:
* `services.py`
  * `analyze_basket_pricing()`
  * `get_breakdown_for_supermarket()`
* `views.py`
  * `view_user_cart()`
  * `add_to_cart_view()`
* `models.py`
  * **CartItem** FK updated with related_name ='items'


## Date: 6th May 2025 (Noki)
### Branches: Noki-User-1
#### Refactor Pricing Logic, Implement Full API Layer, Fix Totals, and Seed Dataset for Shopping List System

##### Refactor and Fix Shopping List Pricing Logic:
* Extend and cleaned up `analyze_basket_pricing()`:
  * Removed duplicate product entries.
  * Added handling of products with missing variants.
  * Refactored output structure to be consistent even when errors occur.
  * Added accurate Decimal-based total calculations with rounding.
  * Built robust "meta" output: supermarket_totals, warnings, mixed_basket.

##### API Layer for Shopping List Operations:
* Amended the API endpoints for user shopping list interactions.
  * `add/` - Adds item to list
  * `remove/ `- Removes item from the list (fixed faulty logic)
  * `clear/` - Clears the entire shopping list.
  * `view/` - Views all of the items in the shopping list.
  * `compare/` - Compare the total cost across the supermarkets.
  * `mixed-basket/` - Return best-value list using the cheapest variants.
  * `supermarket-breakdown/` - Get detailed per-supermarket price breakdown.
* Structured responses for frontend compatibility (item names, quantities, pricing, variant info).

##### Robust Error Handling;
* View-layer feedback for:
  * Missing shopping list
  * Empty list states
  * Invalid product or supermarket inputs
* Serializer-level validation:
  * `quantity >= 1`
  * `product_id`
    * `product_id` present
    * `variant_id` optional but validated if given

##### Bug Fixes and Core Logic Corrections:
Fixed: Totals were missing/inconsistent:
  * Used Decimal for precision in financial values.
  * Applied round(..., 2) to all prices and totals.
  * Ensured every supermarket was accounted for in the output, even if a variant is missing.
Fixed: Missing Variant or Product Crashed Logic:
  * Added warnings for missing products or unavailable variants.
  * Populated fallback rows with None instead of skipping entries silently.
  * Guaranteed consistent response structure even when some items were missing.
* Fixed `/remove/` View Was Broken:
  * Removed incorrect `get_or_create()` usage in deletion logic.
  * Checked for actual existence of item before removing.
  * Returned clear messages and 404 when item not found.
* Fixed: Unstable or Tuple-Based Responses:
  * Standardised function return formats to always yield clean dicts.
  * Used `.get()` accessors and wrapped logic to avoid unexpected None/tuple returns.
  * Ensured frontend receives consistent, parseable structure.
* Fixed: Duplicate Products Were Not Aggregated/Tallied:
  * Consolidated all product quantities in basket before pricing analysis.
  * Used `defaultdict(Decimal)` to merge duplicate product entries.
  * Prevented inflation of pricing totals from repeated inputs.

#### Files Created/Updated:
* s`ervices.py`
  * Refactored pricing logic, fixed total calculations, added warning system.
* `views.py`
  * Built all REST endpoints for shopping list operations and pricing insights.
* `serializers.py`
  Added custom serializers for adding, removing, and validating shopping list input.
* `urls.py`
  Connected all new endpoints under the /list/ namespace.
  
## Date: 5th May 2025 (Teo)
### Branches: third_party_apps_v2
#### Sendgrid automatic email implementation and testing, RECAPTCHA V3 and V2 as fallback implementation and testing

##### Sendgrid automatic email implementation and testing
  * config/settings.py: imported necessary files for sendgrid, defined default email and secret key (.env).
  * utils/email.py: defining the base email that will be used for multiple classes/functions.
  * users/models.py: importing timedelta, adding more to the UserVerification object.
  * users/serializers: Inside class RegisterSerializer, after raw token creation, created the structure of the email the user will receive to help them verify themselves.
  * users/views: Inside class PasswordResetRequestView, after raw token creation, created the structure of the email the user will receive to help them reset their password.
  * users/views: Inside class RequestEmailChangeView, after raw token creation, created the structure of the email the user will receive to help them change the email of their account.

##### RECAPTCHA V3 and V2 as fallback implementation and testing
  * config/settings.py: imported necessary files for sendgrid, defined site key and secret key for both V2 and V3 RECAPTCHA
  * utils/recaptcha.py: defying the logic for Recaptcha. Implemented V3 as the main version, but in the case of a low score or failure, the website resorts to V2.
  * users/views.py: Implements the code in recaptcha.py for user registration.



## May 6, 2025 – Product Detail View + Confirm Email Flow (Agáta)

**Implemented product detail API view**:
- Returns product name, amount, unit, and category name.
- Useful for showing product detail pages or popups in the frontend.

**Refined the email change confirmation flow**:
- Ensures that **token-based verification** is required before applying the email change.
- Final email update only occurs **after successful confirmation** via `ConfirmEmailChangeView`.



