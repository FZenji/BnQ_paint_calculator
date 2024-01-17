from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate_paint', methods=['POST'])
def calculate_paint():
    data = request.get_json()
    wall_area = data.get('wallArea')
    paint_coverage = data.get('paintCoverage')

    if wall_area is None or paint_coverage is None:
        return jsonify({'error': 'Invalid input'}), 400

    paint_needed = wall_area / paint_coverage
    return jsonify({'paintNeeded': paint_needed})

if __name__ == '__main__':
    app.run(debug=True)
