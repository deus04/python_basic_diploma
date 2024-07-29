
import requests
import json
from utils.misc.construct_answer import construct_answer, api_token, tomorrow


print('low_request Ready')


def low_request():
    my_req = requests.get('https://api.travelpayouts.com/aviasales/v3/prices_for_dates?'
                          'origin=AER&'
                          'destination=BEG&'
                          'departure_at={departure_at}&'
                          'unique=true&'
                          'sorting=price&'
                          'direct=false&'
                          'currency=rub&'
                          'limit=10&'
                          'page=1&'
                          'one_way=true&'
                          'token={token}'.format(departure_at=tomorrow, token=api_token))

    data = json.loads(my_req.text)
    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    return construct_answer(data)
