from playwright.sync_api import Page, expect

class AutomationExerciseSignupDetailsPage:
    def __init__(self, page: Page):
        self.page = page
        self.form_title = page.locator("b:has-text('Enter Account Information')")
        self.gender_mr_radio = page.locator("#id_gender1")
        self.password_input = page.locator("#password")
        self.days_dropdown = page.locator("#days")
        self.months_dropdown = page.locator("#months")
        self.years_dropdown = page.locator("#years")
        self.newsletter_checkbox = page.locator("#newsletter")
        self.optin_checkbox = page.locator("#optin")
        self.first_name_input = page.locator("#first_name")
        self.last_name_input = page.locator("#last_name")
        self.company_input = page.locator("#company")
        self.address1_input = page.locator("#address1")
        self.address2_input = page.locator("#address2")
        self.country_dropdown = page.locator("#country")
        self.state_input = page.locator("#state")
        self.city_input = page.locator("#city")
        self.zipcode_input = page.locator("#zipcode")
        self.mobile_number_input = page.locator("#mobile_number")
        self.create_account_button = page.locator("button[data-qa='create-account']")

    def verify_account_information_form_is_visible(self) -> None:
        """Step 8: 상세 정보 입력 폼이 나타났는지 검증합니다."""
        expect(self.form_title).to_be_visible()

    def fill_account_details_and_submit(self, user_data: dict) -> None:
        """Step 9 ~ 13: 파라미터화된 딕셔너리 데이터를 받아 폼을 채우고 제출합니다."""
        if user_data["title"] == "Mr.":
            self.gender_mr_radio.check()
            
        self.password_input.fill(user_data["password"])
        self.days_dropdown.select_option(user_data["birth_day"])
        self.months_dropdown.select_option(user_data["birth_month"])
        self.years_dropdown.select_option(user_data["birth_year"])
        
        self.newsletter_checkbox.check()
        self.optin_checkbox.check()
        
        self.first_name_input.fill(user_data["first_name"])
        self.last_name_input.fill(user_data["last_name"])
        self.company_input.fill(user_data["company"])
        self.address1_input.fill(user_data["address1"])
        self.address2_input.fill(user_data["address2"])
        self.country_dropdown.select_option(user_data["country"])
        self.state_input.fill(user_data["state"])
        self.city_input.fill(user_data["city"])
        self.zipcode_input.fill(user_data["zipcode"])
        self.mobile_number_input.fill(user_data["mobile_number"])
        
        self.create_account_button.click()