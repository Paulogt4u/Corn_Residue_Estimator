from flask import Flask, render_template, request, jsonify
import rasterio
import numpy as np

app = Flask(__name__)

# Load yield map TIFFs in read mode
yield_maps = {
    'M1': rasterio.open('path/to/M1.tif', 'r'),
    'L1': rasterio.open('path/to/L1.tif', 'r')
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select-region')
def select_region():
    return render_template('select-region.html')

@app.route('/yield-map', methods=['POST'])
def yield_map():
    data = request.form
    country = data.get('country')
    state = data.get('state')
    field = data.get('field')
    return render_template('yield-map.html', country=country, state=state, field=field)

@app.route('/calculate-residue', methods=['POST'])
def calculate_residue():
    data = request.json
    field = data['field']
    zone = data['zone']
    point_x = int(data['point']['x'])
    point_y = int(data['point']['y'])

    yield_map = yield_maps[field]
    if not (0 <= point_x < yield_map.width and 0 <= point_y < yield_map.height):
        return jsonify(message="Selected point is out of the map bounds."), 400
    value = yield_map.read(1, window=rasterio.windows.Window(point_x, point_y, 1, 1))
    coefficient = {'HS': 0.80, 'MS': 0.70, 'US': 0.75, 'LS': 0.4}[zone]
    residue = np.sum(value) * coefficient

    return jsonify(message=f"The corn residue amount is {residue:.2f} Kg/ha")

if __name__ == '__main__':
    app.run(debug=True)
