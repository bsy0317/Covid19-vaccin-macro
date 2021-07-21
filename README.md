# Covid19-vaccin-macro
>코로나19 백신 사전예약 매크로

설정된 예약시간이 되면, 서버시간에 맞추어 백신예약 페이지로 자동 이동합니다.  
이후 각 버튼을 단계별로 자동으로 클릭한 후 개인정보를 자동으로 기입하게 됩니다.  
본 프로젝트에는 NetFunnel을 우회하는 불법적인 기능을 포함하고있지 않습니다.  

## 사용 방법
1. `git clone https://github.com/bsy0317/Covid19-vaccin-macro`
> 오른쪽 중반 Clone or download 버튼 클릭 > Download Zip을 클릭하여 다운로드 하는 방법도 가능합니다.
2. `다운받은 파일 압축 해제`
3. `python-3.9.exe(최신버전) 설치`
> [python-3.9.exe 다운로드](https://www.python.org/downloads/)  
> ※ 설치 시 하단 Add Python 3.x.x to PATH 체크
4. `Chrome 다운로드 후 설치`
5. `auto.py 파일을 열어 14~18번 줄에 개인정보 수정, 46번 줄에 예약시간을 GMT시간대 기준으로 설정`
>한국시간을 GMT시간대로 변경하는 방법은 [KST to GMT](https://www.freeconvert.com/time/kst-to-gmt) 참고
6. `CMD를 열어 auto.py가 있는 곳 까지 이동`
7. `스크립트 실행`
>py auto.py

## 필요 라이브러리
<pre><code>pip install requests
pip install rich
pip install selenium
pip install python-dateutil
pip install webdriver-manager
pip install unicodedata
</pre></code>

## 주의 사항
1. python-3.8.0.exe 설치 시 설치시 하단 Add Python 3.8 to PATH 체크
2. 필요한 라이브러리는 자동으로 설치되나 오류가 있을 수 있음.
>이런경우 수동으로 설치

## 기여하기
버그 등이 발생하면 이슈로 등록해 주시거나, 문제가 되는 부분을 수정하신 후 PR해 주시면 감사하겠습니다.

## 라이선스
이 매크로는 MIT 라이선스를 적용받습니다.
