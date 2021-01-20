from app.service.task_manager import TaskManager
from app.service.task_helper import getTaskInfoById
from app.model.task import Task

from concurrent.futures import wait
import pytest



@pytest.mark.parametrize("data, res", [
    pytest.param((1, 1, '+'), 2),
    pytest.param((1, -1, '+'), 0),
    pytest.param((-1, 1, '+'), 0),
    pytest.param((1, 0, '+'), 1),
    
    pytest.param((1, -1, '-'), 2),
    pytest.param((-1, 1, '-'), -2),
    pytest.param((0, -1, '-'), 1),
    pytest.param((1, 0, '-'), 1),

    pytest.param((1, 1, '*'), 1),
    pytest.param((-1, 1, '*'), -1),
    pytest.param((1, -1, '*'), -1),
    pytest.param((-1, -1, '*'), 1),
    pytest.param((3, 2, '*'), 6),
    pytest.param((10, 0, '*'), 0),

    pytest.param((1, 1, '/'), 1),
    pytest.param((1, 2, '/'), 0.5),
    pytest.param((4, 2, '/'), 2),
    pytest.param((-4, 1, '/'), -4),
    pytest.param((6, -2, '/'), -3),
    pytest.param((-3, -2, '/'), 1.5),
    pytest.param((0, -2, '/'), 0),
])
def test_fut_result(app, data, res):
    with app.app_context():
        task_id = TaskManager.createTask(*data)

        wait([TaskManager.FutureDict[task_id]])

        assert TaskManager.FutureDict[task_id].result() == res



@pytest.mark.parametrize("data, res", [
    pytest.param((1, 1, '*'), 1),
    pytest.param((1, 1, '+'), 2),
    pytest.param((1, 1, '-'), 0),
    pytest.param((1, 1, '/'), 1),
])
def test_db_refresh(app, data, res):
    with app.app_context():
        task_id = TaskManager.createTask(*data)
        assert Task.query.filter_by(id=task_id).first().finished == False

        wait([TaskManager.FutureDict[task_id]])

        task_info = getTaskInfoById(task_id)
        assert TaskManager.FutureDict.get(task_id, None) == None
        assert Task.query.filter_by(id=task_id).first().finished == True
        assert task_info["result"] == res

        