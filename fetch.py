import os
import sqlite3
import requests

url = "https://api.pokemontcg.io/v2/cards"
API_KEY = "0336902f-9595-4a3d-8d12-115c9d4619f1"
headers = {
    "X-Api-Key": API_KEY
}
conn = sqlite3.connect('pokefolio.db')
cursor = conn.cursor()

create_table_sql="""
    CREATE TABLE IF NOT EXISTS pokemon_cards(
        id TEXT PRIMARY KEY,
        name TEXT,
        types TEXT,
        image TEXT
    );
"""
insert_sql = """
        INSERT INTO pokemon_cards (id, name, types, image)
        VALUES (?, ?, ?, ?)"""

def get_cards_page(page, page_size=250):
    params = {
        "page": page,
        "pageSize": page_size
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

all_cards=[]

page_num = 1
total_count = 1
while len(all_cards) < total_count:
    try:
        data = get_cards_page(page_num)
        total_count = data['totalCount']
        all_cards.extend(data)
        page_num += 1
        print(f"Fetched page {page_num - 1}, total cards fetched: {len(all_cards)}")
    except Exception as e:
        print(f"Error fetching page {page_num}: {e}")
        break
print(f"Total cards fetched: {len(all_cards)}")
cursor.execute(create_table_sql)