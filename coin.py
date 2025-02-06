import requests
import os
from datetime import datetime

# 코인 리스트
symbols = [
    "bitcoin", "ethereum", "binancecoin", "ripple", "cardano",
    "solana", "dogecoin", "litecoin", "polkadot", "bitcoin-cash"
]

# README 파일 경로
README_PATH = "README.md"

# 각 코인의 시세를 가져오는 함수
def get_coin():
    coin_prices = []
    
    # CoinGecko의 API URL
    url = "https://api.coingecko.com/api/v3/simple/price"
    
    # 요청에 포함할 파라미터
    params = {
        'ids': ','.join(symbols),  # symbols에 있는 코인들을 콤마로 구분하여 전달
        'vs_currencies': 'usd'     # 가격을 USD로 요청
    }
    
    try:
        response = requests.get(url, params=params)
        
        # 응답이 정상인 경우
        if response.status_code == 200:
            data = response.json()

            # 각 코인의 가격을 가져와서 출력
            for symbol in symbols:
                if symbol in data:
                    coin_prices.append(f"{symbol.capitalize()}: **${data[symbol]['usd']} USD**")
                else:
                    coin_prices.append(f"{symbol.capitalize()}: Price data missing")
        else:
            coin_prices.append(f"Error: API request failed with status code {response.status_code}")
    except Exception as e:
        coin_prices.append(f"Request failed ({e})")
    
    return coin_prices


# README.md 파일을 업데이트하는 함수
def update_readme():
    """README.md 파일을 업데이트"""
    coin_info = get_coin()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # coin_info를 간결하게 만들기
    coin_info_str = "\n".join(coin_info)
    
    # README 내용 작성 (Markdown)
    readme_content = f"""
# COIN API Status

이 리포지토리는 CoinGecko API를 사용하여 주요 암호화폐 시세를 자동으로 업데이트합니다.

## 📊 현재 시세

다음은 현재 주요 암호화폐의 시세입니다:

{coin_info_str}

## ⏳ 업데이트 시간

최종 업데이트 시간: **{now} (UTC)**

---

자동 업데이트 봇에 의해 관리됩니다.  
[CoinGecko API](https://www.coingecko.com)에서 실시간 시세 정보를 제공합니다.
"""

    # README.md 파일에 내용 쓰기
    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(readme_content)


# 실행
if __name__ == "__main__":
    update_readme()
