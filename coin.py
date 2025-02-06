import requests
import matplotlib.pyplot as plt
from datetime import datetime

symbols = [
    "bitcoin", "ethereum", "binancecoin", "ripple", "cardano",
    "solana", "dogecoin", "litecoin", "polkadot", "bitcoin-cash"
]

def get_coin():
    coin_prices = []
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': ','.join(symbols),
        'vs_currencies': 'usd'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # 각 코인의 가격을 가져와서 출력
        for symbol in symbols:
            if symbol in data:
                coin_prices.append((symbol.capitalize(), data[symbol]['usd']))
            else:
                coin_prices.append((symbol.capitalize(), 'Price data missing'))
    return coin_prices

def plot_graph():
    coin_data = get_coin()

    # 코인 이름과 시세를 리스트로 분리
    coins = [coin[0] for coin in coin_data]
    prices = [coin[1] if isinstance(coin[1], (int, float)) else 0 for coin in coin_data]

    # 그래프 그리기
    plt.figure(figsize=(10, 6))
    plt.barh(coins, prices, color='skyblue')
    plt.xlabel('Price (USD)')
    plt.title('Coin Prices')

    # 이미지로 저장
    plt.tight_layout()
    plt.savefig('coin_prices.png')
    plt.close()

def update_readme():
    coin_info = get_coin()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # coin_info를 문자열로 생성
    coin_info_str = "\n".join([f"{coin[0]}: ${coin[1]} USD" for coin in coin_info])

    # README 내용 작성
    readme_content = f"""
# COIN API Status

이 리포지토리는 COIN API를 사용하여 코인 TOP 10 시세를 자동으로 업데이트합니다.

## 현재 시세
> {coin_info_str}

## 시세 그래프
![Coin Price Chart](coin_prices.png)

⏳ 업데이트 시간: {now} (UTC)

---
자동 업데이트 봇에 의해 관리됩니다.
"""

    # README.md 파일에 내용 쓰기
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(readme_content)

# 실행
if __name__ == "__main__":
    plot_graph()  # 그래프 이미지 생성
    update_readme()  # README.md 파일 업데이트
