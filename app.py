from flask import Flask, render_template, request
from api_service import search_card_by_name
from db_service import search_card_in_db

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
