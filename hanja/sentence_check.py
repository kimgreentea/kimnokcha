
import json

input_file = "sentence.json"
output_file = "sentence_변환.json"


# 1. JSON 읽기 및 문법 검사
try:
    with open(input_file, "r", encoding="utf-8-sig") as f:
        sentences = json.load(f)

except json.JSONDecodeError as e:
    print("❌ JSON 문법 오류")
    print(f"오류 내용: {e.msg}")
    print(f"위치: {e.lineno}행 {e.colno}열")

    with open(input_file, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    start = max(0, e.lineno - 3)
    end = min(len(lines), e.lineno + 2)

    print("\n오류 주변 코드:")
    for i in range(start, end):
        marker = ">>" if i == e.lineno - 1 else "  "
        print(f"{marker} {i + 1}: {lines[i].rstrip()}")
        if i == e.lineno - 1:
            print("      " + " " * (e.colno - 1) + "^")

    raise SystemExit("수정 후 다시 실행하세요.")


# 2. 데이터 구조 검사 및 변환
if not isinstance(sentences, list):
    raise SystemExit("❌ 최상위 데이터는 JSON 배열이어야 합니다.")

result = []
errors = []

for i, sentence in enumerate(sentences, start=1):
    if not isinstance(sentence, dict):
        errors.append(f"{i}번 문장: 객체가 아닙니다.")
        continue

    for field in ("hanmun", "reading", "meaning"):
        if field not in sentence:
            errors.append(f"{i}번 문장: '{field}' 필드가 없습니다.")

    key_hanja = sentence.get("keyHanja", [])

    if not isinstance(key_hanja, list):
        errors.append(f"{i}번 문장: 'keyHanja'가 배열이 아닙니다.")
        continue

    valid_items = []

    for j, item in enumerate(key_hanja, start=1):
        if not isinstance(item, dict):
            errors.append(f"{i}번 문장 keyHanja {j}번: 객체가 아닙니다.")
            continue

        missing = [
            field for field in ("hanja", "meaning", "reading")
            if field not in item
        ]

        if missing:
            errors.append(
                f"{i}번 문장 keyHanja {j}번: "
                f"누락 필드 {', '.join(missing)}"
            )
            continue

        valid_items.append({
            "hanja": item["hanja"],
            "meaning": item["meaning"],
            "reading": item["reading"]
        })

    if any(field not in sentence for field in
           ("hanmun", "reading", "meaning")):
        continue

    result.append({
        "hanmun": sentence["hanmun"],
        "reading": sentence["reading"],
        "meaning": sentence["meaning"],
        "keyHanja": valid_items
    })


# 3. 구조 오류 출력
if errors:
    print("❌ 데이터 구조 오류")
    for error in errors:
        print("-", error)

    raise SystemExit("오류를 수정한 뒤 다시 실행하세요.")


# 4. 원하는 형식으로 저장
with open(output_file, "w", encoding="utf-8") as f:
    f.write("[\n")

    for i, sentence in enumerate(result):
        f.write("    {\n")
        f.write(
            f'        "hanmun": '
            f'{json.dumps(sentence["hanmun"], ensure_ascii=False)},\n'
        )
        f.write(
            f'        "reading": '
            f'{json.dumps(sentence["reading"], ensure_ascii=False)},\n'
        )
        f.write(
            f'        "meaning": '
            f'{json.dumps(sentence["meaning"], ensure_ascii=False)},\n'
        )
        f.write('        "keyHanja": [\n')

        for j, item in enumerate(sentence["keyHanja"]):
            comma = "," if j < len(sentence["keyHanja"]) - 1 else ""
            f.write(
                "            "
                + json.dumps(item, ensure_ascii=False)
                + comma + "\n"
            )

        f.write("        ]\n")
        f.write("    }")

        if i < len(result) - 1:
            f.write(",")

        f.write("\n")

    f.write("]\n")


# 5. 저장된 파일 재검사
try:
    with open(output_file, "r", encoding="utf-8") as f:
        json.load(f)
except json.JSONDecodeError as e:
    raise SystemExit(
        f"❌ 출력 파일 오류: {e.lineno}행 {e.colno}열 - {e.msg}"
    )

print(f"✅ 변환 완료: {len(result)}개 문장")
print(f"저장 파일: {output_file}")
