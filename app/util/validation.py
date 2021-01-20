from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
from wtforms.validators import ValidationError
from app.util.operator_helper import Operator
from app import db
from app.model.task import Task


NEW_TASK_SCHEMA = {
    'type': 'object',
    'properties': {
        'x': {'type': 'integer'},
        'y': {'type': 'integer'},
        'operator': {'enum': [op.value for op in Operator]}
    },
    'required': ['x', 'y', 'operator']
}


GET_TASK_RESULT_SCHEMA = {
    'type': 'object',
    'properties': {
        'task_id': {'type': 'integer'}
    },
    'required': ['task_id']
}


def zeroDivisionChecker(form, field):
    if (field.data.get('y', None) == 0 and
        field.data.get('operator', None) == Operator.DIVIDE.value):

        raise ValidationError("Zero division forbidden")


class NewTaskInputs(Inputs):
    json = [JsonSchema(schema=NEW_TASK_SCHEMA), zeroDivisionChecker]


def taskExistanceChecker(form, field):
    if (field.data.get('task_id', None) != None and
        isinstance(field.data["task_id"], int) and 
        len(Task.query.filter_by(id=field.data["task_id"]).all()) == 0):

        raise ValidationError("No task exist with such id")


class GetTaskResultInputs(Inputs):
    json = [JsonSchema(schema=GET_TASK_RESULT_SCHEMA), taskExistanceChecker]


