from api_service import get_cards_by_page
from db_service import insert_card, setup_database
import time

page_num = 1
total_fetched = 0
total_count = 1
setup_database()
while (total_fetched < total_count):
    data = get_cards_by_page(page_num)

    if not data:
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