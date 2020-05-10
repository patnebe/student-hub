from marshmallow import Schema, fields


class Nanodegree_Input_Schema(Schema):
    """A marshmallow schema which validates the JSON payload accompanying POST requests to create a new nanodegree"""

    title = fields.String(required=True)
    description = fields.String(required=True)
