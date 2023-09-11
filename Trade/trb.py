import requests
import hashlib
import hmac
import time

#balancet = float(102.44)
pr = float(0.1)
x = 'MDT'
y = 'BTC'
params1 = {'symbol': x+'USDT'}
params2 = {'symbol': x+y}
params3 = {'symbol': y+'USDT'}


api_key = '86ArQz6AWQasBZGw9cGsWSDiIBu3Q6MwFFkjenqJc68fhwObVg4SD3XIxozeztwG'
api_secret = 'VdnpzILfXv4ccuJyWev0tAQOoPBotAoGnoBMQITq0q0BlOEwSJ2zlMwAkV4Qwnru'
base_url = 'https://api.binance.com/api/v3'


while True:

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
        #print(f'Ваш баланс USDT: {total_usdt}')
    else:
        print('USDT не найден на вашем аккаунте')


    url = base_url + '/ticker/price'
    urlbook = base_url + '/depth?'

    #https: // api.binance.com / api / v3 / depth?limit = 10 & symbol = BTCUSDT
    responseb = requests.get(urlbook, params=params2)
    datab = responseb.json()
    priceb = float(datab['bids'][0][0])
    print('PricelastOrderBook = ', '{:.10f}'.format(priceb))

    response1 = requests.get(url, params=params1)
    response2 = requests.get(url, params=params2)
    response3 = requests.get(url, params=params3)
    data1 = response1.json()
    data2 = response2.json()
    data3 = response3.json()

    price1 = float(data1['price'])
    price2 = float(data2['price'])
    price3 = float(data3['price'])
    print(price1, '{:.10f}'.format(priceb), price3)
    b = total_usdt/price1
    a = b * priceb
    l = a * price3
    #print(l)
    c = ((l*0.3)/100)
    profit = l-c-total_usdt
    #print('profit = ', profit)

    if profit >= pr:
        #print(f'Ваш баланс USDT: {total_usdt}')
        print('Профит найден!!!!!!!!!!!!!!!!1')
        print('PricelastOrderBook = ', priceb)
        print('profit = ', profit)

    time.sleep(1)