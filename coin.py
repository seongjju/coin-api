import requests
import time
from datetime import datetime
import matplotlib.pyplot as plt

# 코인 리스트
symbols = [
    "bitcoin", "ethereum", "binancecoin", "ripple", "cardano",
    "solana", "dogecoin", "litecoin", "polkadot", "bitcoin-cash"
]

# 파일 경로
README_PATH = "README.md"
IMG_PATH = "crypto_prices.png"


def get_coin():
    """CoinGecko API에서 코인 가격 조회"""
    coin_prices = {}

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': ','.join(symbols),
        'vs_currencies': 'usd'
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            for symbol in symbols:
                coin_prices[symbol.capitalize()] = data.get(symbol, {}).get('usd', None)
        else:
            print(f"Error: API 요청 실패 (Status Code {response.status_code})")
    except Exception as e:
        print(f"Request failed ({e})")

    return coin_prices


def create_graph(coin_prices):
    """Matplotlib로 그래프 생성 후 PNG 저장"""
    coins = list(coin_prices.keys())
    prices = list(coin_prices.values())

    plt.figure(figsize=(10, 5))
    plt.bar(coins, prices, color='blue')
    plt.xlabel("Coins")
    plt.ylabel("Price (USD)")
    plt.title("Cryptocurrency Prices (USD)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(IMG_PATH)  # 이미지 저장
    plt.close()


def update_readme(coin_prices):
    """README.md 업데이트"""
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # 코인 가격 정보 포맷팅
    coin_info_str = "\n".join(
        [f"- {coin}: **${price} USD**" if price else f"- {coin}: 데이터 없음"
         for coin, price in coin_prices.items()]
    )

    # README.md 내용 작성
    readme_content = f"""
# 📊 Cryptocurrency Prices (Updated)

이 리포지토리는 CoinGecko API를 사용하여 코인 TOP 10 시세를 자동으로 업데이트합니다.

## 💰 현재 시세
{coin_info_str}

## 📈 시세 변화 그래프
![Crypto Prices](crypto_prices.png)

⏳ 업데이트 시간: {now} (UTC)

---
자동 업데이트 봇에 의해 관리됩니다.
"""

    # README.md 파일 저장
    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(readme_content)


def track_price():
    """5분간 가격 변동 추적"""
    recent_prices = {symbol: [] for symbol in symbols}

    for _ in range(5):  # 5분 동안 가격 추적
        coin_prices = get_coin()
        for symbol, price in coin_prices.items():
            if price is not None:
                recent_prices[symbol].append(price)
        
        time.sleep(60)  # 1분 간격으로 가격 추적

    return recent_prices


def create_time_series_graph(recent_prices):
    """최근 5분 가격 데이터를 기반으로 선 그래프 생성"""
    times = [f"{i+1} min ago" for i in range(5)]

    for symbol, prices in recent_prices.items():
        plt.plot(times, prices, marker='o', label=f"{symbol} Price (USD)")

    plt.xlabel('Time (Minutes Ago)')
    plt.ylabel('Price (USD)')
    plt.title('Cryptocurrency Prices - Last 5 Minutes')
    plt.legend()
    plt.tight_layout()
    plt.savefig(IMG_PATH)
    plt.close()


# 실행
if __name__ == "__main__":
    recent_prices = track_price()  # 최근 5분간 가격 추적
    create_time_series_graph(recent_prices)  # 선 그래프 생성
    update_readme(recent_prices)  # README.md 업데이트