from marshmallow import Schema, fields, ValidationError


class Login_Input_Validator(Schema):
    """
    A marshmallow schema to validate login data
    """
    email = fields.Email(required=True)
    password = fields.String(required=True)


class Signup_Input_Validator(Schema):
    """
    A marshmallow schema to validate signup data
    """
    email = fields.Email(required=True)
    password = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
