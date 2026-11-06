# EventHub — Booking Management Test Strategy

**Generated**: 2026-10-26
**Scope**: Booking Management (Flow 4 — View, Cancel, Clear, Refund Eligibility)
**Input**: `docs/test-scenarios.md`
**Consumer**: `/generate-tests` skill

---

## Layer Distribution

| Layer | Count | Focus | Avg Speed |
|---|---|---|---|
| **Unit** | 5 | Pure functions — `randomRef`, `generateUniqueRef`, total price calc, refund eligibility logic | < 10 ms |
| **API / Integration** | 22 | HTTP contracts, auth middleware, business rule enforcement, FIFO pruning, error codes | ~200 ms |
| **Component** | 6 | Single-component render: skeleton, empty state, spinner, `ConfirmDialog`, `RefundEligibility` state machine | ~50 ms |
| **E2E** | 20 | Multi-page journeys, critical user flows, cross-layer flows | ~15 s |
| **Total** | **53** | | |

> **Shape**: Wide base (Unit + API = 27) — narrow top (E2E = 20). Meets the test pyramid model.

---

## Layer Assignments

### Unit Tests — 5 scenarios

Pure functions with no I/O, sourced from `bookingService.js:randomRef/generateUniqueRef` and the frontend `RefundEligibility` component logic.

| TC | Title | Rationale |
|---|---|---|
| TC-405 | Booking ref uniqueness — collision retry | Tests `generateUniqueRef` loop/fallback — pure retry logic, no HTTP needed |
| TC-408 | Booking ref prefix for digit-starting event title | Tests `randomRef(eventTitle)` edge: `'1'.toUpperCase() === '1'` — pure function |
| TC-106 | Total price = price × quantity | `totalPrice = parseFloat(event.price) * quantity` — deterministic math |
| TC-103 | Refund eligibility: qty=1 → eligible | Frontend `quantity === 1` branch — pure boolean, no API call |
| TC-104 | Refund eligibility: qty>1 → not eligible | Frontend `quantity > 1` branch — pure boolean, no API call |

---

### API / Integration Tests — 22 scenarios

HTTP contracts, auth middleware, business rules, and error codes against the live Express backend.
Routes handled by `bookingController.js`, enforced in `bookingService.js`.

| TC | Title | Endpoint | Rationale |
|---|---|---|---|
| TC-007 | Lookup booking by ref via API | `GET /api/bookings/ref/:ref` | API contract only — no UI needed |
| TC-100 | FIFO pruning — 10th booking prunes oldest (different event) | `POST /api/bookings` | DB state manipulation; pure service logic in `createBooking` |
| TC-101 | FIFO pruning — same-event fallback burns seat | `POST /api/bookings` | `sameEventFallback` path; DB read+write, no UI involvement |
| TC-107 | Bookings page max 10 per page (API pagination) | `GET /api/bookings?page=1&limit=10` | Pure API pagination response structure |
| TC-108 | Cancelling booking releases dynamic seats | `DELETE /api/bookings/:id` → `GET /api/events/:id` | Seat recompute is backend-only; no UI journey needed |
| TC-201 | Cross-user booking access returns 403 | `GET /api/bookings/:id` | HTTP status code — `getBookingById` ownership guard |
| TC-202 | Cross-user cancellation returns 403 | `DELETE /api/bookings/:id` | HTTP status code — `cancelBooking` ownership guard |
| TC-203 | Unauthenticated GET /api/bookings returns 401 | `GET /api/bookings` | Auth middleware test — no UI needed |
| TC-204 | Unauthenticated GET /api/bookings/:id returns 401 | `GET /api/bookings/:id` | Auth middleware test |
| TC-205 | Unauthenticated DELETE /api/bookings returns 401 | `DELETE /api/bookings` | Auth middleware test |
| TC-206 | Cross-user lookup by ref returns 403 | `GET /api/bookings/ref/:ref` | `getBookingByRef` ownership check |
| TC-301 | GET /api/bookings/:id with non-existent ID returns 404 | `GET /api/bookings/99999` | NotFoundError HTTP code — API layer |
| TC-302 | Create booking with insufficient seats returns 400 | `POST /api/bookings` | `InsufficientSeatsError` in `createBooking` |
| TC-303 | Create booking for non-existent event returns 404 | `POST /api/bookings` | Event lookup NotFoundError |
| TC-304 | Create booking with missing required fields returns 400 | `POST /api/bookings` | Input validator on route |
| TC-305 | quantity = 0 or negative returns 400 | `POST /api/bookings` | Input validator boundary |
| TC-306 | quantity > 10 returns 400 | `POST /api/bookings` | Input validator boundary — **do NOT test at E2E** (anti-pattern) |
| TC-307 | Double-cancel same booking returns 404 | `DELETE /api/bookings/:id` × 2 | Idempotency — pure API state check |
| TC-400 | Edge: 10th booking prunes from different event | `POST /api/bookings` | `findOldestExcluding` preference — DB verification |
| TC-401 | Edge: same-event fallback at limit | `POST /api/bookings` | `decrementSeats` side effect — DB verification |
| TC-406 | Clear all when only 1 booking exists | `DELETE /api/bookings` | Response `{ deleted: 1 }` — API contract |
| TC-407 | Pagination page 2 with partial results | `GET /api/bookings?page=2&limit=5` | API pagination cursor — no UI needed |

---

### Component Tests — 6 scenarios

Single-component rendering and UI state machines in isolation, using mocked API routes.

| TC | Title | Component | Rationale |
|---|---|---|---|
| TC-500 | Skeleton loading state while fetching | `BookingCardSkeleton` | `isLoading=true` branch — mock with route intercept |
| TC-501 | Empty state: user has no bookings | `BookingsContent` | `bookings.length === 0` branch — mock API with empty array |
| TC-502 | Detail page loading spinner | `BookingDetailPage` | `isLoading=true` spinner — isolated render with mock route |
| TC-507 | "Clear all" button shows "Clearing..." while in-flight | `BookingsContent` | `clearing` state variable — test with delayed mock route |
| TC-508 | Refund eligibility state machine: idle → checking → result | `RefundEligibility` | 3-state machine with 4s timer — use fake timers or await |
| TC-510 | Pagination UI renders when totalPages > 1 | `Pagination` (BookingsContent) | Pagination props driven by API mock — isolated render |

---

### E2E Tests — 20 scenarios

Multi-page journeys and full-stack flows. All live in `tests/booking-management.spec.js`.

| TC | Title | Why E2E |
|---|---|---|
| TC-001 | View bookings list with existing bookings | Login → book → navigate → assert card — multi-page |
| TC-002 | View single booking detail page | Login → book → list → detail — multi-page, nested data |
| TC-003 | Cancel booking from detail page | Login → book → list → detail → cancel → redirect — modal + toast |
| TC-004 | Clear all bookings | Login → book → list → clear dialog → empty state |
| TC-005 | Navigate back to bookings list | Login → detail → back button → list URL |
| TC-006 | Navigate via "View My Bookings" post-booking | Booking confirmation → link → list |
| TC-102 | Booking ref starts with event title first char | `bookingRef` readable only from UI confirmation card |
| TC-103 | Refund eligibility: qty=1 → eligible (UI) | 4s spinner requires real page interaction |
| TC-104 | Refund eligibility: qty>1 → not eligible (UI) | Timer and DOM state transition visible only at E2E |
| TC-105 | Refund eligibility spinner visible for ~4s | `#refund-spinner` visibility window — real browser timing |
| TC-106 | Total price displayed correctly in UI | Cross-check DB price with UI rendering |
| TC-109 | "Clear all" button visible when bookings exist | Conditional UI element — needs real booking data |
| TC-200 | Cross-user access shows "Access Denied" in UI | Two-user login switching → foreign booking → 403 UI state |
| TC-300 | Non-existent booking ID shows "Booking not found" | Frontend 404 empty state — browser navigation only |
| TC-402 | Booking with qty=1 (minimum) — full happy path | Quantity stepper at minimum value |
| TC-403 | Booking with qty=10 (maximum) — full happy path | Stepper clicked 9× ; button disabled at 10 — UI behavior |
| TC-404 | Refund boundary: qty=2 → non-refundable | Detail page + spinner — browser timing |
| TC-503 | Cancel booking dialog appears before deletion | ConfirmDialog from full detail page — interaction + assertion |
| TC-504 | Cancel dialog dismissed → no cancellation | Dialog dismiss path — booking persists, no API call |
| TC-509 | Booking detail shows "Access Denied" for 403 | Login switch; distinct from "Not found" — URL navigation |

---

## Defense-in-Depth: Critical Rules Tested at Multiple Layers

| Business Rule | Unit | API | E2E |
|---|---|---|---|
| Booking ref prefix = event title first char | TC-408 | — | TC-102 |
| Total price = price × qty | TC-106 | — | TC-106 |
| Refund eligibility (qty === 1) | TC-103 | — | TC-103 |
| Cross-user access = 403 | — | TC-201 | TC-200 |
| Insufficient seats → 400 | — | TC-302 | implicit in TC-402/403 |

---

## Anti-Patterns Found in Existing Tests

Reviewing `tests/booking-management.spec.js`:

| # | Anti-Pattern | Location | Severity | Fix |
|---|---|---|---|---|
| 1 | **CSS class locator** `.booking-ref` (Priority 5) | Lines 46, 48, 142 | ⚠️ Medium | Replace with `getByTestId('booking-ref')` — request `data-testid` from dev |
| 2 | **CSS class locator** `.confirm-booking-btn` | Lines 43, 138 | ⚠️ Medium | Replace with `getByRole('button', { name: /Confirm Booking/i })` |
| 3 | **CSS class locator** `span.font-mono.font-bold` for breadcrumb | Line 102 | ⚠️ Medium | Request `data-testid="booking-ref-breadcrumb"` |
| 4 | **Hardcoded BASE_URL to production** | Line 3 | 🔴 High | Use `process.env.BASE_URL ?? 'http://localhost:3000'` — running against production pollutes live data |
| 5 | **No teardown** — state cleanup only at test start | Throughout | ⚠️ Medium | Add `test.afterEach(clearBookings)` — current approach is brittle if a test errors before cleanup |
| 6 | **Repeated login+clear+book setup** across tests | Lines 156–168 | ℹ️ Low | Consolidate with `test.beforeEach` scoped to the describe block |

---

## Recommendations

1. **🔴 Immediately fix**: Change `BASE_URL` to `localhost:3000` — highest risk (Anti-pattern #4).
2. **Add `data-testid` attributes** to `.booking-ref`, `.confirm-booking-btn`, and the breadcrumb span — eliminates 3 fragile CSS locators.
3. **Add `test.afterEach(clearBookings)`** to the existing describe block for reliable state isolation.
4. **New test files to create** (for uncovered scenarios):
   - `tests/booking-security.spec.js` — TC-200, TC-201–206, TC-509
   - `tests/booking-refund.spec.js` — TC-103, TC-104, TC-105, TC-404
   - `tests/booking-fifo.spec.js` (API) — TC-100, TC-101, TC-400, TC-401
