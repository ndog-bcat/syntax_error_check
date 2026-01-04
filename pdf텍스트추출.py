# 화면 캡처를 통해 pdf 텍스트를 파일로 추출해주는 프로그램
import pyautogui
import cv2
import numpy as np
from image_process import image_processing
from text_process import extract_text

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
                   'you wanted?(answer is yes or no) ')
    # 앞으로 지켜볼 영역 지정

apply_threshold = False  # 이진화 여부 변수 (이진화를 원하면 True 아니면 False지만 경험상 안쓰는게 나을듯)

result_text = ""
page = 0

while True:
    user_need = input("Need to extract text from PDF? (yes/no) \n")
    if user_need == "no":
        result_file = input("Enter the desired name as the file name.\n")
        output_path = result_file + ".txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result_text)
        print(f"The results were saved to {output_path}\n")
        print("Program end")
        break
    elif user_need != "yes":
        print("The answer must be yes or no\n")
    else:
        page += 1
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        screenshot = image_processing(screenshot, apply_threshold)  # 이미지 전처리
        text = extract_text(screenshot)  # 텍스트 추출
        result_text += "Page " + str(page) + "\n"
        result_text += text + "\n"
