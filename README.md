# django-script-slide
<img src="https://user-images.githubusercontent.com/49490703/94095547-ecb5b880-fe5c-11ea-9413-0f5d83aa8b61.png"  width="70%">

### 프로젝트 소개 
- 언제 어디서든 노트북과 핸드폰만 있으면, 편하게 발표할 수 있도록 도와주는 서비스
- 발표 진행상황에 맞춰 자동으로 넘어가는 대본을 보여주고 발표 남은 시간, 끊어읽기, 대본 작성시 표현 추천 등 발표에 전반적인 부분을 모두 도와주는 토탈 솔루션


### 주요기능
  - Script I/O (대본 입출력 기능 및 디자인)
  - Manual Control ( 음성인식 외 스마트폰 터치 등을 통한 대본 제어 기능)
  - Script Customization ( 발표자에 맞게 대본 텍스트를 커스터 마이징하는 기능)
  - FYI (For your information) ( 발표 시간 입력 및 남은 시간 알림 기능 )
  - PDA(Progress Detection Algorithm) (음성인식 결과 - 대본 텍스트 일치율 알고리즘)
  - STS(Speech to Slide) ( 음성인식 만으로 문장이 넘어가는 대본 기능)
  - Script Highlighting (현재 읽고 있는 위치를 계산하여 현 시점까지 하이라이팅 )


### 팀원 역할
- 박정현
  - React 기반 웹 프론트엔드 개발 (대본 웹 / 컨트롤러 웹), 네트워크 아키텍처, 서비스 기획
- 한상준
  - Swift iOS 모바일 어플리케이션 컨트롤러 개발, 음성데이터 전처리 및 텍스트 변환, 서비스 디자인
- 강지훈
  - Django 백엔드 서버 구축, MSA 아키텍처 구축, 음성인식 분석 및 텍스트 일치 알고리즘 개발


### ScriptSlide를 사용하는 당신은 누구인가?

- 내 생각과 아이디어를 다른 사람들에게 정말 잘 전하고 싶은 사람
- 내 발표가 정말 중요한 사람
  - ScriptSlide를 사용해 발표하는 사람을 보면 다른 사람들은 '이 발표는 정말 중요하겠구나' 라고 생각
- 내가 준비한 발표 내용을 정확하고 완벽하게 전하고 싶은 사람
- 더 프로페셔널한 발표를 하고 싶은 사람

### ScriptSlide를 만드는 사람은 누구인가?

- 자신의 생각, 아이디어를 매우 소중하게 생각하고 이를 남들에게 퍼뜨리고 싶은 사람
- 다른 사람들의 생각, 아이디어도 매우 소중하게 생각하고 경청할 줄 아는 사람
- 더 많은 사람들이 자신의 생각을 자유롭게 펼칠 수 있는 세상을 믿는 사람
- 나로 인해 수 많은 사람들의 불필요한 암기 시간이 절약될 수 있다고 믿는 사람

### Develop
- REST API를 위한 DRF 개발, AWS 아키텍쳐 설계, 음성인식 분석 및 실시간 문장 유사도 알고리즘 개발
- Https, JWT를 사용하여 회원 관리 기능 개발, 웹소켓을 사용하여 실시간 통신, 유사도 계산 함수 비동기 처리, Sentry를 활용하여 에러 트래킹
- 문장 유사도 알고리즘과 논문을 분석하여 LCS 기반의 자체 알고리즘 개발
-  문장의 bi-gram 인덱스에 기반을 두어 log 함수 그래프 형태의 가중치와 연속 일치에 부가 가중치를 부여


### MSA System Architecture
<img src="https://user-images.githubusercontent.com/49490703/94095678-34d4db00-fe5d-11ea-8dbb-f1a4149d26d1.png"  width="50%">
- 클러스터 환경의 아키텍쳐 설계
- AWS RDS를 사용하여 DB 서버를 분리
- 무 중단 배포를 위해 Nginx 웹 서버와 WAS를 분리
- 안정적인 서비스 운영을 위해 기능 단위의 서버를 다중화
- 서버간 데이터 동기화 목적으로 Redis를 사용

### 성과
- 구글 G Suite Market TOP 40 위와 90,000명 이상의 글로벌 사용자 수 달성
- 글로벌 IT 미디어 10곳 이상에서 서비스 소개, 특허 출원
- 상위 10%에 도달하여 장관상 및 미국 연수 보상
- [Pycon Korea 2020 컨퍼런스 연설](https://www.slideshare.net/jihoonkang29/pycon-korea-2020-238626016)


 
### Demo link
[![demo2](https://i.ytimg.com/an_webp/HG-ZsAW134U/mqdefault_6s.webp?du=3000&sqp=CJ_2r_sF&rs=AOn4CLAe-vW7q3W9k5k1a4PV6P7vq2zExA)](https://www.youtube.com/watch?v=HG-ZsAW134U&t=0s) 

[![demo](https://i.ytimg.com/an_webp/9cAL_6Z8OWY/mqdefault_6s.webp?du=3000&sqp=CNaMsPsF&rs=AOn4CLAPUv8SS8Ii6U8Col5DSg-Xhfr1mw)](https://www.youtube.com/watch?v=9cAL_6Z8OWY&t=0s) 






![version](https://img.shields.io/badge/version-alpha1.0-orange) ![language](https://img.shields.io/badge/language-js--swift--python-yellow) ![framework](https://img.shields.io/badge/framework-react--rxswift--django-brightgreen)

