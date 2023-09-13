# migong backend

얼굴형을 분석해주고 자신의 미를 찾아나가는 서비스의 백엔드 로직을 담당합니다

## Get started

### environment setting

```
python3 -m venv venv
source venv/bin/activate
```

### package install

```
pip install -r requirements.txt
```

### server start

```
python manage.py makemigrations
python3 manage.py migrate
python manage.py createsuperuser
python3 manage.py runserver
```

## face 분석 방법

### 기본 플로우

1. kaggle에 있는데 데이터셋을 준비
2. 각 부위인 광대(cheek), 턱(jaw), 가로세로 비율(her_ver_ratio)에 해당하여 주어진 함수에 대입하여 각 부위별 중앙값과 최대값을 구함
3. 0을 0%, 중앙값을 50%, 최대값을 100%로 설정하여 각 점을 잇는 그래프 생성
4. 유저의 사진을 입력하면 주어진 함수에 대하여 값을 구하여 각 그래프에 대입하여 자신의 위치한 백분율을 획득

### 얼굴형 분석

- 전제: 간단하게 구하기 위해 엄청난 비약과 과정이 필요하다, 추후에 알고리즘을 고도화하기 위해서는 더 많은 점을 획득할 수 있는 1) media pipe 라이브러리를 사용하고 2)딥러닝을 사용하여 다양한 악변수에도 대응할 수 있어야할 것이다.

- 원리: 광대와 턱은 대략적으로 광대나 턱을 지칭할 수 있는 위치의 4개의 삼각형의 좌표를 구하면 넓이와 높이를 구할 수 있다. 이를 나누면 너비에 대한 비율값이 나오고 우리는 이를 광대와 턱의 크기라고 지칭할 것이다. 가로 세로 비율은 말그대로 가로길이와 세로길이(눈썹 가운데와 턱 사이 거리)를 구하여 나누어 구한다.

- 아래 그림에서 파란색 삼각형이 광대, 오렌지 삼각형이 턱, 녹색 선이 가로 세로선을 의미한다.
![face](https://github.com/mi-gongan/migong_backend/assets/97350083/745d7d3a-1360-49a7-8443-7f69272d9476)

### 백분율 획득


데이터셋에 위 스크립트를 돌리면 아래와 같은 중앙값과 최대값이 나온다.

1. 광대

- 중앙값: 8
- 최댓값: 13

2. 턱

- 중앙값: 3
- 최대값: 11

3. 가로세로 비율

- 중앙값: 0.9
- 최대값: 1.1

-> 아래는 해당 그래프를 나타낸다

<img width="968" alt="스크린샷 2023-09-13 23 56 39" src="https://github.com/mi-gongan/migong_backend/assets/97350083/583a3542-8bdd-4503-ad2a-cd124c417078">
<img width="413" alt="스크린샷 2023-09-13 23 45 54" src="https://github.com/mi-gongan/migong_backend/assets/97350083/c60961a2-e376-4551-bcd6-e799597c1996">

