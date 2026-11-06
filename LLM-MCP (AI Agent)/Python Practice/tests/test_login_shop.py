from playwright.sync_api import Page

from tests.pages.login_page import LoginPage
from tests.pages.shop_page import ShopPage


def test_valid_login_displays_iphone_x(page: Page) -> None:
    login_page = LoginPage(page)
    login_page.open()
    login_page.sign_in("rahulshettyacademy", "Learning@830$3mK2")

    shop_page = ShopPage(page)
    shop_page.wait_until_loaded()

    assert page.url == ShopPage.URL
    assert shop_page.iphone_x_product.is_visible()
