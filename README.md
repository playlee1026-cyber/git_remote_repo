# Playwright UI E2E Pipeline QA Automation Framework

단순한 스크립트 나열을 넘어, 프론트엔드부터 백엔드, 그리고 인프라 배포까지 유기적으로 연결된 **모듈형 다계층(Multi-Layer) 자동화 테스트 프레임워크**입니다. 
테스트 케이스 유지보수의 어려움과 UI 변경에 따른 취약성(Flaky Test)을 극복하기 위해 **POM(Page Object Model) 패턴**과 **데이터 주도 테스트(DDT)** 방법론을 결합하여 설계했습니다.

**Author:** 지원자 이진행

## 🏗️ System Architecture
*(여기에 Draw.io 등으로 작성한 시스템 아키텍처 다이어그램 이미지를 추가하세요. 예: `![Architecture](./docs/architecture.png)`)*

본 프레임워크는 독립적인 4개의 계층(Layer)으로 구성되어 동작합니다.

### 1. API Data-Driven Testing (DDT) Layer
* **Tech Stack:** PyTest, Requests, Pandas
* **Description:** 비즈니스 로직과 테스트 데이터를 완벽하게 분리했습니다. 하드코딩을 배제하고 CSV 포맷의 데이터를 Pandas로 파싱하여 대량의 API(회원가입, 결제, 게시판 등) 엔드포인트를 동적으로 반복 검증합니다.

### 2. Web E2E UI Testing Layer
* **Tech Stack:** Playwright, PyTest
* **Description:** DOM 구조 변경에 유연하게 대응하기 위해 POM(Page Object Model) 패턴을 엄격하게 적용했습니다. 브라우저의 명시적 대기(Wait)와 예외 처리 로직을 중앙화하여 UI 테스트 특유의 불안정성을 최소화했습니다.

### 3. CI/CD & Notification Layer
* **Tech Stack:** GitHub Actions, Slack Webhook, Pytest-html
* **Description:** 클라우드 환경에서 매일 자정 회귀 테스트(Regression Test)가 자동으로 수행됩니다. 테스트 실패 시 네트워크 트레이스, 스크린샷과 함께 HTML 리포트 링크가 포함된 리치 메시지를 Slack으로 실시간 발송하여 즉각적인 이슈 트래킹이 가능합니다.

### 4. AI Vision Validation Layer (Upcoming)
* **Tech Stack:** YOLO, OpenCV
* **Description:** DOM 트리에 잡히지 않는 특수 렌더링 영역이나 캔버스를 검증하기 위해, 커스텀 객체 탐지 모델을 추론 파이프라인에 통합하는 시각적 회귀 테스트(VRT) 계층을 준비 중입니다.

---

## 📂 Directory Structure

```text
📦 automation-framework
 ┣ 📂 .github/workflows   # CI/CD 파이프라인 (playwright.yml)
 ┣ 📂 config              # 전역 환경 변수 및 설정 중앙화 (settings.py)
 ┣ 📂 data                # API 테스트용 CSV 데이터셋
 ┣ 📂 pages               # 웹 UI 도메인별 페이지 객체 (POM)
 ┣ 📂 tests               # 실제 구동되는 테스트 스크립트 모음
 ┃ ┣ 📂 api               # API DDT 검증 스크립트
 ┃ ┗ 📂 ui                # Playwright 기반 E2E 검증 스크립트
 ┣ 📂 utils               # API 래퍼, Pandas 파싱 등 헬퍼 모듈
 ┣ 📜 conftest.py         # PyTest 전역 픽스처
 ┗ 📜 requirements.txt    # 의존성 패키지 명세