---
name: playwright-python-pom
description: Python Playwright E2E test automation standards with Page Object Model (POM) — locator strategy, fixtures, assertions, page classes, and anti-patterns. Use when writing, refactoring, or reviewing Python Playwright tests.
---

# Python Playwright & Page Object Model (POM) Standards

## Overview
This skill provides conventions and patterns for authoring end-to-end tests using Python, `pytest-playwright`, and the Page Object Model (POM) within the `LLM-MCP (AI Agent)` project.

---

## 1. Test Suite Configuration
- **Root Directory**: `Python Practice/`
- **Config**: `pytest.ini` (`testpaths = tests`, `addopts = --browser chromium --headed`)
- **Dependencies**: `requirements-test.txt` (`pytest>=8.0`, `pytest-playwright>=0.5.0`)

---

## 2. Page Object Model (POM) Structure

### Page Class Pattern
Store all page classes under `Python Practice/tests/pages/<page_name>.py`.
- Define the target page URL as a class attribute `URL`.
- Initialize element locators in `__init__(self, page: Page)`.
- Implement user action methods that operate on those locators.
- Do NOT place `assert` statements inside page classes; keep assertions in test functions.

```python
from playwright.sync_api import Page

class LoginPage:
    URL = "https://rahulshettyacademy.com/loginpagePractise/"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.username = page.get_by_role("textbox", name="Username:")
        self.password = page.get_by_role("textbox", name="Password:")
        self.terms_checkbox = page.get_by_role(
            "checkbox", name="I Agree to the terms and conditions"
        )
        self.sign_in_button = page.get_by_role("button", name="Sign In")

    def open(self) -> None:
        self.page.goto(self.URL)

    def sign_in(self, username: str, password: str) -> None:
        self.username.fill(username)
        self.password.fill(password)
        self.terms_checkbox.check()
        self.sign_in_button.click()
```

---

## 3. Test File Pattern
Store tests under `Python Practice/tests/test_<feature>.py`.
- Inject the Playwright `page: Page` fixture.
- Instantiate necessary page objects.
- Perform actions via page methods.
- Assert final states and visibility.

```python
from playwright.sync_api import Page
from tests.pages.login_page import LoginPage
from tests.pages.shop_page import ShopPage

def test_valid_login_displays_iphone_x(page: Page) -> None:
    # 1. Arrange & Act
    login_page = LoginPage(page)
    login_page.open()
    login_page.sign_in("rahulshettyacademy", "Learning@830$3mK2")

    # 2. Wait for transition
    shop_page = ShopPage(page)
    shop_page.wait_until_loaded()

    # 3. Assert
    assert page.url == ShopPage.URL
    assert shop_page.iphone_x_product.is_visible()
```

---

## 4. Locator Strategy (Priority Order)

1. **Role Locators (Preferred)**:
   ```python
   page.get_by_role("button", name="Sign In")
   page.get_by_role("textbox", name="Username:")
   page.get_by_role("link", name="iphone X", exact=True)
   ```
2. **Label / Placeholder Locators**:
   ```python
   page.get_by_label("Username:")
   page.get_by_placeholder("Username")
   ```
3. **Text Locators**:
   ```python
   page.get_by_text("Incorrect username/password.")
   ```
4. **Stable IDs**:
   ```python
   page.locator("#signInBtn")
   ```

### Anti-Patterns to Avoid:
- ❌ Never use `time.sleep()`. Use Playwright's built-in auto-waiting or `page.wait_for_url()`.
- ❌ Avoid fragile XPath or long CSS selector chains (`div > table > tr:nth-child(2) > td`).
- ❌ Do not hardcode test assertions inside Page Object methods.
