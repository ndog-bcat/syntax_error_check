# 실시간 화면 캡처를 통해 기초 문법적 오류를 수정해주는 프로그램
import time
import pyautogui
import cv2
import numpy as np
import keyboard
from image_process import image_processing
from error_process import analyze_code, display_errors
from png_to_html import get_code


def on_press(key):
    if key.name == 'esc':
        print("program end")
        return False  # 프로그램 종료 함수 (사용자가 esc키를 누르면 종료)


keyboard.on_press(on_press)  # 키보드 이벤트 리스너 설정

answer = 'no'

while answer == 'no':
    get_region = np.array(pyautogui.screenshot())
    get_region = cv2.cvtColor(get_region, cv2.COLOR_RGB2BGR)
    x, y, width, height = cv2.selectROI(
        windowName='Drag mouse to select region. When youre done, press enter',
        img=get_region
        )
    selected_region = get_region[y:y+height, x:x+width]  # 선택영역 이미지 잘라내기

    cv2.imshow('show you the region for 3 seconds', selected_region)
    cv2.waitKey(3000)
    cv2.destroyAllWindows()

    answer = input('Are you sure that this region is'
                   'you wanted?(answer is yes or no)')
    # 앞으로 지켜볼 영역 지정

apply_threshold = False  # 이진화 여부 변수 (이진화를 원하면 True 아니면 False지만 경험상 안쓰는게 나을듯)

while True:
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    screenshot = image_processing(screenshot, apply_threshold)  # 이미지 전처리
    html_code = get_code(screenshot)  # html 코드로 변환
    errors = analyze_code(html_code)  # 오류검사
    if errors:
        display_errors(errors)  # 수정안 이미지 반환
    time.sleep(5)  # 5초마다 체크
