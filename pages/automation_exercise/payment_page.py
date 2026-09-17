from playwright.sync_api import Page, expect

class AutomationExercisePaymentPage:
    NAME_ON_CARD_INPUT_LOCATOR = "input[data-qa='name-on-card']"
    CARD_NUMBER_INPUT_LOCATOR = "input[data-qa='card-number']"
    CVC_INPUT_LOCATOR = "input[data-qa='cvc']"
    EXPIRATION_MONTH_INPUT_LOCATOR = "input[data-qa='expiry-month']"
    EXPIRATION_YEAR_INPUT_LOCATOR = "input[data-qa='expiry-year']"
    PAY_AND_CONFIRM_BUTTON_LOCATOR = "button[data-qa='pay-button']"

    def __init__(self, page: Page):
        self.page = page

    def enter_payment_details_and_confirm(self, payment_data: dict) -> None:
        self.page.fill(self.NAME_ON_CARD_INPUT_LOCATOR, payment_data["name_on_card"])
        self.page.fill(self.CARD_NUMBER_INPUT_LOCATOR, payment_data["card_number"])
        self.page.fill(self.CVC_INPUT_LOCATOR, payment_data["cvc"])
        self.page.fill(self.EXPIRATION_MONTH_INPUT_LOCATOR, payment_data["expiration_month"])
        self.page.fill(self.EXPIRATION_YEAR_INPUT_LOCATOR, payment_data["expiration_year"])
        self.page.click(self.PAY_AND_CONFIRM_BUTTON_LOCATOR)