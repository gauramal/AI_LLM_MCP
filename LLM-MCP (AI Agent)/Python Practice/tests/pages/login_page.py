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
