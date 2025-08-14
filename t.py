# diag.py
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

s = requests.Session()
s.headers.update({"User-Agent": "kimp-bot/1.0"})
s.mount("https://", HTTPAdapter(max_retries=Retry(
    total=3, backoff_factor=0.5, status_forcelist=[429,500,502,503,504]
)))

def check_binance(sym="BTCUSDT"):
    r = s.get("https://api.binance.com/api/v3/ticker/price",
              params={"symbol": sym}, timeout=8)
    print("BIN", r.status_code, r.text[:200])

def check_bybit(sym="BTCUSDT"):
    r = s.get("https://api.bybit.com/v5/market/funding/history",
              params={"symbol": sym, "category": "linear", "limit": 1}, timeout=8)
    print("BYB", r.status_code, r.text[:200])

if __name__ == "__main__":
    check_binance()
    check_bybit()






