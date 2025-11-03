from api_service import get_cards_by_page,get_all_sets
from db_service import insert_card, setup_database, insert_set
import time

page_num = 1
total_fetched = 0
total_count = 1
setup_database()
while (total_fetched < total_count):
    data = get_cards_by_page(page_num)

    if data == "STOP":
        break 
    elif not data:
        print(f"Failed to get page {page_num}, retrying in 5 seconds...")
        time.sleep(5)
        continue
    results = data.get('data')

    total_count = data.get('totalCount')
    
    for card in results:
        insert_card(card)
    
    page_num = page_num+1
    total_fetched += len(results)

    time.sleep(1)

sets_data = None
max_retries = 3
for attempt in range(max_retries):
    print(f"Fetching all sets (Attempt {attempt + 1}/{max_retries})...")
    
    sets_data = get_all_sets()
    
    if sets_data:
        break
    
    if attempt < max_retries - 1:
        print("Set fetch failed. Retrying in 10 seconds...")
        time.sleep(10)
    else:
        print("FATAL: All set fetch attempts failed.")

if not sets_data:
    print("Could not fetch set data. Skipping set import.")
else:
    results = sets_data.get('data')
    
    for set_data in results:
        insert_set(set_data)
    
    print("Successfully inserted all sets into database.")