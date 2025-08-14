import json
import os, requests
from datetime import datetime, timezone, timedelta

# ===== 1. 시총 상위 코인 필터 =====
def fetch_top_marketcap(limit=20):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1
    }
    headers = {"User-Agent": "Mozilla/5.0 (compatible; topcap/1.0)"}
    data = requests.get(url, params=params, headers=headers , timeout=10)
    data.raise_for_status()
    data=data.json()

    return [
        coin['symbol'].upper() 
        for coin in data ]

# ===== 2. 펀딩비  =====
def fetch_bybit_data(symbols):
   data=[]
   f_url = "https://api.bybit.com/v5/market/funding/history"
   k_url = "https://api.manana.kr/exchange/rate/KRW/USD.json"
   upbit_url = "https://api.upbit.com/v1/ticker"
   bin_url = "https://api.binance.com/api/v3/ticker/price"
   

  
   for sym in symbols:
       try:
           upbit_params = {
            "markets": "KRW-"+sym  # 원하는 코인심볼 콤마로 구분
            }
           bin_params = {
           "symbol": sym+"USDT"
            }
   
         
           f_params = {
              "symbol":sym+"USDT", 
              "category":"linear",
              "limit":1
           }
         

           up=requests.get(upbit_url, params= upbit_params).json()[0]['trade_price']
           bin=float(requests.get(bin_url, params= bin_params).json()['price'])
           krw=requests.get(k_url).json()[0]['rate']
           if bin ==0 or up ==0 :
               continue
           else:
              
              
               kimp = ((up / (bin * krw)) - 1) * 100
               r = requests.get(f_url, params= f_params)
               r.raise_for_status() 
              
               data.append({
                   'symbol' : sym,
                   'fundingRate' : r.json()["result"]["list"][0]["fundingRate"],
                   'kimp' : kimp
               })



       except Exception as e:
        print("요청 실패:", e)
        continue
       
      
   return data   

def sendmessage(data):
    TOKEN = "8091499353:AAFkdchr_aIBnjTLGIhmFSWwbmDY5fCWbIE"
    CHAT_ID = 7288071784
    
    # 한국 시간
    kst = datetime.now(timezone.utc) + timedelta(hours=9)
    now_time = kst.strftime("%Y-%m-%d %H:%M:%S")
    
    # 표 데이터 만들기
    rows = []
    for i, it in enumerate(data[:10], start=1):
        sym  = it.get("symbol", "").replace("USDT", "")
        kimp = float(it.get("kimp", 0.0))            # 예: -0.85
        fr   = float(it.get("fundingRate", 0.0)) * 100  # 예: 0.0100%
        rows.append(f"{i:>2}.  {sym:<5} | KIMP {kimp:+7.2f}% | FUND {fr:>8.4f}%")
    
    table = "\n".join(rows) if rows else "No data"
    
    # 최종 메시지
    msg = (
        f"📊 <b>김프 & 펀딩피 리포트</b>\n"
        f"🕒 {now_time}\n"
        f"<pre>{table}</pre>\n"
        "#김프 #펀딩피 #트레이딩"
    )
    
    # 전송
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = requests.get(url, params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"})
    
    # 결과 확인
    if response.status_code == 200:
        print("메시지가 성공적으로 전송되었습니다.")
    else:
        print(f"메시지 전송 실패: {response.text}")



  
def main():
    a=[]
    b=[]
    a=fetch_top_marketcap(limit=20)
    print(a)
    b=fetch_bybit_data(a)
    print(b)
    sendmessage(b)



if __name__ == "__main__":   # ← 파일 직접 실행해야 동작
    main()

      

