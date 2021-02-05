# Metis Engine Project

![프로젝트 구조][1]

## 1. 로컬개발환경(Local Develop Environment)

- 엔진 개발 인력은 로컬개발환경(본인 노트북 및 개인 개발환경)에서 개발 진행
- DBeaver / SQL을 이용하여 Postgresql의 Procedure / Function 개발 진행
- VScode / Python을 이용하여 Metis Engine 기능 개발 진행
- Excel(Power Query, etc...)을 이용하여 개발한 Metis Engine 기능 테스트 진행

## 2. 원격개발환경(Remote Develop Environment)

- Gitlab, Docker 및 Kubernetes와 같은 테스트 / 배포를 위한 개발 환경을 의미
- 로컬개발환경에서 개발한 내용을 관리 / 테스트/ 배포를 위해 사용

## 3. 배포환경(Deploy Environment)

- 실제 서비스가 이루어지는 환경
- 로컬개발환경에서 개발 후 원격개발환경에서 테스트를 마친 후 자동으로 배포환경에 적용 예정

## 내용 추가 진행중
### 추가 내용

[1]: ./docs/resources/구조.png