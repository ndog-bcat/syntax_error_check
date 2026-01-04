import pytesseract


def extract_text(img):
    # OCR 설정: psm6(한글인식.....텍스트의 균일한 단일 블록을 가정함)-코드 블록 적합
    custom_config = r"--oem 3 --psm 6"

    # 텍스트 추출
    extracted_text = pytesseract.image_to_string(
        img,
        lang="eng+kor",
        config=custom_config
        )

    return extracted_text
