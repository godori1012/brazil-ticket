import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException

# --- 설정 ---
KFA_ID = "rhdmstjrjdi"
KFA_PW = "koko1379!!"
LOGIN_URL = "https://shop.playkfa.com/login"
TICKET_PAGE_URL = "https://shop.playkfa.com/ticket/koreavsbrazil"

def login(driver, user_id, user_pw):
    """로그인 페이지로 이동하여 KFA 통합회원 로그인을 수행합니다."""
    print("로그인을 시도합니다...")
    try:
        # 1. shop.playkfa.com/login 페이지로 이동
        driver.get(LOGIN_URL)
        wait = WebDriverWait(driver, 10)

        # 2. "KFA 통합회원 로그인" 버튼을 찾아 클릭 (텍스트 기반으로 안정적으로 찾기)
        print("KFA 통합회원 로그인 버튼을 찾습니다...")
        kfa_login_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'KFA 통합회원 로그인')]"))
        )
        kfa_login_button.click()
        print("KFA 통합회원 로그인 버튼 클릭 완료")

        # 3. KFA 통합 로그인 페이지(account.kfa.or.kr)로 넘어갈 때까지 대기
        wait.until(EC.url_contains("account.kfa.or.kr"))
        print(f"KFA 통합 로그인 페이지로 이동: {driver.current_url}")

        # 4. ID, PW 입력
        id_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
        pw_input = driver.find_element(By.ID, "password")

        for char in user_id:
            id_input.send_keys(char)
            time.sleep(random.uniform(0.05, 0.1))
        for char in user_pw:
            pw_input.send_keys(char)
            time.sleep(random.uniform(0.05, 0.1))

        # 5. 로그인 버튼 클릭 (KFA 페이지의 submit 버튼)
        login_submit_button = driver.find_element(By.CSS_SELECTOR, "button[name='login']")
        login_submit_button.click()
        print("로그인 정보 제출 완료")

        # 6. 최종적으로 playkfa.com 페이지로 돌아와서 로그아웃 버튼이 보일 때까지 대기
        print("로그인 성공 여부를 확인합니다...")
        WebDriverWait(driver, 15).until(EC.url_contains("playkfa.com"))
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".logout"))
        )
        print("로그인 성공!")
        return True

    except UnexpectedAlertPresentException as e:
        print(f"로그인 중 예기치 않은 경고창 발생: {e.alert_text}")
        return False
    except TimeoutException:
        print("로그인 실패: 특정 단계에서 시간 초과가 발생했습니다.")
        print(f"현재 URL: {driver.current_url}")
        return False
    except Exception as e:
        print(f"로그인 중 알 수 없는 오류 발생: {e}")
        return False

def main():
    """매크로 실행 메인 함수"""
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)

    # 로그인 시도
    if not login(driver, KFA_ID, KFA_PW):
        print("로그인에 실패하여 프로그램을 종료합니다.")
        driver.quit()
        return
    
    # 2. 예매 버튼 무한 클릭 (필요시 주석 해제)
    find_ticket_button_and_click(driver)

    # 3. 매크로 종료 방지
    print("자동화 단계를 완료했습니다. 5분 후 브라우저가 종료됩니다.")
    time.sleep(300)
    driver.quit()

if __name__ == "__main__":
    main()