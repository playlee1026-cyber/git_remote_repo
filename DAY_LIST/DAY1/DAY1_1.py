class CartPage:
    # 1. 초기화 함수: 페이지의 고유한 정보(URL, 버튼 위치 등)를 세팅하세요.
    def __init__(self):
        self.url = "https://example.com/cart"
        self.item_locator = ".cart-item"        # 장바구니에 담긴 상품 요소
        self.delete_btn = "delete-button"     # 삭제 버튼
        # 💡 [도전] '주문하기 버튼'의 locator 변수를 하나 더 만들어 보세요!
        self.oder_btn = "oder_button"

    # 2. 이 페이지에서 유저가 할 수 있는 행동(함수)들을 정의하세요.
    def add_item(self, item_name = '맥북 프로'):
        print(f"{item_name}을(를) 장바구니에 추가합니다.")

    # 💡 [도전] 장바구니의 상품을 삭제하는 'delete_item' 함수를 완성해 보세요.
    def delete_item(self):
        # 여기에 self.delete_btn을 활용해서 "OO 버튼을 클릭하여 삭제합니다."라고 출력해 보세요.
        print(f'{self.delete_btn} 버튼을 클릭하여 상품을 삭제합니다.')

    # 💡 [도전] 주문을 진행하는 'proceed_to_checkout' 함수를 만들어 보세요.
    def proceed_to_checkout(self):
        print(f'{self.oder_btn} 버튼을 클릭하여 주문을 진행합니다.')

    def finish_item(self, item_name):
        print(f'{item_name}을(를) 주문에 성공했습니다.')

# 3. 실제 객체를 만들어서 함수를 실행해 보세요.
cart = CartPage()
item_name = "에어팟 프로"
cart.add_item()
cart.delete_item()
cart.add_item(item_name)
cart.proceed_to_checkout()
cart.finish_item(item_name)