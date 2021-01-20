from app.service.task_manager import TaskManager
from concurrent.futures import wait

import json
import pytest



@pytest.mark.parametrize("data, res", [
    pytest.param({"x": 1, "y": 1, "operator": '+'}, {"code": 200}),
    pytest.param({"x": -1, "y": 1, "operator": '-'}, {"code": 200}),
    pytest.param({"x": 1, "y": -1, "operator": '*'}, {"code": 200}),
    pytest.param({"x": -1, "y": -1, "operator": '/'}, {"code": 200}),
    pytest.param({"x": 0, "y": 1, "operator": '*'}, {"code": 200}),
    pytest.param({"x": 0, "y": 1, "operator": '/'}, {"code": 200}),
    pytest.param({"x": 1, "y": 0, "operator": '/'}, {"code": 400}),
    pytest.param({"y": 0, "operator": '+'}, {"code": 400}),
    pytest.param({"x": 1, "operator": '+'}, {"code": 400}),
    pytest.param({"x": 1, "y": 0}, {"code": 400}),
    pytest.param({"x": 'f', "y": 2, "operator": '-'}, {"code": 400}),
    pytest.param({"x": 1.2, "y": 2, "operator": '*'}, {"code": 400}),
    pytest.param({"x": 1, "y": 'g', "operator": '+'}, {"code": 400}),
    pytest.param({"x": 3, "y": -5.6, "operator": '-'}, {"code": 400}),
    pytest.param({"x": 3, "y": 4, "operator": 'p'}, {"code": 400}),
    
])
def test_new_task_request(client, data, res):
    response = client.post("/new_task", data=json.dumps(data), content_type='application/json')
    resp_obj = json.loads(response.data.decode())
    assert response.status_code == res["code"]

    if response.status_code == 200:
        print(type(resp_obj))
        assert resp_obj["task_id"] == 1
    
    if response.status_code == 400:
        assert 'messages' in resp_obj



@pytest.mark.parametrize("data, res", [
    pytest.param({"task_id": 5}, {"code": 400}),
    pytest.param({"task_id": 'f'}, {"code": 400}),
    pytest.param({"random_name": 13}, {"code": 400}),
    pytest.param({"task_id": -5}, {"code": 400}),
    pytest.param({"task_id": 0}, {"code": 400}),
])
def test_check_task_request(client, data, res):
    response = client.post("/check_task", data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400



def test_check_existance_task_request(client):
    response = client.post(
        "/new_task",
        data=json.dumps({"x": 15, "y": 16, "operator": '+'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    task_id = json.loads(response.data.decode())["task_id"]
    assert task_id == 1

    check_response = client.post(
        "/check_task",
        data=json.dumps({"task_id": task_id}),
        content_type='application/json'
    )
    assert check_response.status_code == 200



def test_check_task_result(client):
    response = client.post(
        "/new_task",
        data=json.dumps({"x": 15, "y": 16, "operator": '+'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    task_id = json.loads(response.data.decode())["task_id"]
    assert task_id == 1

    wait([TaskManager.FutureDict[task_id]])

    check_response = client.post(
        "/check_task",
        data=json.dumps({"task_id": task_id}),
        content_type='application/json'
    )
    dict_resp = json.loads(check_response.data.decode())
    assert check_response.status_code == 200
    assert dict_resp["status"] == "finished"
    assert dict_resp["result"] == 31



def test_check_all_task_result(client):
    response = client.post(
        "/new_task",
        data=json.dumps({"x": 10, "y": 2, "operator": '/'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    task_id = json.loads(response.data.decode())["task_id"]
    assert task_id == 1

    wait([TaskManager.FutureDict[task_id]])

    all_response = client.post(
        "/get_all_tasks",
        content_type='application/json'
    )
    dict_resp = json.loads(all_response.data.decode())
    assert all_response.status_code == 200
    assert len(dict_resp["tasks"]) == 1
    assert dict_resp["tasks"][0]["status"] == "finished"
    assert dict_resp["tasks"][0]["result"] == 5

