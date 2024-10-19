from flask import Blueprint, Response, jsonify, request


usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@usuarios_bp.route("", methods=["GET"])
def get_all_users():
    all_users = [{"id":1, "name":"bob"},{"id":2, "name":"carl"}]
    return jsonify(all_users)



@usuarios_bp.route("", methods=["POST"])
def create_usuario():
    d = request.json
    print(d)
    #return Response(status=204)
    return jsonify(d), 201