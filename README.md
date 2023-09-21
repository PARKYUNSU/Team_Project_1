<br>

 ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
 ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
 ![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
 ![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
 ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
 
 ![bootstrap](https://img.shields.io/badge/bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
 ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
 ![looker](https://img.shields.io/badge/looker-4285F4?style=for-the-badge&logo=looker&logoColor=white)
 ![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

<br>

# P향저격
머신러닝을 활용한 여행경비 예측

## 프로젝트 개요
이 프로젝트는 여행자들을 위한 여행 경비 예측 솔루션을 개발하는 것을 목표로 합니다. Python을 사용하여 데이터 수집, EDA, 머신러닝 모델링 및 Flask 앱 배포를 통해 이를 구현하였습니다. 또한 Looker Studio를 사용하여 대시보드를 생성하여 사용자에게 직관적인 정보를 제공합니다.

## 주요 기술 및 라이브러리
- 주요 언어: Python
- 데이터 수집: Selenium, Scrapy
- 데이터 분석 및 머신러닝: Pandas, Scikit-Learn, Xgboost, Catboost
- 웹 개발: Flask, Bootstrap
- 대시보드 생성: Looker Studio

## 팀원 및 역할
| name | Role | 
| ---- | ---- |
|한주호| 데이터 크롤링, FLASK, 웹페이지 제작|
|박윤수| 데이터 크롤링, EDA, 모델링, 피클링, git 관리|
|정지현| 데이터 크롤링, EDA, 모델링, 피클링|
|조재현| 데이터 크롤링, EDA, 모델링, 피클링|
|김소연| 데이터 크롤링, EDA, 대시보드|

## 프로젝트 세부 내용

### 프로젝트 도식화
![도식화](/Users/parkyunsu/Downloads/스크린샷 2023-09-21 오후 6.06.03.png)


1. **데이터 수집**: Selenium 및 Scrapy를 사용하여 여행 관련 데이터를 크롤링하였습니다.<br>
   a. 항공권<br>

   - 데이터 출처 : 네이버 항공권 (https://flight.naver.com/)<br>
   - 데이터 형태 : (43449, 11)<br>
   - 검색 기간 : 2023.08.01 - 2023.10.31<br>
   - 검색 도구 : Selenium<br>
   
   b. 호텔<br>

   - 데이터 출처 : 여기어때 (https://www.goodchoice.kr/)<br>
   - 데이터 형태 : (13751, 13)<br>
   - 검색 기간 : 2023.08.01 - 2023.10.31<br>
   - 검색 도구 : Scrapy<br>
   
   c. 렌트카<br>

   - 데이터 출처 : 제주속으로 (https://jejussok.com/rent/rent.php?co=rent)
   - 데이터 형태 : (13751, 13)<br>
   - 검색 기간 : 2023.08.01 - 2023.10.23 [크롤링 당일 23일이 마지막데이터]<br>
   - 검색 도구 : Selenium<br>

3. **데이터 분석 및 전처리**: 크롤링한 데이터를 Pandas를 활용하여 탐색적 데이터 분석(EDA)을 수행하였습니다. 데이터 전처리를 통해 모델링에 사용할 준비를 마쳤습니다.

ㅁㄴㅇ

4. **머신러닝 모델링**: 여행 경비를 예측하기 위한 머신러닝 모델을 구축하였습니다. Scikit-Learn 라이브러리를 사용하여 모델 학습 및 평가를 진행하였습니다.

5. **Flask 웹 애플리케이션**: 머신러닝 모델을 Flask를 사용하여 웹 애플리케이션으로 개발하였습니다. 사용자는 여기에서 여행 경비를 예측하고 결과를 확인할 수 있습니다.

6. **Looker Studio 대시보드**: Looker Studio를 활용하여 사용자에게 직관적인 대시보드를 제공하였습니다. 시각화를 통해 여행 경비 및 예측 결과를 시각적으로 확인할 수 있습니다.

## 프로젝트 구성
프로젝트의 디렉토리 구조 및 파일 설명은 다음과 같습니다:

- `data/`: 크롤링한 데이터 및 전처리된 데이터가 저장된 디렉토리.
- `notebooks/`: Jupyter Notebook 파일들이 저장된 디렉토리로, EDA 및 모델 학습 과정이 기록되어 있습니다.
- `webapp/`: Flask 웹 애플리케이션 코드와 템플릿이 포함되어 있습니다.
- `looker_dashboard/`: Looker Studio 대시보드 관련 파일들이 저장된 디렉토리.

## 실행 가이드
프로젝트 실행을 위한 가이드:

1. 데이터 수집: `data/` 디렉토리에 크롤링한 데이터를 저장하십시오.
2. 데이터 전처리 및 모델링: `notebooks/` 디렉토리의 Jupyter Notebook을 참조하여 데이터 전처리 및 머신러닝 모델링을 진행하십시오.
3. Flask 웹 애플리케이션 실행: `webapp/` 디렉토리에서 Flask 애플리케이션을 실행하십시오.
4. Looker 대시보드: Looker Studio를 사용하여 대시보드를 설정하고 업로드하십시오.

## 기여 및 라이선스
이 프로젝트는 오픈 소스로 개발되었으며 기여를 환영합니다. 기여자는 CONTRIBUTING.md 파일을 참조하십시오. 이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 연락처
- 개발자: [Your Name]
- 이메일: [Your Email]

## 라이선스
이 프로젝트는 MIT 라이선스에 따라 배포됩니다. 자세한 내용은 [LICENSE.md](LICENSE.md) 파일을 참조하십시오.
