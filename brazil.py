 │      1                                                                                                                                                         │
 │      2 # -*- coding: utf-8 -*-                                                                                                                                 │
 │      3                                                                                                                                                         │
 │      4 import time                                                                                                                                             │
 │      5 from selenium import webdriver                                                                                                                          │
 │      6 from selenium.webdriver.common.by import By                                                                                                             │
 │      7 from selenium.webdriver.support.ui import WebDriverWait                                                                                                 │
 │      8 from selenium.webdriver.support import expected_conditions as EC                                                                                        │
 │      9 from selenium.common.exceptions import TimeoutException                                                                                                 │
 │     10                                                                                                                                                         │
 │     11 # --- 설정 ---                                                                                                                                          │
 │     12 # 실제 범인은 이 부분에 자신의 정보를 입력합니다.                                                                                                       │
 │     13 KFA_ID = "YOUR_ID"                                                                                                                                      │
 │     14 KFA_PW = "YOUR_PASSWORD"                                                                                                                                │
 │     15                                                                                                                                                         │
 │     16 # 예매 페이지 URL (정확한 URL은 경기마다 다를 수 있음)                                                                                                  │
 │     17 TICKET_PAGE_URL = "https://www.playkfa.com/ticket/event_list.php"                                                                                       │
 │     18                                                                                                                                                         │
 │     19 # 사용할 웹 드라이버 (Chrome)                                                                                                                           │
 │     20 # 범인은 자신의 컴퓨터에 설치된 chromedriver 경로를 지정해야 합니다.                                                                                    │
 │     21 DRIVER_PATH = "./chromedriver"                                                                                                                          │
 │     22                                                                                                                                                         │
 │     23 # --- 경고 ---                                                                                                                                          │
 │     24 # 이 코드는 티켓 예매 매크로의 작동 방식을 이해하기 위한 교육용 예시입니다.                                                                             │
 │     25 # 이 코드를 사용하여 실제 티켓 예매를 시도하는 것은 불법이며,                                                                                           │
 │     26 # 웹사이트 이용 약관에 따라 계정 정지 등의 불이익을 받을 수 있습니다.                                                                                   │
 │     27 # 모든 책임은 사용자에게 있습니다.                                                                                                                      │
 │     28                                                                                                                                                         │
 │     29 def login(driver, user_id, user_pw):                                                                                                                    │
 │     30     """로그인 페이지로 이동하여 로그인을 수행합니다."""                                                                                                 │
 │     31     print("로그인을 시도합니다...")                                                                                                                     │
 │     32     try:                                                                                                                                                │
 │     33         # playKFA 메인 페이지는 리디렉션될 수 있으므로 로그인 페이지로 직접 접근                                                                        │
 │     34         driver.get("https://www.playkfa.com/member/login.php")                                                                                          │
 │     35                                                                                                                                                         │
 │     36         # 실제 웹사이트의 ID, PW 입력 필드, 로그인 버튼의 selector를 찾아야 합니다.                                                                     │
 │     37         # 예: driver.find_element(By.ID, "member_id")                                                                                                   │
 │     38         id_input = driver.find_element(By.CSS_SELECTOR, "#login_id")                                                                                    │
 │     39         pw_input = driver.find_element(By.CSS_SELECTOR, "#login_pw")                                                                                    │
 │     40         login_button = driver.find_element(By.CSS_SELECTOR, ".login_btn")                                                                               │
 │     41                                                                                                                                                         │
 │     42         id_input.send_keys(user_id)                                                                                                                     │
 │     43         pw_input.send_keys(user_pw)                                                                                                                     │
 │     44         login_button.click()                                                                                                                            │
 │     45                                                                                                                                                         │
 │     46         # 로그인이 완료될 때까지 잠시 대기                                                                                                              │
 │     47         WebDriverWait(driver, 10).until(                                                                                                                │
 │     48             EC.presence_of_element_located((By.CSS_SELECTOR, ".logout")) # 로그아웃 버튼이 보이면 로그인 성공                                           │
 │     49         )                                                                                                                                               │
 │     50         print("로그인 성공!")                                                                                                                           │
 │     51         return True                                                                                                                                     │
 │     52     except Exception as e:                                                                                                                              │
 │     53         print(f"로그인 실패: {e}")                                                                                                                      │
 │     54         return False                                                                                                                                    │
 │     55                                                                                                                                                         │
 │     56 def find_ticket_button_and_click(driver):                                                                                                               │
 │     57     """'예매하기' 버튼이 활성화될 때까지 페이지를 새로고침하며 대기하고, 활성화되면 즉시 클릭합니다."""                                                 │
 │     58     print("예매 페이지로 이동합니다.")                                                                                                                  │
 │     59     driver.get(TICKET_PAGE_URL)                                                                                                                         │
 │     60                                                                                                                                                         │
 │     61     while True:                                                                                                                                         │
 │     62         try:                                                                                                                                            │
 │     63             # '예매하기' 버튼이 나타나고 '클릭 가능'해질 때까지 최대 1초간 대기합니다.                                                                  │
 │     64             # 실제 사이트에서는 버튼의 selector가 다를 수 있습니다. (예: .btn_buy, #ticket_open)                                                        │
 │     65             # 또한, '품절'이 아닌 '예매하기' 상태를 특정해야 할 수 있습니다.                                                                            │
 │     66             ticket_button = WebDriverWait(driver, 1).until(                                                                                             │
 │     67                 EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), '예매하기')]"))                                                             │
 │     68             )                                                                                                                                           │
 │     69                                                                                                                                                         │
 │     70             print("예매하기 버튼 발견! 즉시 클릭합니다.")                                                                                               │
 │     71             ticket_button.click()                                                                                                                       │
 │     72             break # 버튼 클릭에 성공하면 루프 탈출                                                                                                      │
 │     73                                                                                                                                                         │
 │     74         except TimeoutException:                                                                                                                        │
 │     75             # 1초 안에 버튼을 찾지 못하면 페이지를 새로고침하고 다시 시도합니다.                                                                        │
 │     76             # 이것이 서버에 엄청난 부하를 주는 주범입니다.                                                                                              │
 │     77             print("아직 예매 시작 전입니다. 페이지를 새로고침합니다.")                                                                                  │
 │     78             driver.refresh()                                                                                                                            │
 │     79         except Exception as e:                                                                                                                          │
 │     80             print(f"알 수 없는 오류 발생: {e}")                                                                                                         │
 │     81             time.sleep(1)                                                                                                                               │
 │     82             driver.refresh()                                                                                                                            │
 │     83                                                                                                                                                         │
 │     84 def select_seat_and_proceed(driver):                                                                                                                    │
 │     85     """좌석 선택 페이지로 넘어간 후, 가능한 좌석을 자동으로 선택합니다."""                                                                              │
 │     86     try:                                                                                                                                                │
 │     87         # 좌석 선택 페이지(iframe)로 전환해야 할 수 있습니다.                                                                                           │
 │     88         # WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "seat_iframe")))                                            │
 │     89                                                                                                                                                         │
 │     90         print("좌석 선택을 시도합니다.")                                                                                                                │
 │     91                                                                                                                                                         │
 │     92         # 가장 간단한 매크로는 등급과 상관없이 첫 번째 선택 가능한 좌석을 클릭합니다.                                                                   │
 │     93         # 실제 좌석 선택기의 selector는 매우 복잡합니다. (예: #seat_area .seat.available)                                                               │
 │     94         available_seat = WebDriverWait(driver, 20).until(                                                                                               │
 │     95             EC.presence_of_element_located((By.CSS_SELECTOR, ".seat_able")) # '선택 가능한 좌석'을 나타내는 가상 selector                               │
 │     96         )                                                                                                                                               │
 │     97                                                                                                                                                         │
 │     98         print("선택 가능한 좌석 발견! 클릭합니다.")                                                                                                     │
 │     99         available_seat.click()                                                                                                                          │
 │    100                                                                                                                                                         │
 │    101         # 좌석 선택 완료 후 다음 단계로 넘어가는 버튼 클릭                                                                                              │
 │    102         # 예: driver.find_element(By.ID, "next_step_button").click()                                                                                    │
 │    103         next_button = driver.find_element(By.CSS_SELECTOR, "#next_btn") # '다음 단계'를 나타내는 가상 selector                                          │
 │    104         next_button.click()                                                                                                                             │
 │    105                                                                                                                                                         │
 │    106         print("좌석 선택 완료. 결제 페이지로 이동합니다.")                                                                                              │
 │    107         # 이후 결제 과정은 자동화가 더 복잡하여 보통 여기서 멈추고 수동으로 진행합니다.                                                                 │
 │    108                                                                                                                                                         │
 │    109     except Exception as e:                                                                                                                              │
 │    110         print(f"좌석 선택 중 오류 발생: {e}")                                                                                                           │
 │    111                                                                                                                                                         │
 │    112 def main():                                                                                                                                             │
 │    113     """매크로 실행 메인 함수"""                                                                                                                         │
 │    114                                                                                                                                                         │
 │    115     # Selenium 웹 드라이버 시작                                                                                                                         │
 │    116     options = webdriver.ChromeOptions()                                                                                                                 │
 │    117     # 매크로 탐지를 피하기 위한 옵션들을 추가할 수 있습니다.                                                                                            │
 │    118     options.add_experimental_option("excludeSwitches", ["enable-automation"])                                                                           │
 │    119     options.add_argument("--disable-blink-features=AutomationControlled")                                                                               │
 │    120                                                                                                                                                         │
 │    121     driver = webdriver.Chrome(options=options)                                                                                                          │
 │    122     driver.implicitly_wait(3) # 암묵적 대기                                                                                                             │
 │    123                                                                                                                                                         │
 │    124     # 1. 로그인                                                                                                                                         │
 │    125     if not login(driver, KFA_ID, KFA_PW):                                                                                                               │
 │    126         driver.quit()                                                                                                                                   │
 │    127         return                                                                                                                                          │
 │    128                                                                                                                                                         │
 │    129     # 2. 예매 버튼 무한 클릭                                                                                                                            │
 │    130     find_ticket_button_and_click(driver)                                                                                                                │
 │    131                                                                                                                                                         │
 │    132     # 3. 좌석 선택                                                                                                                                      │
 │    133     select_seat_and_proceed(driver)                                                                                                                     │
 │    134                                                                                                                                                         │
 │    135     # 4. 매크로 종료 방지 (사용자가 수동으로 결제할 시간을 줌)                                                                                          │
 │    136     print("자동화 단계를 완료했습니다. 5분 후 브라우저가 종료됩니다.")                                                                                  │
 │    137     time.sleep(300)                                                                                                                                     │
 │    138     driver.quit()                                                                                                                                       │
 │    139                                                                                                                                                         │
 │    140                                                                                                                                                         │
 │    141 if __name__ == "__main__":                                                                                                                              │
 │    142     main()            