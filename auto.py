def install_and_import(package,import_name="NULL"):
    if import_name == "NULL":
        import_name = package
    import importlib
    try:
        importlib.import_module(import_name)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(import_name)
    return 0

#<--import library-->#
install_and_import("subprocess")
install_and_import("sys")
install_and_import("os")
install_and_import("time")
install_and_import("unicodedata")        
install_and_import("requests")
install_and_import("rich")
install_and_import("selenium")
install_and_import("python-dateutil","dateutil.parser")
install_and_import("datetime")
install_and_import("signal")
install_and_import("webdriver-manager","webdriver_manager.chrome")
#<!--import library-->#

from dateutil.parser import parse
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from rich.console import Console
console = Console()
driver = None

#<--USER DATA-->#
NAME = "홍길동"
KRRN = "980502-2100000"
PHONE = "010-1234-5678"
START_TIME = parse("6 Aug 2021 11:00:00 GMT") #GMT 기준 시작시간(GMT AM11:00 => KST PM08:00)
DEBUG = False     #True 로 변경시 시작시간 무시
NF_PASS = False    #무시무시한 기능
#<!--USER DATA-->#

def install_check():
    with console.status("Chrome Driver 설치 확인중..", spinner="monkey"):
        path = ChromeDriverManager().install()
    return path

def frame_change():
    driver.switch_to.default_content() #기본 프레임으로 돌아감
    with console.status("프레임 전환 대기중...", spinner="dots3"):
        WebDriverWait(driver, 60*60*5).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"/html/frameset/frame[1]"))) #메인프레임 전환 
    return 0

def execute_script(driver, text):
    try:
        frame_change() #base(home_n.html) 프레임으로 전환
        driver.execute_script(text) #script 실행
    except Exception as ex:
        console.log("[bold red]SCRIPT EXECUTE ERROR[/bold red]",ex)
    return 0

def getToken():
    f1 = open('./bin/script1','r', encoding='UTF-8')
    f2 = open('./bin/script2','r', encoding='UTF-8')
    script1 = f1.read()
    script2 = f2.read()
    f1.close()
    f2.close()
    execute_script(driver, script1) #NetFunnel 통과 토큰 받음
    time.sleep(1) #응답 수신까지 대기시간 
    execute_script(driver, script2) #토큰 전처리(html에 tokk로 hidden타입으로 저장)
    return 0

def goNfCheck():
    f3 = open('./bin/script3','r', encoding='UTF-8')
    script3 = f3.read()
    f3.close()
    execute_script(driver, script3) #실 변수에 대입
    return 0
    
def main():
    global driver
    options = webdriver.ChromeOptions()
    
    # 브라우저 윈도우 사이즈
    options.add_argument('window-size=1020x700')
    
    # 사람처럼 보이게 하는 옵션들
    options.add_argument("disable-gpu")   # 가속 사용 x
    options.add_argument("lang=ko_KR")    # 가짜 플러그인 탑재
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')  # user-agent 이름 설정
    
    #개발자모드 활성화
    options.add_argument("--auto-open-devtools-for-tabs")
    
    #웹드라이버 로드
    driver = webdriver.Chrome(install_check(), options=options)
    
    response = requests.get("https://ncvr.kdca.go.kr/index.html") #서버시간 수신(GMT)
    server_time = parse(response.headers['date'].split(', ')[1])  #서버시간 DateTime/필요없는 데이터 절삭
    remain_time = START_TIME - server_time                        #남은시간 계산
    console.log("서버시간 = [bold blue] GMT "+server_time.strftime("%H시 %M분 %S초")+"[/bold blue]")
    
    if (not DEBUG): #디버깅 모드일경우 시간 체크 PASS
        with console.status("[bold green]시작 대기중 입니다.", spinner="dots3") as status:
            while(True):
                response = requests.get("https://ncvr.kdca.go.kr/index.html")   #서버시간 수신(GMT)
                server_time = parse(response.headers['date'].split(', ')[1])   #서버시간 DateTime/필요없는 데이터 절삭
                remain_time = START_TIME - server_time                        #남은시간 계산
                if(remain_time.seconds <= 30 and NF_PASS):                   #Token 유효시간 30초
                    break
                if(remain_time.seconds <= 0):
                    break
                else:
                    console.log(f"남은시간 = [bold red]"+str(remain_time.seconds)+"초[/bold red]")
                    time.sleep(0.5)  #0.5초 대기
                
    driver.implicitly_wait(time_to_wait=60*60*5) #driver 최대 timeout시간을 5시간으로
    driver.get(url="https://ncvr.kdca.go.kr/index.html") #메인예약 페이지로 이동
    
    frame_change() #실제 정보가 담긴 메인 프레임으로 변경
    
    if(not NF_PASS): #NetFunnel PASS is False?
        with console.status("'사전예약 바로가기' 페이지 로딩 대기중...", spinner="dots3"):
            try:
                element = WebDriverWait(driver, 60*60*5).until(
                    EC.presence_of_element_located((By.CLASS_NAME , 'btn-booking')) #버튼이 로딩될때까지 대기
                )
            finally:
                console.log("'사전예약 바로가기' 페이지 로딩 완료!")
        driver.find_element_by_xpath("/html/body/div/div/div[2]").click() #로딩되면 클릭
    else: #NetFunnel PASS is True
        getToken() #Netfunnel 토큰 사전 발급
        goNfCheck() #사전예약 버튼 강제클릭
    
    frame_change()
    
    with console.status("'예방접종 예약하기' 페이지 로딩 대기중...", spinner="dots3"):
        WebDriverWait(driver, 60*60*5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div/section/div[1]/div[2]/div[1]/a"))).click()
    console.log("'예방접종 예약하기' 페이지 로딩 완료!")
    
    frame_change()
    
    with console.status("'코로나19 예방접종 본인예약' 페이지 로딩 대기중...", spinner="dots3"):
        WebDriverWait(driver, 60*60*5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="rsrvSelfBtn"]'))).click()
    console.log("'코로나19 예방접종 본인예약' 페이지 로딩 완료!")
    
    frame_change()
    
    #예약정보 기록 시작
    driver.find_element_by_xpath('//*[@id="apnmNm"]').send_keys(NAME)
    driver.find_element_by_xpath('//*[@id="apnmRrn1"]').send_keys(KRRN.split('-')[0])
    driver.find_element_by_xpath('//*[@id="apnmRrn2"]').send_keys(KRRN.split('-')[1])
    driver.find_element_by_xpath('//*[@id="apnmMtnoTofmn"]').send_keys(PHONE.split('-')[0])
    driver.find_element_by_xpath('//*[@id="apnmMtno1"]').send_keys(PHONE.split('-')[1])
    driver.find_element_by_xpath('//*[@id="apnmMtno2"]').send_keys(PHONE.split('-')[2])
    driver.find_element_by_xpath('//*[@id="vcnRsrvFrm"]/div/table/tbody/tr[7]/td/span[2]/label').click()
    #예약 기본정보 입력 완료
    
    #본인인증 시작(공동인증)
    driver.find_element_by_xpath('//*[@id="vcnRsrvFrm"]/div/table/tbody/tr[3]/td/ul/li[3]/a').click()
    
    console.log("[bold magenta]명령 수행완료[/bold magenta]") 
    return 0

def Exit_gracefully(signal, frame):
    sys.exit(-1)
    
if __name__ == "__main__":
    signal.signal(signal.SIGINT, Exit_gracefully)
    try:
        main()
    except Exception as ex:
        if(ex == KeyboardInterrupt):
            exit(0)
        else:
            print('오류가 발생 했습니다', ex)
    