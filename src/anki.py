import json
import urllib.request

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

def findCard(word, deck="Russian::A::1-RU-EN", verbose=False):
    query = "deck:" + deck + " Word:" + word
    card_ids = invoke('findCards', query=query)
    if verbose: print(query, card_ids)
    cards = invoke('cardsInfo', cards=card_ids)
    
    if len(cards) == 0: return None
    assert len(cards) == 1, f"Ambigous results in ANKI ({len(cards)}: {str(cards)}"
    card = cards[0]
    
    trans = card['fields']['Meaning']['value']
    return trans, card
