from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str, wait_until="networkidle"):
        self.page.goto(url, wait_until=wait_until)

    def wait_for_url(self, url: str, timeout=15000):
        expect(self.page).to_have_url(url, timeout=timeout)