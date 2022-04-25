import requests
import smtplib

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
my_email = "sender_email@yahoo.com"
password = "01234567()"
recipient_address = "recipient_email@yahoo.com"

# Determine STOCK price increase/decrease between yesterday and the day before yesterday
api_url = "https://www.alphavantage.co/query"
api_key = "LC24BRFD7074L98D"
params = {"function":"TIME_SERIES_DAILY",
          "symbol":STOCK,
          "apikey":api_key}
response = requests.get(url=api_url, params=params)
response.raise_for_status()
response = response.json()

keys = [key for (key, val) in response['Time Series (Daily)'].items()]
last_trading_day_close = float(response['Time Series (Daily)'][keys[0]]['4. close'])
day_before_last_close = float(response['Time Series (Daily)'][keys[1]]['4. close'])
percentage_change = (last_trading_day_close - day_before_last_close)/day_before_last_close * 100

if abs(percentage_change) > 5:
    #get the first 3 news pieces for the COMPANY_NAME.
    api_url = "https://newsapi.org/v2/everything"
    api_key = "c91b0b75fce946aab2176ddf18f39ab1"
    params = {"q":COMPANY_NAME,
              "sortby":"publishedAt",
              "searchIn":"title",
              "language":"en",
              "apikey":api_key}

    response = requests.get(url=api_url, params=params)
    response.raise_for_status()
    response = response.json()

    if last_trading_day_close > day_before_last_close:
        icon = "🔺"
    else:
        icon = "🔻"

    messages = []
    messages.append(f"{STOCK}: {icon}{round(abs(percentage_change), 2)}% \n"
                   f"Headline: {response['articles'][0]['title']}. \n"
                   f"Brief: {response['articles'][0]['description']}")

    messages.append(f"{STOCK}: {icon}{round(abs(percentage_change), 2)}% \n"
                   f"Headline: {response['articles'][1]['title']}. \n"
                   f"Brief: {response['articles'][1]['description']}")

    messages.append(f"{STOCK}: {icon}{round(abs(percentage_change), 2)}% \n"
                   f"Headline: {response['articles'][2]['title']}. \n"
                   f"Brief: {response['articles'][2]['description']}")

    for message in messages:
        with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=recipient_address,
                msg=message
            )