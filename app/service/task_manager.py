import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Union


from app import db
from app.model.task import Task
from app.util.operator_helper import getOperFunc
from app.service import logger



MAX_WORKERS = int(os.getenv('N_WORKERS') or 5)


class TaskWrapper():

    def __init__(self, x: int, y: int, operation: str, task_id: int):
        self.x = x
        self.y = y
        self.operation = operation
        self.task_id = task_id

    def __call__(self) -> Union[int, float]:
        return self.operation(self.x, self.y)



class TaskManager():

    Pool = ProcessPoolExecutor(MAX_WORKERS)
    FutureDict = dict()

    @staticmethod
    def createTask(x: int, y: int, operator: str) -> int:
        task = Task(x=x, y=y, operator=operator)
        TaskManager.saveTask(task)
        logger.info(f"Task created id={task.id}")

        operation = getOperFunc(operator)
        tw = TaskWrapper(x, y, operation, task.id)
        TaskManager.FutureDict[task.id] = TaskManager.Pool.submit(tw)
    
        return task.id
    

    @staticmethod
    def saveTask(task) -> None:
        db.session.add(task)
        db.session.commit()
