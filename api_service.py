import requests

url = "https://api.pokemontcg.io/v2/cards"
set_url = "https://api.pokemontcg.io/v2/sets"
API_KEY = "0336902f-9595-4a3d-8d12-115c9d4619f1"
headers = {
    "X-Api-Key": API_KEY
}

def search_card_by_name(name):

    params = {
        "q": f'name:"{name}"'
    }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
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

def get_cards_by_page(page_number):
    params = {
        "page": page_number,
        "pageSize": 250
    }
    try: 
        response = requests.get(url, headers = headers, params=params)
        response.raise_for_status()
        
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print("API: Reached end of data (404)")
            return "STOP"
        else:
            print(f"API request failed: {e}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None

def get_all_sets():
    try: 
        response = requests.get(set_url, headers = headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None