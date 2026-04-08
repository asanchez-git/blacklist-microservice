from marshmallow import Schema, fields, validate


class BlacklistCreateSchema(Schema):
    email = fields.Email(required=True)
    app_uuid = fields.UUID(required=True)
    blocked_reason = fields.String(
        required=False,
        allow_none=True,
        validate=validate.Length(max=255)
    )


class BlacklistResponseSchema(Schema):
    message = fields.String(required=True)
    email = fields.String(required=True)
    app_uuid = fields.String(required=True)
    blocked_reason = fields.String(allow_none=True)
    ip_address = fields.String(required=True)
    created_at = fields.DateTime(required=True)


class BlacklistCheckResponseSchema(Schema):
    email = fields.String(required=True)
    is_blacklisted = fields.Boolean(required=True)
    blocked_reason = fields.String(allow_none=True)