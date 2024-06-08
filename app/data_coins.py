

def get_data_coins(count_data=100):
    coins = []
    data = {
        'coin_table__num': '1',
        'coin_table__name': {'name': 'Meta Masters Guild', 'label': 'Cheap Master Prod.', 'name-tag': 'KYC'},
        'coin_table__chain': 'ETH',
        'coin_table__cap': '$1,584.53',
        'coin_table__price': '$1,584.53',
        'coin_table__volume': {'value': '$26,721,855,845', 'label': '1,157,275 BTC'},
        'coin_table__24h': '5.93%',
        'coin_table__date': 'In 2 months',
        'coin_table__votes': '1, 302, 000',
        'coin_table__votes24h': '1, 300, 941%',
        'coin_table__vote': 'Vote'
    }

    for i in range(count_data):
        new_data = data.copy()
        new_data['coin_table__num'] = str(i + 1)
        coins.append(new_data)

    return coins
