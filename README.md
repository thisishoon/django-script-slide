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


### 왜 이것이 중요한가?

- 사람들이 발표를 하는 이유?
  - **자신의 생각, 아이디어를 다른 사람들에게 전하고 퍼뜨리고 싶어서.**
  - 발표를 함으로써 남들도 나와 똑같은 생각을 갖게 만들기 위함.
- 이러한 목표를 달성하기 위해서는 매우 효과적인 발표가 필요하다.
  - 단순히 아이디어 자체만으로는 남을 설득할 수 없다.
  - **그 아이디어가 믿음으로 이어질 수 있는 설득력 있는 발표 내용이 훨씬 더 중요하다.**
- 하지만 사람들은 발표를 준비하는 대부분의 시간을 발표 내용보다는 준비한 내용을 암기하는 것에 많은 시간을 쏟는다.
  - **아무리 준비한 내용을 완벽하게 암기했다 하더라고 내용 그 자체가 좋지 않다면 아무 소용이 없다.**
  - 사실 진정으로 그 생각을 믿는 사람이라면, 굳이 모든 내용을 암기하지 않더라도 누군가 계속 발표의 방향성을 잡아주기만 한다면 완벽하게 발표를 진행할 수 있다.
  - 이에 사람들은 종종 그들의 대본을 종이 대본으로 인쇄해 이용하기도 한다.
  - **하지만 종이 쪼가리를 읽는 것으로는 남들을 설득할 수 없다.**
- ScriptSlide 는 사람들로 하여금 더 많은 시간을 '아이디어'와 '내용'에 쏟을 수 있도록 해준다.
  - 발표에 있어서 더 이상 암기라는 쓸모없고 낭비적인 행동은 필요 없다.
  - 사람들은 한정된 시간에서 아이디어 그 자체에 더 집중할 수 있게 된다.
  - 구글 검색 등장 후 우리는 더 이상 암기를 하지 않는다. 언제든지 모든 정보를 알 수 있기 때문에.
  - ScriptSlide 등장 후 우리는 더 이상 암기를 하지 않는다. 언제든지 모든 대본을 알 수 있기 때문에.

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
- 내가 만든 ScriptSlide를 사용해 성공적인 발표를 하는 사람

### MSA System Architecture
<img src="https://user-images.githubusercontent.com/49490703/94095678-34d4db00-fe5d-11ea-8dbb-f1a4149d26d1.png"  width="50%">
 
### Demo link
[![demo2](https://i.ytimg.com/an_webp/HG-ZsAW134U/mqdefault_6s.webp?du=3000&sqp=CJ_2r_sF&rs=AOn4CLAe-vW7q3W9k5k1a4PV6P7vq2zExA)](https://www.youtube.com/watch?v=HG-ZsAW134U&t=0s) 

[![demo](https://i.ytimg.com/an_webp/9cAL_6Z8OWY/mqdefault_6s.webp?du=3000&sqp=CNaMsPsF&rs=AOn4CLAPUv8SS8Ii6U8Col5DSg-Xhfr1mw)](https://www.youtube.com/watch?v=9cAL_6Z8OWY&t=0s) 






![version](https://img.shields.io/badge/version-alpha1.0-orange) ![language](https://img.shields.io/badge/language-js--swift--python-yellow) ![framework](https://img.shields.io/badge/framework-react--rxswift--django-brightgreen)

