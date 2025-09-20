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

def find_ticket_button_and_click(driver):
    """'예매하기' 버튼이 활성화될 때까지 페이지를 새로고침하며 대기하고, 활성화되면 즉시 클릭합니다."""
    print("예매 페이지로 이동합니다.")
    driver.get(TICKET_PAGE_URL)
    
    while True:
        try:
            ticket_button = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), '예매하기')]")) # 수정 필요
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
    
    # 좌석 선택 코드 구현 필요

def select_seat_and_proceed(driver):
    """좌석 선택 및 결제 단계를 진행합니다."""
    print("좌석 선택 및 결제 단계를 시작합니다.")
    wait = WebDriverWait(driver, 10)

    try:
        # --- 1. 좌석 선택 페이지 > 선택 가능한 좌석 요소를 찾아서 클릭
        # 예시: available_seat = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#seat_map .available-seat")))
        # available_seat.click()
        print("TODO: 좌석 선택 코드를 여기에 구현해주세요.")
        time.sleep(2) # 임시 대기

        # 다음 단계 버튼 클릭
        # 예시: next_button = wait.until(EC.element_to_be_clickable((By.ID, "nextStepButton")))
        # next_button.click()
        print("TODO: 좌석 선택 후 다음 버튼 클릭 코드를 여기에 구현해주세요.")
        time.sleep(2) # 임시 대기

        # --- 2. 결제 정보 입력/확인 페이지
        
        # 약관 동의 체크박스 클릭 (필요한 경우)
        # 예시: agree_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "agreeTerms")))
        # agree_checkbox.click()
        print("TODO: 약관 동의 체크박스 클릭 코드를 여기에 구현해주세요.")
        time.sleep(2) # 임시 대기

        # 결제 수단 선택 (필요한 경우)
        # 예시: payment_method = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='creditcard']")))
        # payment_method.click()
        print("TODO: 결제 수단 선택 코드를 여기에 구현해주세요.")
        time.sleep(2) # 임시 대기

        # 최종 결제 버튼 클릭
        # 예시: final_pay_button = wait.until(EC.element_to_be_clickable((By.ID, "finalPayButton")))
        # final_pay_button.click()
        print("TODO: 최종 결제 버튼 클릭 코드를 여기에 구현해주세요.")
        time.sleep(2) # 임시 대기

        print("좌석 선택 및 결제 단계 완료.")
        return True
    except TimeoutException:
        print("좌석 선택/결제 단계에서 시간 초과가 발생했습니다.")
        print(f"현재 URL: {driver.current_url}")
        return False
    except Exception as e:
        print(f"좌석 선택/결제 중 오류 발생: {e}")
        print(f"현재 URL: {driver.current_url}")
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
    
    # 2. 예매 버튼 무한 클릭
    find_ticket_button_and_click(driver)

    # # 3. 좌석 선택 및 결제 단계
    # if not select_seat_and_proceed(driver):
    #     print("좌석 선택 및 결제 단계에 실패하여 프로그램을 종료합니다.")
    #     driver.quit()
    #     return

    # 4. 매크로 종료 방지
    print("자동화 단계를 완료했습니다. 5분 후 브라우저가 종료됩니다.")
    time.sleep(300)
    driver.quit()

if __name__ == "__main__":
    main()
