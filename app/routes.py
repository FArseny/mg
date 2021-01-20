from flask import Blueprint, jsonify
from flask import send_from_directory, request
import logging

from app.util.validation import NewTaskInputs, GetTaskResultInputs
from app.util.invalid_usage import InvalidUsage
from app.service.task_manager import TaskManager
from app.service.task_helper import getTaskInfoById, getAllTask



bp = Blueprint('index', __name__, url_prefix='')
logger = logging.getLogger(__name__)


@bp.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
   response = jsonify(error.to_dict())
   response.status_code = error.status_code
   return response


@bp.route('/')
def index():
    return send_from_directory('static/templates', "index.html")


@bp.route("/static/<path:filename>")
def downloadStaticFile(filename):
    return send_from_directory('static/', filename)


@bp.route("/new_task", methods=["POST"])
def newTask():
    inputs = NewTaskInputs(request)
    if not inputs.validate():
        logger.warn(f"Cant create task with params: {request.json}")
        raise InvalidUsage(inputs.errors)

    
    x, y, operator = request.json["x"], request.json["y"], request.json["operator"]
    task_id = TaskManager.createTask(x, y, operator)
    logger.info(f"Create task {x}{operator}{y} with id {task_id}")

    return jsonify({"task_id": task_id})


@bp.route("/check_task", methods=["POST"])
def getResult():
    inputs = GetTaskResultInputs(request)
    if not inputs.validate():
        logger.warn(f"Cant get task presented by: {request.json}")
        raise InvalidUsage(inputs.errors)
    
    task_id = request.json["task_id"]
    info = getTaskInfoById(task_id)
    logger.info(f"Returning task info with id={task_id}")
    
    return jsonify(info)


@bp.route("/get_all_tasks", methods=["POST"])
def getAllTasks():
    tasks = getAllTask()
    logger.info(f"Returning all tasks; len={len(tasks)}")
    return jsonify({"tasks": tasks})
