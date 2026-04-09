from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import Blacklist
from app.schemas.blacklist_schema import BlacklistCreateSchema, BlacklistResponseSchema

blacklists_bp = Blueprint("blacklists", __name__)

create_schema = BlacklistCreateSchema()
response_schema = BlacklistResponseSchema()


def get_client_ip() -> str:
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.remote_addr or "unknown"


def is_authorized() -> bool:
    auth_header = request.headers.get("Authorization", "")
    expected_token = current_app.config["STATIC_BEARER_TOKEN"]

    if not auth_header.startswith("Bearer "):
        return False

    token = auth_header.split(" ", 1)[1].strip()
    return token == expected_token


@blacklists_bp.route("/blacklists", methods=["POST"])
def create_blacklist():
    if not is_authorized():
        return jsonify({"message": "Unauthorized"}), 401

    json_data = request.get_json(silent=True)
    if not json_data:
        return jsonify({"message": "Invalid or missing JSON body"}), 400

    try:
        data = create_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400

    blacklist_entry = Blacklist(
        email=data["email"],
        app_uuid=str(data["app_uuid"]),
        blocked_reason=data.get("blocked_reason"),
        ip_address=get_client_ip(),
    )

    try:
        db.session.add(blacklist_entry)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        print("INTEGRITY ERROR REAL:", str(e.orig))
        return jsonify({
            "message": "Database integrity error",
            "detail": str(e.orig)
        }), 409

    response_data = response_schema.dump({
        "message": "Email added to blacklist successfully",
        "email": blacklist_entry.email,
        "app_uuid": blacklist_entry.app_uuid,
        "blocked_reason": blacklist_entry.blocked_reason,
        "ip_address": blacklist_entry.ip_address,
        "created_at": blacklist_entry.created_at,
    })

    return jsonify(response_data), 201

from email_validator import validate_email, EmailNotValidError
from app.schemas.blacklist_schema import (
    BlacklistCreateSchema,
    BlacklistResponseSchema,
    BlacklistCheckResponseSchema,
)

check_response_schema = BlacklistCheckResponseSchema()


@blacklists_bp.route("/blacklists/<string:email>", methods=["GET"])
def check_blacklist(email):
    if not is_authorized():
        return jsonify({"message": "Unauthorized"}), 401

    try:
        valid = validate_email(email, check_deliverability=False)
        normalized_email = valid.email
    except EmailNotValidError:
        return jsonify({"message": "Invalid email format"}), 400

    blacklist_entry = Blacklist.query.filter_by(email=normalized_email).first()

    if blacklist_entry:
        response_data = check_response_schema.dump({
            "email": normalized_email,
            "is_blacklisted": True,
            "blocked_reason": blacklist_entry.blocked_reason,
        })
        return jsonify(response_data), 200

    response_data = check_response_schema.dump({
        "email": normalized_email,
        "is_blacklisted": False,
        "blocked_reason": None,
    })
    return jsonify(response_data), 200