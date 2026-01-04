import cv2
import pytesseract


# 이미지 전처리 함수
def image_processing(screenshot, apply_threshold):
    # 그레이스케일 변환
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # 노이즈 제거
    gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

    # 대비 향상 : 이진화 (배경에서 코드 추출 잘 되도록)
    if apply_threshold:
        gray = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )

    # 글자 높이 기반 이미지 크기 조정
    height, width = gray.shape
    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

    # 글자 크기 측정
    heights = [
        int(data['height'][i])
        for i in range(len(data['text']))
        if data['text'][i].strip() != ''
        ]
    average_height = sum(heights) / len(heights)

    # 이미지 크기 조정 비율
    scale_factor = 37 / average_height
    new_size = (int(width*scale_factor), int(height*scale_factor))

    # 이미지 크기 변경
    gray = cv2.resize(gray, new_size)

    return gray
