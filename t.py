import requests
def main():
  urls = {
    "bybit_funding": "https://api.bybit.com/v5/market/funding/history",
    "manana_fx": "https://api.manana.kr/exchange/rate/KRW/USD.json",
    "upbit_ticker": "https://api.upbit.com/v1/ticker?markets=KRW-BTC",
    "binance_price": "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
}

  for name, url in urls.items():
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        print(f"[OK] {name} 응답 길이: {len(r.text)}")
    except Exception as e:
        print(f"[FAIL] {name} → {e}")

   



if __name__ == "__main__":   # ← 파일 직접 실행해야 동작
    main()
