import requests
import time
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image
import io
import base64

# 코인 리스트
symbols = [
    "bitcoin", "ethereum", "binancecoin", "ripple", "cardano",
    "solana", "dogecoin", "litecoin", "polkadot", "bitcoin-cash"
]

# README 파일 경로
README_PATH = "README.md"


def get_coin():
    coin_prices = []
    
    # CoinGecko API URL
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


def create_graph():
    # 코인 리스트와 가격 데이터
    coin_prices = get_coin()
    coins = [coin.split(":")[0].strip() for coin in coin_prices]  # 코인 이름 추출
    prices = [float(coin.split("$")[1].split(" ")[0].strip()) for coin in coin_prices]  # 가격 추출

    # 그래프 그리기
    plt.figure(figsize=(10, 6))
    plt.bar(coins, prices, color='skyblue')
    plt.xlabel('Coins')
    plt.ylabel('Price in USD')
    plt.title('Cryptocurrency Prices')

    # 그래프 이미지로 저장
    graph_path = "coin_prices_graph.png"
    plt.tight_layout()
    plt.savefig(graph_path)

    # 그래프 이미지 열기
    img = Image.open(graph_path)

    # 이미지를 base64로 인코딩
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return f"![Coin Prices Graph](data:image/png;base64,{img_str})"


def update_readme():
    """README.md 파일을 업데이트"""
    coin_info = get_coin()
    graph_image = create_graph()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # coin_info를 간결하게 만들기
    coin_info_str = "\n".join(coin_info)
    
    # README 내용 작성
    readme_content = f"""
# COIN API Status

이 리포지토리는 CoinGecko API를 사용하여 코인 TOP 10 시세를 자동으로 업데이트합니다.

## 현재 시세
> {coin_info_str}

## 시세 변화 그래프
{graph_image}

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
