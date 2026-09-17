 # Playwright UI E2E Pipeline QA Automation Framework

프론트엔드(Playwright UI), 백엔드(Flask API), 인프라 배포(Render + GitHub Actions)를 하나의 파이프라인으로 연결한 **모듈형 다계층(Multi-Layer) 자동화 테스트 프레임워크**입니다.

테스트 케이스 유지보수성과 안정성 확보를 위해 다음을 적용했습니다:
- **POM(Page Object Model) 패턴**: `pages/base_page.py`를 상속하는 구조로 UI 요소와 테스트 로직을 분리
- **데이터 주도 테스트(DDT)**: 회원가입·결제·게시판 API 테스트 케이스를 CSV로 분리하고 Pandas로 동적 파싱하여 하드코딩 없이 대량 검증
- **Flaky Test 방지 장치**: 광고 네트워크 요청 차단(`conftest.py`), 타임아웃 값 중앙화(`config/settings.py`)로 UI 테스트의 불안정성을 최소화

단순 정상 흐름(Happy Path) 검증에 그치지 않고, 실제 서비스에서 발생 가능한 **보안·금융 엣지케이스**까지 다룹니다:
- 관리자 페이지 무단 접근 차단 등 **RBAC 권한 제어** 검증
- 인증 토큰 누락/만료, 타 계정 권한 우회, 결제 한도 초과, 중복 트랜잭션, **자금세탁방지(AML) 한도 초과** 등 결제 API 방어 로직 검증

CI/CD 파이프라인은 매일 자정(KST) 정기 회귀 테스트 외에도 **테스트 대상(전체/API/UI/스모크) 수동 선택 실행**, Render 콜드 스타트 방지를 위한 **서버 Wake-up**, 테스트 성공 시 **자동 재배포**, 실패 시 **Slack 실시간 알림**(UI는 스크린샷 포함, API는 로그만)까지 포함합니다.

**Author:** 지원자 이진행

## 🏗️ System Architecture
![Architecture](./System_Architecture.png)

본 프레임워크는 독립적인 5개의 계층(Layer)으로 구성되어 동작합니다.

### 1. API Data-Driven Testing (DDT) Layer
* **Tech Stack:** PyTest, Requests, Pandas
* **Description:** 비즈니스 로직과 테스트 데이터를 완벽하게 분리했습니다. 하드코딩을 배제하고 CSV 포맷의 데이터를 Pandas로 파싱하여 대량의 API(회원가입, 결제, 게시판 등) 엔드포인트를 동적으로 반복 검증합니다.

### 2. Web E2E UI Testing Layer
* **Tech Stack:** Playwright, PyTest
* **Description:** DOM 구조 변경에 유연하게 대응하기 위해 POM(Page Object Model) 패턴을 엄격하게 적용했습니다. 브라우저의 명시적 대기(Wait)와 예외 처리 로직을 중앙화하고, 광고 네트워크 요청을 컨텍스트 단에서 차단하는 픽스처를 두어 UI 테스트 특유의 불안정성(Flaky)을 최소화했습니다.

### 3. Security & Exception Handling Validation Layer
* **Tech Stack:** Playwright Network Interception, Flask RBAC
* **Description:** 정상 흐름(Happy Path) 검증을 넘어, 실제 서비스에서 발생 가능한 보안·금융 엣지케이스를 방어 로직 레벨에서 검증합니다. 일반 사용자의 관리자 페이지 강제 접근 차단(RBAC), 인증 토큰 누락/만료, 타 계정 권한 우회 시도, 결제 한도 초과 및 중복 트랜잭션 방어, 자금세탁방지(AML) 한도 초과 시나리오(네트워크 인터셉트 기반 목킹)를 포함합니다.

### 4. CI/CD & Notification Layer
* **Tech Stack:** GitHub Actions, Slack SDK/Webhook, Gunicorn, Pytest-html
* **Description:** 매일 자정(KST) 회귀 테스트가 자동 수행되며, `workflow_dispatch`를 통해 전체/API/UI/스모크(`-m smoke`) 단위로 원하는 테스트만 수동 실행할 수도 있습니다. Render 무료 플랜의 콜드 스타트 문제를 고려해 테스트 실행 전 서버를 미리 깨우는(Wake-up) 단계를 두었고, 테스트 성공 시 Render 재배포를 트리거합니다. 테스트 실패 시 UI 테스트는 스크린샷과 함께, API 테스트는 로그만 별도로 Slack Bot을 통해 실시간 전송됩니다.

### 5. AI Vision Validation Layer (Upcoming)
* **Tech Stack:** YOLO, OpenCV
* **Description:** DOM 트리에 잡히지 않는 특수 렌더링 영역이나 캔버스를 검증하기 위해, 커스텀 객체 탐지 모델을 추론 파이프라인에 통합하는 시각적 회귀 테스트(VRT) 계층을 준비 중입니다.


## 🏷️ Test Markers
도메인/유형별로 테스트를 태깅하여 선택적 실행이 가능합니다.

| Marker | 설명 |
|---|---|
| `api` | 백엔드 API 응답 및 비즈니스 로직 검증 |
| `ui` | Playwright 기반 UI E2E 테스트 |
| `security` | 보안 및 권한(RBAC) 접근 관련 테스트 |
| `registration` | 회원가입 및 계정 생성 플로우 |
| `login` | 로그인/로그아웃 플로우 |
| `products` | 상품 탐색 및 장바구니 |
| `checkout` | 체크아웃 전체 플로우 (배송지~결제 완료) |

예: `pytest -m security` 로 보안 테스트만 선택 실행 가능

---

## 📂 Directory Structure
📦 automation-framework
 ┣ 📂 .github/workflows   # CI/CD 파이프라인 (playwright.yml) - 수동 타겟 선택, Render Wake-up/재배포 포함
 ┣ 📂 config              # 전역 환경 변수 및 설정 중앙화 (settings.py)
 ┣ 📂 data                # API 테스트용 CSV 데이터셋
 ┣ 📂 pages               # 웹 UI 도메인별 페이지 객체 (POM)
 ┣ 📂 tests               # 실제 구동되는 테스트 스크립트 모음
 ┃ ┣ 📂 api               # API DDT 검증 스크립트
 ┃ ┗ 📂 ui                # Playwright 기반 E2E 검증 스크립트 (회원가입/로그인/장바구니/체크아웃/RBAC/결제 예외)
 ┣ 📂 utils               # API 래퍼, Pandas 파싱, Slack 알림 헬퍼 모듈
 ┣ 📜 app.py               # Flask 목업 서버 (Render 배포, 로그인/RBAC/결제/게시판 API)
 ┣ 📜 conftest.py          # PyTest 전역 픽스처 (Slack 알림, 광고 네트워크 차단 등)
 ┗ 📜 requirements.txt     # 의존성 패키지 명세 (Flask, Gunicorn 등 배포 스택 포함)