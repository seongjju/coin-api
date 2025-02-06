import requests
import time
from datetime import datetime
import matplotlib.pyplot as plt


# 코인 리스트
symbols = [
    "bitcoin"
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


def track_price():
    """현재 시점에서 5분 간의 가격 추적 (최근 5개 가격 기록)"""
    prices = []  # 가격을 저장할 리스트

    for _ in range(5):  # 5번 가격을 추적 (5분)
        coin_prices = get_coin()
        price = coin_prices.get(symbols[0].capitalize(), None)
        if price is not None:
            prices.append(price)

        time.sleep(60)  # 1분 간격으로 가격 추적

    return prices


def create_graph(prices):
    """Matplotlib로 그래프 생성 후 PNG 저장"""
    plt.figure(figsize=(10, 5))
    
    # x축은 시간 (현재, 1분전, 2분전, 3분전, 4분전)
    times = ["Now", "1 min ago", "2 min ago", "3 min ago", "4 min ago"]
    
    # y축은 가격
    plt.plot(times, prices, label="Price (USD)", marker='o')
    
    plt.xlabel("Time")
    plt.ylabel("Price (USD)")
    plt.title("Cryptocurrency Price Changes Over the Last 5 Minutes")
    plt.legend()
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


# 실행
if __name__ == "__main__":
    prices = track_price()  # 최근 5분간 가격 추적
    create_graph(prices)  # 가격 변동 그래프 생성
    coin_prices = get_coin()  # 최신 코인 가격 조회
    update_readme(coin_prices)  # README 파일 업데이트