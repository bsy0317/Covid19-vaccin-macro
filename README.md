#  코로나19 백신 사전예약 매크로
> 설정된 예약시간이 되면, 서버시간에 맞추어 백신예약 페이지로 자동 이동합니다.  
이후 각 버튼을 단계별로 자동으로 클릭한 후 개인정보를 자동으로 기입하게 됩니다.  
  
##  주요 변수

 - `NAME` 변수는 접종대상자의 이름
 - `KRRN` 변수는 `하이픈('-')`을 포함한 주민번호 13자리
 - `PHONE` 변수는 `하이픈('-')`을 포함한 전화번호 11자리
 - `START_TIME` 변수는 `GMT 기준`으로 사전예약 접수 시작시간
 - `DEBUG` 변수는 시작시간을 무시하고 진행함
 - `NF_PASS` Netfunnel 통과
 
## 필요 라이브러리

`pip install requests, rich, selenium, python-dateutil, webdriver-manager, unicodedata`
 - 자동으로 설치되니 따로 설치할 필요는 없습니다.

## 사용 방법

1. `git clone https://github.com/bsy0317/Covid19-vaccin-macro`
> 오른쪽 중반 Clone or download 버튼 클릭 > Download Zip을 클릭하여 다운로드 하는 방법도 가능.
2. 다운받은 파일 압축 해제
3. `python-3.9.exe(최신버전)` 설치
> [python-3.9.exe 다운로드](https://www.python.org/downloads/)  
> ※ 설치 시 하단 Add Python 3.x.x to PATH 체크
4. Chrome 다운로드 후 설정
5. auto.py 파일을 열어 41~48번 줄에 개인정보, 예약시간을 GMT시간대 기준으로 설정
>한국시간을 GMT시간대로 변경하는 방법은 [KST to GMT](https://www.freeconvert.com/time/kst-to-gmt) 참고
6. `CMD`를 열어 `auto.py`가 있는 곳 까지 이동
7. 스크립트 실행
>py auto.py

또는 `jupyter notebook`에서 `auto.ipynb`을 실행

## 사용문의

>Email: talk@kakao.one