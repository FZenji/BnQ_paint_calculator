from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate_paint', methods=['POST'])
def calculate_paint():
    data = request.json()
    print(data)
    return jsonify({'paintNeeded': 1})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
