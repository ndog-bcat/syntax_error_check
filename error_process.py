import ast

# 오류 검사
def analyze_code(text):
    errors = []
    try:
        ast.parse(text)
    except SyntaxError as e:
        errors.append({"lineno": e.lineno, "msg": e.msg})
    return errors


# 수정안 반환
def display_errors(errors, image, ocr_data):
    return
