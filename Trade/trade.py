import requests
import hashlib
import hmac
import time



pr = float(0.1)
listcript = []
target_cryptos = ["BTC", "BNB", "ETH"]
split_pairs = []
##params3 = {'symbol': y+'USDT'}
#print(x+'USDT')


api_key = '86ArQz6AWQasBZGw9cGsWSDiIBu3Q6MwFFkjenqJc68fhwObVg4SD3XIxozeztwG'
api_secret = 'VdnpzILfXv4ccuJyWev0tAQOoPBotAoGnoBMQITq0q0BlOEwSJ2zlMwAkV4Qwnru'
base_url = 'https://api.binance.com/api/v3'
urllist = 'https://api.binance.com/api/v3/ticker/price'
response = requests.get(urllist)
rlist = response.json()

url = base_url + '/account'
# Время в миллисекундах с начала эпохи Unix
timestamp = int(time.time() * 1000)
# Создайте подпись для запроса
query_string = f'timestamp={timestamp}'
signature = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
# Добавьте подпись и API Key к запросу
headers = {
    'X-MBX-APIKEY': api_key
}
params = {
    'timestamp': timestamp,
    'signature': signature
}
# Отправьте GET-запрос для получения баланса
response = requests.get(url, headers=headers, params=params)
account_info = response.json()
# Поиск баланса USDT
usdt_balance = next((balance for balance in account_info['balances'] if balance['asset'] == 'USDT'), None)
if usdt_balance:
    free_usdt = float(usdt_balance['free'])
    locked_usdt = float(usdt_balance['locked'])
    total_usdt = free_usdt + locked_usdt
    print(f'Ваш баланс USDT: {total_usdt}')
else:
    print('USDT не найден на вашем аккаунте')

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
#print(filtered_pairs2)

stripped_pairs = [pair[:-3] for pair in filtered_pairs2]

unique_set = set(stripped_pairs)
# Преобразовываем обратно в список, если это необходимо
unique_list = list(unique_set)

def get_price(crypto, base_crypto):
    pair = f"{crypto}{base_crypto}"
    params = {'symbol': pair}
    response = requests.get(urllist, params=params)
    data = response.json()
    if 'price' in data:
        return float(data['price'])
    else:
        return None

def priceCryptoUSDT():
    paramsx = {'symbol': crypto + 'USDT'}
    responsex = requests.get(urllist, params=paramsx)
    datax = responsex.json()
    return float(datax['price'])

def priceBasecryptoUSDT():
    paramsy = {'symbol': base_crypto + 'USDT'}
    responsey = requests.get(urllist, params=paramsy)
    datay = responsey.json()
    return float(datay['price'])

# Получаем цены для всех пар
for crypto in stripped_pairs:
    for base_crypto in target_cryptos:
        price = get_price(crypto, base_crypto)
        price1 = priceCryptoUSDT()
        price3 = priceBasecryptoUSDT()
        if price is not None:
            format_price = "{:10f}".format(price)
            #print(f"Цена {crypto}/{base_crypto}: {price}")
            print(f"{crypto}USDT", price1)
            print(f"{crypto}{base_crypto}: {format_price}")
            print(f"{crypto}USDT", price3)
