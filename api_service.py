import requests

url = "https://api.pokemontcg.io/v2/cards"
API_KEY = "0336902f-9595-4a3d-8d12-115c9d4619f1"
headers = {
    "X-Api-Key": API_KEY
}

def search_card_by_name(name):

    params = {
        "q": f'name:"{name}"'
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
    
        card_results = data.get('data')
        if card_results and len(card_results) > 0:
            return card_results[0]
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"API request failed:{e}")
        return None

    
    
