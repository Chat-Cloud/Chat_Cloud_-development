from dotenv import load_dotenv
import os
# .env 파일 불러오기
# 현재 파일(db.py)이 있는 위치에서 .env 절대경로 지정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
import os
from dotenv import load_dotenv

print("ENV_PATH:", ENV_PATH)
print("File exists:", os.path.exists(ENV_PATH))

with open(ENV_PATH, "rb") as f:
    print("Raw bytes:", f.read())

with open(ENV_PATH, "r", encoding="utf-8") as f:
    print("Text:", f.read())

load_dotenv(ENV_PATH)

print("DB_HOST =", os.getenv("DB_HOST"))
print("DB_USER =", os.getenv("DB_USER"))
print("DB_PASSWORD =", os.getenv("DB_PASSWORD"))
print("DB_DATABASE =", os.getenv("DB_DATABASE"))

