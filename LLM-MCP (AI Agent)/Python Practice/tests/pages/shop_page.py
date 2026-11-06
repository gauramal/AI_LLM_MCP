from playwright.sync_api import Page


class ShopPage:
    URL = "https://rahulshettyacademy.com/angularpractice/shop"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.iphone_x_product = page.get_by_role("link", name="iphone X", exact=True)

    def wait_until_loaded(self) -> None:
        self.page.wait_for_url(self.URL)
