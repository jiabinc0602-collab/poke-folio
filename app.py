from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods =['GET'])
def search():
    card_name = request.args.get('name')
    print(f"Searching for card: {card_name}")
    return f"You searched for the card: {card_name}"

if __name__ == '__main__':
    app.run(debug=True)