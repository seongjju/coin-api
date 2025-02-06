import requests
import time
from datetime import datetime
import plotext as plt  # ASCII 그래프 라이브러리

# 코인 리스트
symbols = [
    "bitcoin", "ethereum", "binancecoin", "ripple", "cardano",
    "solana", "dogecoin", "litecoin", "polkadot", "bitcoin-cash"
]

# README 파일 경로
README_PATH = "README.md"


def get_coin():
    coin_prices = {}
    
    # CoinGecko API URL
    url = "https://api.coingecko.com/api/v3/simple/price"
    
    params = {
        'ids': ','.join(symbols),  # symbols 리스트의 코인들을 콤마로 구분하여 전달
        'vs_currencies': 'usd'     # 가격을 USD로 요청
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            for symbol in symbols:
                if symbol in data:
                    coin_prices[symbol.capitalize()] = data[symbol]['usd']
                else:
                    coin_prices[symbol.capitalize()] = None  # 가격 데이터 없음
        else:
            print(f"Error: API request failed with status code {response.status_code}")
    except Exception as e:
        print(f"Request failed ({e})")
    
    return coin_prices


def create_ascii_graph():
    """ASCII 그래프 생성"""
    coin_prices = get_coin()
    coins = list(coin_prices.keys())
    prices = list(coin_prices.values())

    # ASCII 그래프 생성
    plt.clear_data()
    plt.bar(coins, prices, width=100)
    plt.title("Cryptocurrency Prices (USD)")
    plt.xlabel("Coins")
    plt.ylabel("Price")
    
    return plt.build()  # ASCII 그래프 문자열 반환


def update_readme():
    """README.md 업데이트"""
    coin_prices = get_coin()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 코인 가격 정보 문자열 변환
    coin_info_str = "\n".join(
        [f"- {coin}: **${price} USD**" if price else f"- {coin}: 데이터 없음" for coin, price in coin_prices.items()]
    )

    # ASCII 그래프 생성
    ascii_graph = create_ascii_graph()

    # README.md 내용 작성
    readme_content = f"""
# COIN API Status

이 리포지토리는 CoinGecko API를 사용하여 코인 TOP 10 시세를 자동으로 업데이트합니다.

## 📊 현재 시세
{coin_info_str}

## 📈 시세 변화 그래프
{ascii_graph}
⏳ 업데이트 시간: {now} (UTC)

---
자동 업데이트 봇에 의해 관리됩니다.
"""

    # README.md 파일 업데이트
    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(readme_content)


# 실행
if __name__ == "__main__":
    update_readme()