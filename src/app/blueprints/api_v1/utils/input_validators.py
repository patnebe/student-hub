from marshmallow import Schema, fields


class Nanodegree_Input_Schema(Schema):
    """A marshmallow schema which validates the JSON payload accompanying POST requests to create a new nanodegree"""

    title = fields.String(required=True)
    description = fields.String(required=True)


class Project_Input_Schema(Schema):
    """A marshmallow schema which validates the JSON payload accompanying POST requests to create a new project"""

    title = fields.String(required=True)


class Question_Input_Schema(Schema):
    """A marshmallow schema which validates the JSON payload accompanying POST requests to create a new question"""

    title = fields.String(required=True)
    details = fields.String(required=True)
    nanodegree_id = fields.Integer(required=True)
    project_id = fields.Integer(required=True)
    github_link = fields.String(allow_none=True)
