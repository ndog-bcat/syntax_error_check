from collections import defaultdict
import pytesseract


def extract_structured_text(img):
    data = pytesseract.image_to_data(
        img, lang='eng+kor', config="--oem 3 --psm 6",
        output_type=pytesseract.Output.DICT
    )
    # 1) line_num별 단어 수집
    lines = defaultdict(list)
    widths = []
    for i, txt in enumerate(data['text']):
        if not txt.strip():
            continue
        ln = data['line_num'][i]
        x = data['left'][i]
        w = data['width'][i]
        lines[ln].append((x, txt))
        widths.append(w)

    # 2) char_width 계산 (평균 문자 폭)
    char_width = sum(widths) / len(widths)  # px

    # 3) base_x 계산
    base_x = min(xs for words in lines.values() for xs, _ in words)

    # 4) 줄별 재구성
    reconstructed = []
    for ln in sorted(lines):
        words = sorted(lines[ln], key=lambda x: x[0])
        indent = int((words[0][0] - base_x) / char_width)
        line = " " * indent + " ".join(w for _, w in words)
        reconstructed.append(line)

    return "\n".join(reconstructed)
