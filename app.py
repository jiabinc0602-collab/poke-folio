from flask import Flask, render_template, request, redirect, url_for
from db_service import (
    search_card_in_db, get_all_sets_from_db, get_all_portfolio_cards, 
    add_card_to_portfolio, update_card_quantity, get_card_details_for_portfolio # NEW
)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods =['GET'])
def search():
    card_name = request.args.get('card_name')
    print(f"Searching for card: {card_name}")
    card_data = search_card_in_db(card_name)
    return render_template('results.html', card = card_data)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/sets')
def setsIndex():
    all_sets = get_all_sets_from_db()
    return render_template('sets.html', set_list = all_sets)

@app.route('/add_to_portfolio/<card_id>')
def add_to_portfolio(card_id):
    card_details = get_card_details_for_portfolio(card_id)
    if card_details:
        market_price = card_details['market_price']
        add_card_to_portfolio(card_id, 1, market_price)
    return redirect(url_for('/'))

@app.route('/portfolio')
def view_portfolio():
    collection = get_all_portfolio_cards()
    total_value = sum(card['subtotal'] for card in collection)
    total_value_displayed = f"{total_value:.2f}"
    return render_template('portfolio.html', collection = collection, total_value = total_value_displayed)


@app.route('/update_quantity', methods=['POST'])
def update_quantity():
    card_id = request.form.get('card_id')
    new_quantity = request.form.get('quantity',type=int)
    if card_id and new_quantity is not None:
        update_card_quantity(card_id, new_quantity)
    return redirect(url_for('view_portfolio'))