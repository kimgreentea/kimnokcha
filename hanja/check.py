from pyodide.http import open_url
from collections import Counter

url = "https://kimgreentea.github.io/kimnokcha/hanja/words.json"

response = open_url(url)
response.raise_for_status()

words = response.json()

counts = Counter(word["hanja"] for word in words)

print("전체 데이터:", len(words), "개")
print("한자 종류:", len(counts), "개")
print()

for hanja, count in counts.items():
    if count > 1:
        print("중복", hanja, count, "개")

print()

for i in words:
    print(i["hanja"], end="")
