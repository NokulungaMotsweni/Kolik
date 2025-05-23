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