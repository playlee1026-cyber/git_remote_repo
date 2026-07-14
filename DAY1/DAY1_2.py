# 상속에 대해서 공부해보자
class BasePage:
    def __init__(self):
        # 모든 페이지가 공통으로 가질 기본 정보
        self.browser_name = "Chrome"

    def open_browser(self):
        print(f"[{self.browser_name}] 브라우저를 엽니다.")

    def take_screenshot(self):
        print("현재 화면의 스크린샷을 저장합니다.")


# 괄호 안에 BasePage를 넣어서 상속을 받습니다!
class CartPage(BasePage):
    def __init__(self):
        # ⚠️ 중요: 부모 클래스의 __init__도 같이 실행해 달라고 컴퓨터에 알려줍니다.
        super().__init__() 
        
        # 장바구니 페이지만의 고유한 정보들만 적어줍니다.
        self.url = "https://example.com/cart"
        self.delete_btn = "delete-button"

    # 장바구니 페이지만의 고유한 행동들
    def delete_item(self):
        print(f'{self.delete_btn} 버튼을 클릭하여 상품을 삭제합니다.')



# # 장바구니 객체 생성
# cart = CartPage()

# # 1. CartPage에는 안 적었지만, 부모(BasePage)에게 물려받은 함수를 바로 쓸 수 있습니다!
# cart.open_browser()      # 출력: [Chrome] 브라우저를 엽니다.

# # 2. 물론 CartPage 본인의 고유한 함수도 잘 작동합니다.
# cart.delete_item()       # 출력: delete-button 버튼을 클릭하여 상품을 삭제합니다.

# # 3. 부모가 가진 또 다른 공통 기능도 호출 가능합니다.
# cart.take_screenshot()   # 출력: 현재 화면의 스크린샷을 저장합니다.


# ✍️ [미션 1] LoginPage도 BasePage를 상속받도록 괄호 안을 채워보세요.
class LoginPage(BasePage):
    def __init__(self):
        super().__init__()
        # 로그인의 고유한 변수 세팅
        self.login_btn = "login-button"

    # 로그인의 고유한 함수
    def login(self):
        print(f"{self.login_btn}을 눌러 로그인을 시도합니다.")

# ----------------------------------------
# 실행 테스트
# ----------------------------------------
login_page = LoginPage()

# ✍️ [미션 2] 로그인 페이지를 열기 위해 부모에게 물려받은 '브라우저 열기' 함수를 호출해 보세요!
login_page.open_browser()

# 로그인 하기
login_page.login()