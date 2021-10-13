from marshmallow import Schema, fields, validate

class LocationSchema(Schema):
    id = fields.Integer(
        validate=[validate.Range(min=1, error="Value must be greater than 0")])
    person_id = fields.Integer(
        validate=[validate.Range(min=1, error="Value must be greater than 0")])
    latitude = fields.Float(
        attribute="latitude",
        validate=[validate.Range(min=-90, max=90, error="Value must be between -90 and 90")])
    longitude = fields.Float(
        attribute="longitude",
        validate=[validate.Range(min=-180, max=180, error="Value must be between -180 and 180")])
    creation_time = fields.DateTime()
