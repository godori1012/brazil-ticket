import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# --- 설정 ---
KFA_ID = "YOUR_ID"
KFA_PW = "YOUR_PASSWORD"
TICKET_PAGE_URL = "https://www.playkfa.com/ticket/event_list.php"
DRIVER_PATH = "./chromedriver"

def login(driver, user_id, user_pw):
    """로그인 페이지로 이동하여 로그인을 수행합니다."""
    print("로그인을 시도합니다...")
    try:
        driver.get("https://www.playkfa.com/member/login.php")
        
        id_input = driver.find_element(By.CSS_SELECTOR, "#login_id")
        pw_input = driver.find_element(By.CSS_SELECTOR, "#login_pw")
        login_button = driver.find_element(By.CSS_SELECTOR, ".login_btn")
        
        id_input.send_keys(user_id)
        pw_input.send_keys(user_pw)
        login_button.click()
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".logout"))
        )
        print("로그인 성공!")
        return True
    except Exception as e:
        print(f"로그인 실패: {e}")
        return False

def find_ticket_button_and_click(driver):
    """'예매하기' 버튼이 활성화될 때까지 페이지를 새로고침하며 대기하고, 활성화되면 즉시 클릭합니다."""
    print("예매 페이지로 이동합니다.")
    driver.get(TICKET_PAGE_URL)
    
    while True:
        try:
            ticket_button = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), '예매하기')]"))
            )
            
            print("예매하기 버튼 발견! 즉시 클릭합니다.")
            ticket_button.click()
            break
            
        except TimeoutException:
            print("아직 예매 시작 전입니다. 페이지를 새로고침합니다.")
            driver.refresh()
        except Exception as e:
            print(f"알 수 없는 오류 발생: {e}")
            time.sleep(1)
            driver.refresh()

def select_seat_and_proceed(driver):
    """좌석 선택 페이지로 넘어간 후, 가능한 좌석을 자동으로 선택합니다."""
    try:
        print("좌석 선택을 시도합니다.")
        
        available_seat = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".seat_able"))
        )
        
        print("선택 가능한 좌석 발견! 클릭합니다.")
        available_seat.click()
        
        next_button = driver.find_element(By.CSS_SELECTOR, "#next_btn")
        next_button.click()
        
        print("좌석 선택 완료. 결제 페이지로 이동합니다.")
        
    except Exception as e:
        print(f"좌석 선택 중 오류 발생: {e}")

def main():
    """매크로 실행 메인 함수"""
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    
    # 1. 로그인
    if not login(driver, KFA_ID, KFA_PW):
        driver.quit()
        return
    
    # 2. 예매 버튼 무한 클릭
    find_ticket_button_and_click(driver)
    
    # 3. 좌석 선택
    select_seat_and_proceed(driver)
    
    # 4. 매크로 종료 방지
    print("자동화 단계를 완료했습니다. 5분 후 브라우저가 종료됩니다.")
    time.sleep(300)
    driver.quit()

if __name__ == "__main__":
    main()