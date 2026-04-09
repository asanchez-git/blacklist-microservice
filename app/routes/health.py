from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "blacklist microservice running"
    }), 200


@health_bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "message": "service is healthy"
    }), 200