import requests
import os
from datetime import datetime

# 코인 리스트
symbols = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT",
    "SOLUSDT", "DOGEUSDT", "LTCUSDT", "DOTUSDT", "BCHUSDT"
]

# README 파일 경로
README_PATH = "README.md"

# 각 코인의 시세를 가져오는 함수
def get_coin():
    coin_prices = []
    
    for symbol in symbols:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                # 'price' 키가 있는지 확인
                if 'price' in data:
                    coin_prices.append(f"{symbol}: {data['price']} USDT")
                else:
                    coin_prices.append(f"{symbol}: Price data missing")
            else:
                coin_prices.append(f"{symbol}: Error - API request failed with status code {response.status_code}")
        except Exception as e:
            coin_prices.append(f"{symbol}: Request failed ({e})")
    
    return coin_prices

# README.md 파일을 업데이트하는 함수
def update_readme():
    """README.md 파일을 업데이트"""
    coin_info = get_coin()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # coin_info를 간결하게 만들기
    coin_info_str = "\n".join(coin_info)
    
    # README 내용 작성
    readme_content = f"""
# COIN API Status

이 리포지토리는 BIANANCE API를 사용하여 코인 TOP 10 시세를 자동으로 업데이트합니다.

## 현재 시세
> {coin_info_str}

⏳ 업데이트 시간: {now} (UTC)

---
자동 업데이트 봇에 의해 관리됩니다.
"""

    # README.md 파일에 내용 쓰기
    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(readme_content)

# 실행
if __name__ == "__main__":
    update_readme()
