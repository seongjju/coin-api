import requests
import os
from datetime import datetime
from dotenv import load_dotenv


# 코인 리스트
symbols = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT",
    "SOLUSDT", "DOGEUSDT", "LTCUSDT", "DOTUSDT", "BCHUSDT"
]


# README 파일 경로
README_PATH = "README.md"

# 각 코인의 시세를 가져와 출력
def get_coin():
    symbols = [
        "BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT",
        "SOLUSDT", "DOGEUSDT", "LTCUSDT", "DOTUSDT", "BCHUSDT"
    ]
    coin_prices = []
    
    for symbol in symbols:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url)
        data = response.json()
        coin_prices.append(f"{symbol}: {data['price']} USDT")
    
    return coin_prices



def update_readme():
    """README.md 파일을 업데이트"""
    coin_info = get_coin()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    readme_content = f"""
# COIN API Status

이 리포지토리는 BIANANCE API를 사용하여 코인 TOP 10 시세를 자동으로 업데이트합니다.

## 현재 서울 날씨
> {coin_info}

⏳ 업데이트 시간: {now} (UTC)

---
자동 업데이트 봇에 의해 관리됩니다.
"""

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(readme_content)

if __name__ == "__main__":
    update_readme()