import requests
import hashlib
import hmac
import time
import asyncio
import aiohttp

min_profit = 0.1  # Минимальный профит
max_profit = 2.0  # Максимальная цена для проверки

# Функция для создания подписи запроса
def create_signature(api_secret, query_string):
    return hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()


# Функция для выполнения безопасных GET-запросов
def safe_get(url, params=None, headers=None):
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при запросе: {e}")
        return None


# Функция для получения баланса USDT
def get_usdt_balance(api_key, api_secret):
    base_url = 'https://api.binance.com/api/v3'
    url = f"{base_url}/account"
    timestamp = int(time.time() * 1000)
    query_string = f'timestamp={timestamp}'
    signature = create_signature(api_secret, query_string)

    headers = {'X-MBX-APIKEY': api_key}
    params = {'timestamp': timestamp, 'signature': signature}

    response_data = safe_get(url, params=params, headers=headers)
    if response_data:
        usdt_balance = next((balance for balance in response_data['balances'] if balance['asset'] == 'USDT'), None)
        if usdt_balance:
            return float(usdt_balance['free']) + float(usdt_balance['locked'])
    return None

# Функция для получения актуальной цены по криптопаре с книги ордеров
async def get_order_book_price(session, pair):
    try:
        base_url = 'https://api.binance.com/api/v3'
        url = f"{base_url}/depth"
        params = {'symbol': pair, 'limit': 5}

        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                if 'bids' in data and len(data['bids']) > 0:
                    best_bid_price = float(data['bids'][0][0])
                    return best_bid_price
    except aiohttp.ClientConnectionError as e:
        print(f"Произошла ошибка при выполнении запроса с использованием aiohttp: {e}")
    except Exception as e:
        print(f"Произошла неизвестная ошибка: {e}")
    return None

# Основная функция для анализа
async def analyze_crypto_pairs(api_key, api_secret):
    target_cryptos = ["BTC", "BNB", "ETH"]

    usdt_balance = get_usdt_balance(api_key, api_secret)
    if usdt_balance is not None:
        print(f'Ваш баланс USDT: {usdt_balance}')
    else:
        print('USDT не найден на вашем аккаунте')

    base_url = 'https://api.binance.com/api/v3'
    listcript = []

    urllist = f"{base_url}/ticker/price"
    response = requests.get(urllist)
    rlist = response.json()

    for i in rlist:
        listcript.append(i['symbol'])

    def filter_pairs1(pair):
        for crypto in target_cryptos:
            if pair.startswith(crypto):
                return False
        return True

    filtered_pairs1 = list(filter(filter_pairs1, listcript))

    def filter_pairs2(pair):
        for crypto in target_cryptos:
            if crypto in pair:
                return True
        return False

    filtered_pairs2 = list(filter(filter_pairs2, filtered_pairs1))

    stripped_pairs = [pair[:-3] for pair in filtered_pairs2]

    unique_set = set(stripped_pairs)
    unique_list = list(unique_set)

    async with aiohttp.ClientSession() as session:
        for crypto in stripped_pairs:
            for base_crypto in target_cryptos:
                price = await get_order_book_price(session, f"{crypto}{base_crypto}")
                price1 = await get_order_book_price(session, f"{crypto}USDT")
                price3 = await get_order_book_price(session, f"{base_crypto}USDT")

                if price1 is not None:
                    format_price1 = float(price1)

                if price is not None:
                    format_price = float("{:.11f}".format(price))
                    format_price3 = float(price3)


                b = usdt_balance / format_price1
                a = b * format_price
                l = a * format_price3
                c = ((l * 0.3) / 100)
                profit = l - c - usdt_balance
                #print('Profit = ', profit)


                if profit > min_profit and profit < max_profit:
                    print(f"{crypto}USDT", format_price1)
                    print(f"{crypto}{base_crypto}: {format_price}")
                    print(f"{base_crypto}USDT", format_price3)
                    print('Профит найден!')
                    print('Profit = ', profit)
                    print("-------------------------------------")


if __name__ == "__main__":
    api_key = '86ArQz6AWQasBZGw9cGsWSDiIBu3Q6MwFFkjenqJc68fhwObVg4SD3XIxozeztwG'
    api_secret = 'VdnpzILfXv4ccuJyWev0tAQOoPBotAoGnoBMQITq0q0BlOEwSJ2zlMwAkV4Qwnru'
    asyncio.run(analyze_crypto_pairs(api_key, api_secret))
