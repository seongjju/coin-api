import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# 추적할 코인 리스트
coins = ["bitcoin", "ethereum", "ripple"]  # Coingecko ID 기준 (ripple = XRP)

IMG_PATHS = {coin: f"{coin}_price.png" for coin in coins}

def get_price(coin, time_delta=0):
    """
    지정된 코인의 가격을 가져옴.
    time_delta: 현재 기준 몇 분 전 데이터를 가져올지
    """
    time_stamp = datetime.utcnow() - timedelta(minutes=time_delta)
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": coin, "vs_currencies": "usd"}
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return time_stamp.strftime("%H:%M"), response.json()[coin]["usd"]
    return time_stamp.strftime("%H:%M"), None

def update_graphs():
    """
    모든 코인에 대한 그래프를 업데이트
    """
    for coin in coins:
        price_data = [get_price(coin, i) for i in range(5)][::-1]  # 5분간 데이터 수집
        
        times, prices = zip(*price_data)
        
        plt.figure(figsize=(6, 4))
        plt.plot(times, prices, marker="o", linestyle="-", color="blue", label=f"{coin.upper()} Price (USD)")
        plt.xlabel("Time (UTC)")
        plt.ylabel("Price (USD)")
        plt.title(f"{coin.upper()} Price - Last 5 min")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid()
        
        plt.savefig(IMG_PATHS[coin])
        plt.close()

def update_readme():
    """
    README.md 업데이트
    """
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    readme_content = f"""
# 📊 Real-time Crypto Price Tracker

매 1분마다 업데이트되는 코인 가격 그래프입니다.  
최근 **5분 간의 가격 변화**를 보여줍니다.

## 📈 최근 5분 가격 변동

### Bitcoin (BTC)
![Bitcoin Price](bitcoin_price.png)

### Ethereum (ETH)
![Ethereum Price](ethereum_price.png)

### Ripple (XRP)
![Ripple Price](ripple_price.png)

⏳ 업데이트 시간: {now} (UTC)

---
자동 업데이트 봇에 의해 관리됩니다.
"""

    with open("README.md", "w", encoding="utf-8") as file:
        file.write(readme_content)

if __name__ == "__main__":
    update_graphs()
    update_readme()