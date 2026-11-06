# Style Haven: Shift-Left Test Pyramid Master Specification
**Document Title:** Style Haven - Test Pyramid Layer-by-Layer Master Specification  
**Platform:** Fashion E-commerce Marketplace  
**Document Version:** 3.0.0-PROD  
**Author:** Principal QA Test Architect  
**Scope:** Exhaustive catalog of all 33 test scenarios cleanly partitioned into dedicated sections: **Unit Tests**, **Component Tests**, **Integration & API Tests**, and **End-to-End (E2E) Tests**.

---

## Executive Overview: Test Pyramid Architecture

```
                         / \
                        /   \
                       / E2E \              [ 5 Tests  - 15% ]  -> Section 4
                      /-------\
                     /  Comp.  \            [ 7 Tests  - 21% ]  -> Section 2
                    /-----------\
                   / Integration \          [ 15+5 Tests - 46% ] -> Section 3
                  /---------------\
                 /    Unit Tests   \        [ 6 Tests  - 18% ]  -> Section 1
                /-------------------\
```

---

## SECTION 1: UNIT TESTS LAYER
* **Shift-Left Focus:** Shifted completely to developer local environment and pre-commit hooks (`husky`).  
* **Target Execution Speed:** `< 10ms` per test (Full suite runs in `< 1s`).  
* **Recommended Frameworks:** `Vitest` / `Jest`  
* **Scope:** Pure functions, mathematical formulas, regex validators, string sanitizers, and array filtering algorithms.

| Test Case ID | Req Ref | Test Scenario Title | Specific Logic / Pure Function Tested | Test Input & Conditions | Expected Outcome | Assigned Engineer |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-CRT-004-U** | Req 3.3 | Promo code discount & subtotal calculation | `calculateCartTotals(items, coupon, taxRate)` | Subtotal: $95.00, Coupon: `SUMMER15` (15%), NY Tax: 8.875%, Free Shipping Threshold: $100 | Discount = -$14.25; New Subtotal = $80.75; Shipping added ($10.00); Tax = $7.17; Total = $97.92 | QA Eng 2 |
| **TC-CAT-004-U** | Req 2.2 | Size chart unit conversions (Metric vs Imperial) | `convertDimensions(val, unit)` | Imperial input: Chest = 38.0", Waist = 32.0", Hips = 40.0" | Function converts accurately using `* 2.54`: Chest = 96.52 cm, Waist = 81.28 cm, Hips = 101.60 cm | QA Eng 2 |
| **TC-OPT-002-U** | Req 7.3 | Loyalty rewards points valuation formula | `pointsToDiscountValue(points, rate)` | User points: 500 points, conversion rule: 100 points = $1.00 | Returns exact monetary credit of `$5.00`; negative points throw `InvalidPointException` | QA Eng 1 |
| **TC-ACC-001-U** | Req 1.1 | Password complexity & email format regex | `validatePasswordStrength(pwd)`, `validateEmail(email)` | Passwords: `weakpass` vs `SecurePass#2026!`; Emails: `user@domain` vs `valid@stylehaven.io` | Weak password rejected with specific policy violation flags; valid email and 12+ char password return `isValid: true` | QA Eng 1 |
| **TC-ACC-004-U** | Req 1.2 | Profile address XSS input sanitizer | `sanitizeAddressInput(rawString)` | Input: `<script>alert('XSS')</script>Apt #4-B, St. John's` | Script tags stripped/escaped; harmless punctuation preserved: `Apt #4-B, St. John's` | QA Eng 1 |
| **TC-SUP-002-U** | Req 6.2 | FAQ keyword search array filter | `filterFaqList(faqs, query)` | 25 FAQ items, search query: `"refund timeline"` | Returns only 2 matching entries tagged with returns/refunds; case-insensitive | QA Eng 1 |

---

## SECTION 2: COMPONENT TESTS LAYER
* **Shift-Left Focus:** Frontend UI isolated testing; runs on every Pull Request build.  
* **Target Execution Speed:** `~200ms - 500ms` per component.  
* **Recommended Frameworks:** `Playwright Component Testing`, `React Testing Library (RTL)`, `Cypress Component`  
* **Scope:** Interactive UI states, swatches, form error styling, disabled button states, modal drawers, and accessibility (ARIA).

| Test Case ID | Req Ref | Test Scenario Title | Component Under Test | Component Props / State | Expected Render & State Behavior | Assigned Engineer |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-CAT-003-C** | Req 2.2 | PDP variant switcher & inventory reflection | `<ProductVariantSelector />` | Variant matrix with `[Cream, M]` stock = 0, `[Black, M]` stock = 5 | Clicking Cream + M renders disabled "Out of Stock" button; switching to Black + M enables button with "Low Stock: Only 5 left!" | QA Eng 2 |
| **TC-CAT-004-C** | Req 2.2 | Size chart drawer & image zoom modal | `<SizeChartDrawer />`, `<ImageZoom />` | `isOpen: true`, high-res image URL: `blazer_hero.webp` | Drawer renders with accessible focus trap; unit toggle switches table values; hover zooms image without pixelation | QA Eng 2 |
| **TC-CRT-003-C** | Req 3.2 | Cart quantity adjustment exceeding stock | `<CartItemQuantityPicker />` | `currentQty: 2`, `maxAvailableStock: 2` | Clicking `+` button is disabled; inline banner renders: *"Only 2 units available in stock"*; quantity clamped at 2 | QA Eng 2 |
| **TC-CHK-001-C** | Req 4.1 | Shipping tier radio selection | `<ShippingMethodSelector />` | Rates: Standard ($8.00, 3-5 days), Express ($20.00, 1-2 days) | Selecting Express radio highlights row and dynamically updates estimated delivery date banner without page reload | QA Eng 3 |
| **TC-SUP-002-C** | Req 6.2 | FAQ accordion expand/collapse transitions | `<FaqAccordion />` | List of 10 FAQ questions, initial state: collapsed | Clicking question expands answer with smooth CSS animation; updates `aria-expanded="true"`; closes on second click | QA Eng 1 |
| **TC-OPT-001-C** | Req 7.1 | Wishlist Heart icon toggle | `<WishlistToggleButton />` | Initial state: `isSaved: false` | Clicking button toggles SVG fill state to active red; fires micro-bounce animation; calls `onToggle(productId)` callback | QA Eng 1 |
| **TC-ACC-004-C** | Req 1.2 | Address form validation & error borders | `<AddressForm />` | Form inputs with missing postal code or invalid characters | Leaving ZIP empty highlights field with red border and renders inline error: *"Postal code is required"* | QA Eng 1 |

---

## SECTION 3: INTEGRATION & API TESTS LAYER
* **Shift-Left Focus:** Backend services, REST/GraphQL APIs, database persistence, and message brokers; runs on PR builds.  
* **Target Execution Speed:** `~50ms - 300ms` per endpoint.  
* **Recommended Frameworks:** `Supertest`, `Playwright API`, `k6` (concurrency), `Testcontainers`  
* **Scope:** Controller validation, database transactions, concurrency row-locks, token lifecycles, and security barriers.

### 3.1 Functional Integration & API Tests

| Test Case ID | Req Ref | Test Scenario Title | Target Endpoint / Event | Test Request Payload | Expected Response & DB Assertion | Assigned Engineer |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-ACC-001-A** | Req 1.1 | User registration endpoint | `POST /api/v1/auth/register` | `{ email: "valid@sh.io", password: "SecurePass#2026!" }` | HTTP 201 Created; password hashed via bcrypt in DB; verification token created in Redis/DB | QA Eng 1 |
| **TC-ACC-003-A** | Req 1.1 | Account lockout defense (Brute Force) | `POST /api/v1/auth/login` | 5 consecutive invalid password payloads within 2 mins | 6th attempt returns HTTP 429 Too Many Requests; lockout flag set in Redis for 15 mins | QA Eng 1 |
| **TC-ACC-004-A** | Req 1.2 | Address book persistence | `POST /api/v1/user/addresses` | `{ addressLine1: "452 Fashion Ave", isDefault: true }` | HTTP 200 OK; address persisted in DB; prior default address toggled to `isDefault: false` | QA Eng 1 |
| **TC-ACC-005-A** | Req 1.3 | Order history pagination | `GET /api/v1/user/orders?page=2&limit=10` | Authenticated user JWT with 25 past orders | HTTP 200 OK; payload returns exactly 10 order records with correct total page count metadata | QA Eng 1 |
| **TC-CAT-001-A** | Req 2.1 | Faceted product search against index | `GET /api/v1/catalog/search?category=blazers&brand=atelier&size=M` | URL query params executed against Elasticsearch cluster | HTTP 200 OK; only products matching all 3 filter criteria returned; response time < 200ms | QA Eng 2 |
| **TC-CAT-002-A** | Req 2.1 | Typo tolerance and fuzzy search fallback | `GET /api/v1/catalog/search?q=vntage+jaket` | Misspelled search tokens | HTTP 200 OK; fuzzy match suggests "vintage jacket"; returns relevant items; zero empty results | QA Eng 2 |
| **TC-CAT-005-A** | Req 2.3 | Personalized recommendation scoring | `GET /api/v1/recommendations/user` | User JWT with past viewing history: 5 outerwear items | HTTP 200 OK; returns items scored by affinity vector for category "outerwear" and designer affinity | QA Eng 2 |
| **TC-CRT-002-A** | Req 3.1 | Guest cart session migration upon login | `POST /api/v1/cart/merge` | Header: User JWT, Body: `{ guestCartSessionId: "uuid-123" }` | HTTP 200 OK; guest items consolidated into database user cart; duplicate SKU quantities merged | QA Eng 2 |
| **TC-CRT-005-A** | Req 3.3 | Dynamic cart price update reconciliation | `GET /api/v1/cart` | Cart contains SKU whose catalog price dropped from $120 to $100 | HTTP 200 OK; cart total reflects updated $100 price; response contains `priceChangedAlert: true` | QA Eng 2 |
| **TC-CHK-003-A** | Req 4.2 | Payment gateway decline error handling | `POST /api/v1/orders/checkout` | Payment payload using Stripe decline token (`card_declined`) | HTTP 402 Payment Required; non-technical error returned; order remains in `UNPAID` status | QA Eng 3 |
| **TC-CHK-005-A** | Req 4.3 | Asynchronous order confirmation event | Message Queue (`RabbitMQ` / `Kafka`) | Event emitted: `order.created` with `{ orderId: "#SH-98241" }` | Notification worker consumes event and dispatches email via SendGrid sandbox within 5s | QA Eng 3 |
| **TC-SEL-001-A** | Req 5.1 | Product listing creation with image upload | `POST /api/v1/seller/products` | Multipart form-data with variant SKUs, prices, WebP images | HTTP 201 Created; images processed to CDN; listing records written to relational catalog DB | QA Eng 2 |
| **TC-SEL-002-A** | Req 5.2 | Low stock automated alert trigger | `POST /api/v1/inventory/decrement` | Product inventory decremented from 3 units to 2 units | Alert daemon triggers; generates low stock badge and dispatches automated restock notification email | QA Eng 2 |
| **TC-SEL-004-A** | Req 5.3 | IDOR & RBAC cross-seller security | `GET /api/v1/seller/orders/999` | Seller A JWT attempting to view Order #999 owned by Seller B | HTTP 403 Forbidden or 404 Not Found; zero customer or financial data leaked | QA Eng 3 |
| **TC-SUP-001-A** | Req 6.1 | Real-time Live Chat WebSocket exchange | `WS /api/v1/chat/ws` | Client handshake with JWT; transmits message payload | Connection established; bidirectional message delivered to agent dashboard in < 500ms | QA Eng 1 |

### 3.2 Non-Functional, Concurrency & Security Edge Scenarios

| Edge ID | Scenario Title | Target Vector | Test Methodology | Expected Result | Assigned Engineer |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SEC-01** | **Inventory Race Condition (Double Spend)** | Stock Locking Engine | `k6` script sends 50 concurrent `POST /checkout` requests for 1 remaining item | Exactly 1 transaction succeeds (HTTP 201); 49 requests receive HTTP 409 Conflict; stock never drops below 0 | QA Eng 3 |
| **SEC-02** | **Payment Webhook Loss & Network Recovery** | Stripe Webhook Listener | Drop browser connection post-3DS; send raw webhook `payment_intent.succeeded` | Backend fulfills order idempotently; order status transitions to `PAID` without browser redirect | QA Eng 3 |
| **SEC-03** | **IDOR & Authorization Fuzzing** | Seller & Order Endpoints | Automated OWASP ZAP script fuzzing user/order IDs across authorization barriers | All cross-tenant access attempts return HTTP 403/404; zero PII exposed | QA Eng 3 |
| **SEC-04** | **WebSocket Reconnection & Message Replay** | Live Chat Connection | Disconnect network socket for 15s; queue 2 client messages; restore connection | Socket automatically re-authenticates; flushes queued messages; reconciles conversation state | QA Eng 1 |
| **SEC-05** | **XSS Injection in Reviews & Seller Notes** | Review Submission API | Submitting `<script>fetch('http://evil.com')</script>` in product review body | Payload is HTML-encoded on ingestion; rendered harmlessly as plaintext text in browser | QA Eng 2 |

---

## SECTION 4: END-TO-END (E2E) TESTS LAYER
* **Shift-Left Focus:** Reserved strictly for high-value Golden User Journeys and cross-domain third-party interactions.  
* **Target Execution Speed:** `~45s - 2 minutes` per test flow.  
* **Recommended Frameworks:** `Playwright E2E Runner` (Chromium, WebKit, Firefox)  
* **Execution Gate:** Merge to `main`, Nightly regression runs, and Release Candidate sign-offs.

| Test Case ID | Req Ref | Golden Flow Name | Complete User Journey & Interaction | Browser Assertion & Verification Points | Assigned Engineer |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-ACC-002-E** | Req 1.1 | Social OAuth Login (Google & Apple) | User on login modal -> Clicks "Continue with Google" -> Browser navigates to Google consent -> User approves -> Callback to Style Haven | Browser receives OAuth callback; establishes authenticated session cookie; navbar updates to user avatar | QA Eng 1 |
| **TC-CRT-001-E** | Req 3.1 | Add to Cart & Mini-Cart Flyout Flow | Browse to PDP -> Select Size "M" + Color "Black" -> Click "Add to Cart" | Mini-cart drawer flies out from right side; line item reflects correct SKU and $120.00; cart badge updates from 0 to 1 | QA Eng 2 |
| **TC-CHK-002-E** | Req 4.2 | **Master Golden Shopper Checkout** | Cart -> Proceed to Checkout -> Confirm default shipping address -> Choose Express Shipping -> Input Card -> Solve 3DS OTP iframe -> Place Order | Payment captures; browser redirects to `/order-success/{orderId}`; order badge increments in Order History; cart resets to 0 | QA Eng 3 |
| **TC-CHK-004-E** | Req 4.2 | Digital Wallet Transaction (Apple Pay / Google Pay) | User selects "Apple Pay" on checkout -> Web Payment sheet displays -> Biometric authentication completed | Order creates seamlessly without manual shipping address input; auth token validates on backend | QA Eng 3 |
| **TC-SEL-003-E** | Req 5.3 | Seller Order Fulfillment & Label Generation | Seller logs into dashboard -> Navigates to Unfulfilled Orders -> Inputs parcel weight -> Clicks "Generate Label" | Carrier API returns tracking number; order transitions to `SHIPPED`; printable shipping label PDF renders in browser | QA Eng 3 |

---

## SECTION 5: MASTER SUMMARY & EXECUTION CADENCE

| Section | Pyramid Layer | Total Test Scenarios | Proportion | Average Speed | CI/CD Pipeline Stage |
| :---: | :--- | :---: | :---: | :--- | :--- |
| **Section 1** | **Unit Tests** | **6** | ~18% | < 1 second | Pre-commit hook / Local IDE save |
| **Section 2** | **Component Tests** | **7** | ~21% | ~15 seconds | Every Pull Request build |
| **Section 3** | **Integration & API Tests** | **15 (+5 Edge)** | ~46% | ~45 seconds | Every Pull Request build |
| **Section 4** | **End-to-End (E2E) Tests** | **5** | ~15% | ~2 minutes | Nightly / Production Release Gate |
| **TOTAL** | **Full Quality Stack** | **33 Scenarios** | **100%** | **< 3.5 minutes total** | Continuous Shift-Left Quality Gate |
