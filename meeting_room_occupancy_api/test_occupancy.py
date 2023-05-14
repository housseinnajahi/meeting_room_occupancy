import json

import pytest

from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_status_code_ok(client):
    response = client.get('/api/sensors')
    assert response.status_code == 200


def test_status_code_not_ok(client):
    response = client.post('/api/sensors')
    assert response.status_code != 200


def test_sensors(client):
    response = client.get('/api/sensors')
    data = response.json
    assert data['sensors'] == []


def test_add_sensor(client):
    response = client.post('/api/webhook', data=json.dumps({"sensor":"cbd","ts":"2018-11-14T13:34:49Z","in":3,"out":2}),
                           headers={"Content-Type": "application/json"})
    data = response.json
    print(data)
    assert data['error'] is False
    response = client.post('/api/webhook',
                           data=json.dumps({"sensor": "cbd", "ts": "2018-11-14T13:34:49Z", "out": 1}),
                           headers={"Content-Type": "application/json"})
    data = response.json
    print(data)
    assert data['error'] is False
    response = client.post('/api/webhook',
                           data=json.dumps({"sensor": "zcbd", "ts": "2018-11-14T13:34:49Z", "in": 3}),
                           headers={"Content-Type": "application/json"})
    data = response.json
    print(data)
    assert data['error'] is False
    response = client.post('/api/webhook',
                           data=json.dumps({"sensor": "acbd", "in": 3, "out": 3}),
                           headers={"Content-Type": "application/json"})
    data = response.json
    print(data)
    assert data['error'] is False
    response = client.post('/api/webhook',
                           data=json.dumps({"ts": "2018-11-14T13:34:49Z", "in": 3, "out": 2}),
                           headers={"Content-Type": "application/json"})
    data = response.json
    print(data)
    assert data['error'] is True


def test_occupancy(client):
    response = client.get('/api/occupancy')
    data = response.json
    assert data['inside'] == 0

    client.post('/api/webhook',
                           data=json.dumps({"sensor": "cbd", "ts": "2023-11-14T13:34:49Z", "in": 3, "out": 0}),
                           headers={"Content-Type": "application/json"})
    response = client.get('/api/occupancy?sensor=cbd')
    data = response.json
    assert data['inside'] == 3
    client.post('/api/webhook',
                           data=json.dumps({"sensor": "cbd", "ts": "2022-11-14T13:34:49Z", "in": 2, "out": 0}),
                           headers={"Content-Type": "application/json"})
    response = client.get('/api/occupancy?sensor=cbd')
    data = response.json
    assert data['inside'] == 5

    response = client.get('/api/occupancy?sensor=cbd&atInstant=2023-05-14T13:34:49Z')
    data = response.json
    assert data['inside'] == 2

    client.post('/api/webhook',
                           data=json.dumps({"sensor": "abce", "ts": "2023-11-14T13:34:49Z", "in": 3, "out": 1}),
                           headers={"Content-Type": "application/json"})
    response = client.get('/api/occupancy?sensor=abce')
    data = response.json
    assert data['inside'] == 2