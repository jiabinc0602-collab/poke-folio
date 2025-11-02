import sqlite3


def setup_database():
    conn = sqlite3.connect('pokefolio.db')
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS cardData (
                   id TEXT PRIMARY KEY,
                   name TEXT NOT NULL,
                   type TEXT NOT NULL,
                   image_url TEXT,
                   market_price REAL NOT NULL,
                   price_type TEXT NOT NULL
                   )
    ''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS cardSets (
                   setId TEXT PRIMARY KEY,
                   setName TEXT NOT NULL,
                   setImage_url TEXT
                   )
    ''')
    conn.commit()
    conn.close()

def insert_card(card_data):
    conn = sqlite3.connect('pokefolio.db')
    cursor = conn.cursor()
    try:
        card_id = card_data.get('id')
        card_name = card_data.get('name')
        types_list = card_data.get('types', [])
        card_type = ','.join(types_list)
        image_url = card_data.get('images', {}).get('small')
        prices_dict = card_data.get('tcgplayer', {}).get('prices', {})
        market_price = 0.0
        price_type = "N/A"
        if 'holofoil' in prices_dict:
            market_price = prices_dict['holofoil'].get('market',0.0)
            price_type = "Holofoil"
        elif 'reverseHolo' in prices_dict:
            market_price = prices_dict['reverseHolo'].get('market',0.0)
            price_type = "Reverse Holo"
        elif 'normal' in prices_dict:
            market_price = prices_dict['normal'].get('market',0.0)
            price_type = "Normal"
        elif 'fullArt' in prices_dict:
            market_price = prices_dict['fullArt'].get('market',0.0)
            price_type = "Full Art"
        else:
            market_price = 0.0
        
        
        pulled = (
            card_id,
            card_name,
            card_type,
            image_url,
            market_price,
            price_type
        )

        cursor.execute("INSERT OR IGNORE INTO cardData(id, name, type, image_url, market_price, price_type) VALUES (?,?,?,?,?,?)", pulled)
        conn.commit()

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

def insert_set(set_data):
    conn = sqlite3.connect('pokefolio.db')
    cursor = conn.cursor()
    set_id = set_data.get('id')
    set_name = set_data.get('name')
    set_image_url = set_data.get('images', {}).get('logo')
    pulled = (
        set_id,
        set_name,
        set_image_url
    )
    try:
        cursor.execute("INSERT OR IGNORE INTO cardSets(setId, setName, setImage_url) VALUES (?,?,?)", pulled)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

def search_card_in_db(card_name):
    conn = sqlite3.connect('pokefolio.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql_query = "SELECT * FROM cardData WHERE name LIKE ?"
    search = f"%{card_name}%"
    
    cursor.execute(sql_query,(search,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_all_sets_from_db():
    conn = sqlite3.connect('pokefolio.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql_query = "SELECT * FROM cardSets"
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    conn.close()
    return rows
