import json
import uuid

def test_add_writer(client):
    fake_data = str(uuid.uuid4())
    resp = client.post(
        '/writer/create',
        data={
            "name": fake_data,
            "age": 10,
            "email": fake_data
        }
    )

    assert resp.status_code == 200
    assert resp.json["name"] == fake_data
    assert resp.json["email"] == fake_data
    assert resp.json["age"] == 10

def test_get_writer(client):
    fake_data = str(uuid.uuid4())
    resp = client.post(
        '/writer/create',
        data={
            "name": fake_data,
            "age": 10,
            "email": fake_data
        }
    )

    get_resp = client.get(
        f'/writer/get/{resp.json["id"]}',
    )
    assert get_resp.status_code == 200
    assert get_resp.json["name"] == fake_data
    assert get_resp.json["email"] == fake_data
    assert get_resp.json["age"] == 10
    

def test_update_writer(client):
    fake_data = str(uuid.uuid4())
    resp = client.post(
        '/writer/create',
        data={
            "name": fake_data,
            "age": 10,
            "email": fake_data
        }
    )

    assert resp.status_code == 200
    assert resp.json["name"] == fake_data
    assert resp.json["email"] == fake_data
    assert resp.json["age"] == 10

    new_data = str(uuid.uuid4())

    up_resp = client.post(
        '/writer/update',
        data={
            "id": resp.json["id"],
            "name": new_data,
            "age": 11,
            "email": new_data
        }
    )

    assert up_resp.status_code == 200

def test_delete_writer(client):
    fake_data = str(uuid.uuid4())
    resp = client.post(
        '/writer/create',
        data={
            "name": fake_data,
            "age": 10,
            "email": fake_data
        }
    )

    assert resp.status_code == 200
    assert resp.json["name"] == fake_data
    assert resp.json["email"] == fake_data
    assert resp.json["age"] == 10

    up_resp = client.post(
        f'/writer/delete/{resp.json["id"]}'
    )

    assert up_resp.status_code == 200
    