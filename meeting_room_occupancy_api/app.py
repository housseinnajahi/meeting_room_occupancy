from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


sensors_data = {}


@app.route('/api/webhook', methods=['POST'])
def add_sensor_data():
    try:
        data = request.json
        if 'sensor' not in data.keys():
            return jsonify({'error': True, 'message': 'missing data'})
        if data.get('sensor') not in sensors_data.keys():
            sensors_data.update({data.get('sensor'): [data]})
        else:
            sensors_data.get(data.get('sensor')).append(data)
        return jsonify({'error': False, 'message': 'data received successfully'})
    except:
        return jsonify({'error': True, 'message': 'error while handling data update'})


@app.route('/api/sensors', methods=['GET'])
def get_sensors():
    return jsonify({'sensors': list(sensors_data.keys())})


@app.route('/api/occupancy', methods=['GET'])
def get_occupancy():
    args = request.args
    if not args.get('sensor'):
        jsonify({'inside': 0})
    inside = get_inside(sensor=args.get('sensor'), at_instant=args.get('atInstant', None))
    return jsonify({'inside': inside})


def get_inside(sensor, at_instant=None):
    try:
        if not at_instant:
            inside_list = [data.get('in', 0) - data.get('out', 0) for data in sensors_data.get(sensor, [])]
            return sum(inside_list)
        timestamp = datetime.strptime(at_instant, '%Y-%m-%dT%H:%M:%SZ').timestamp()
        inside_list = [data.get('in', 0) - data.get('out', 0) for data in sensors_data.get(sensor, []) if at_instant and
                       datetime.strptime(data.get('ts', 0), '%Y-%m-%dT%H:%M:%SZ').timestamp() <= timestamp]
        return sum(inside_list)
    except:
        return 0

if __name__ == '__main__':
    app.run()
