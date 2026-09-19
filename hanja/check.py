import os
import json
import requests
from collections import Counter

url = "https://kimgreentea.github.io/kimnokcha/hanja/words.json"

if os.path.exists("words.json"):
    print("로컬 사용")
    
    with open("words.json", "r", encoding="utf-8") as f:
        words = json.load(f)

else:
    print("깃허브 검사")
    
    response = requests.get(url)
    response.raise_for_status()
    words = response.json()


counts = Counter(word["hanja"] for word in words)
print("전체 데이터:", len(words), "개")
print("한자 종류:", len(counts), "개")
print()
print()
for hanja, count in counts.items():
    if count > 1:
        print("중복", hanja, count, "개")


print()
for i in words:
    print(i["hanja"], end="")
