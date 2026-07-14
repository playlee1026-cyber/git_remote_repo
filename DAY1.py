# 클래스에 대해서 알아보자
# 클래스 => 과자틀같은 설계도
# 과자 틀 (클래스) / 과자 (객체)

# 부모 클래스
class Fourcal:
    # init?? => 처음 실행 하는 설계도 (예약어)
    # 맨앞에 쓰는게 규칙 (생성자 개념으로 딱 한번만 사용)
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def setdata(self, first, second):
        self.first = first
        self.second = second

    def add(self):
        result = self.first + self.second
        return result
    
# 부모에게 상속받은 클래스
# 리소스를 효율적으로 사용하기 위해서 사용
class MoreFourCal(Fourcal):
    def pow(self):
        result = self.first ** self.second
        return result
    
    def div(self):
        result = self.first // self.second
        return result

# 메서드 오버라이딩
# div 함수 재생성 (코드 사용시 자식이 우선 사용)
# 자식 함수가 부모 함수를 덮어씌운것임
class safeFourCal(Fourcal):
    def div(self):
        if self.second == 0 :
            return 0
        else : 
            return self.first / self.second

a = safeFourCal(4,0)
#a = Fourcal(4,0)
#print(a.div())

# 클래스 자체에서 변경해서 바꿀 수 있음
# 공통으로 쓸때는 클래스 변수를 변경
class Family:
    lastname = '이'

#설계도를 호출하여 변경하는 원리 
Family.lastname = '박'
print(Family.lastname)

a = Family()
b = Family()

print(a.lastname)
print(b.lastname)
