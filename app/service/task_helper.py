from typing import Union, Dict, List

from app.model.task import Task
from app.service.task_manager import TaskManager
from app.service import logger
from app import db



def refreshTask(task) -> None:
    task.finished = True
    task.result = TaskManager.FutureDict[task.id].result()
    db.session.commit()


def getTaskInfo(task) -> Dict[str, Union[int, str]]:
    if (not task.finished and TaskManager.FutureDict.get(task.id, None) != None and
        TaskManager.FutureDict[task.id].done()):

        refreshTask(task)
        del TaskManager.FutureDict[task.id]        
        logger.info(f"Task {task.id} result setted")

    return {
        "status": "finished" if task.finished else "processing",
        "result": task.result,
        "description": str(task)
    }


def getTaskInfoById(task_id: int) -> Dict[str, Union[int, str]]:
    task = Task.query.filter_by(id=task_id).first()
    return getTaskInfo(task)


def getAllTask() -> List[Dict[str, Union[int, str]]]:
    return [ getTaskInfo(task) for task in Task.query.all() ]