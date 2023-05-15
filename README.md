# My_Animal

📚 stacks 
------
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">  <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white"> <img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white">  <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"> 

***

💖 장고 심화 프로젝트 : DRF를 사용한 커뮤니티 사이트! 반려동물을 자랑하는 커뮤니티 🐶🐱
------
> 2023.05.08 ~ 2023.05.15
  
백오피스 프로젝트 - Django DRF를 활용하여 프론트엔드와 백엔드가 분리된 프로젝트를 구성해보기

🖼️ Front-End 
------
https://github.com/ksw406020230309/Myanimal_front02


🤔 기능
------
### 회원기능 : jwt token 사용

1. 회원가입 `POST`
    - id : 데이터 고유 id(PK)
    - account : 아이디, `UNIQUE`
    - email : 이메일, 회원가입/비밀번호 찾기 시에 인증 정보로 사용
    - password : 비밀번호, 회원 가입이나 회원 수정 시에 해시
    - nickname : 닉네임
    - category : 관심있거나 키우는 반려동물
2. 로그인
3. 회원 정보 수정 `PATCH`
4. 회원 탈퇴 `DELETE`
5. 팔로우 ,팔로워
    - 팔로우 여부에 따라 팔로우/언팔로우 버튼
    - 자기 자신 팔로우 불가
6. 프로필 페이지
    - 팔로우 목록, 팔로잉 목록

### Article

1. 게시글 CREATE - ToDo List 생성 `POST`
    - 로그인한 사용자만 가능
    - 테이블 필드
      - id : 데이터 고유 id
      - title : 제목
      - content : 내용
      - category : 어떤 동물에 관한 글인가
      - created_at : 글 생성 시각
      - updated_at : 글 수정 시각, `default=None`
      - user_id : User과 FK

2. 게시글 READ `GET`
    - 목록
        - 홈, 게시글 목록
    - 상세페이지
        - 해당 게시글의 상세 페이지
        
4. 게시글 UPDATE `PATCH`
    - **로그인한 사용자이면서 글 작성자일 때만 가능**

5. 게시글 DELETE `DELETE`
    - **로그인한 사용자이면서 글 작성자일 때만 가능**

6. 댓글 작성
    - 게시글 상세 페이지에서 로그인한 사용자만 댓글 작성 가능
7. 댓글 수정, 삭제 
    - 로그인한 사용자이면서 댓글 작성자일 때만 가능

8. 좋아요, 북마크
    - 글 하단 하트 버튼 누르면 좋아요, 한 번 더 누르면 좋아요 취소 (북마크도 동일)



### 추가 요구사항


***

ERD
------
![image](https://github.com/ksw406020230309/MyAnimal/assets/120750451/3f791fe2-1060-40c3-856c-40010e035d9a)

