import cv2
import base64
import openai
from apikey import OPENAI_API_KEY
from bs4 import BeautifulSoup

openai.api_key = OPENAI_API_KEY


def image_to_base64(image):
    _, buffer = cv2.imencode('.png', image)  # PNG 형식으로 인코딩
    return base64.b64encode(buffer).decode('utf-8')


def get_code(img):
    encoded_image = image_to_base64(img)
    image_payload = {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/png;base64,{encoded_image}"
        }
    }
    response = openai.chat.completions.create(
        model="gpt-4o",  # 또는 gpt-4-vision-preview
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "이 이미지에 있는 코드를"
                        " HTML + CSS 형식으로 복원해줘. 줄바꿈과 들여쓰기,"
                        " 구조를 유지해서 <pre><code> 블록에 담아줘."},
                    image_payload
                ]
            }
        ],
        temperature=0.2,
        max_tokens=2048  # 원하는 출력 길이에 따라 조정 가능
    )

    result_html = response['choices'][0]['message']['content']
    soup = BeautifulSoup(result_html, 'html.parser')
    python_code = soup.find('code').get_text()
    return python_code
