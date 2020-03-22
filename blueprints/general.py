
from flask import Blueprint
from utils.responses import ApiResult


bp = Blueprint('general', __name__, url_prefix='/general')


@bp.route("/infrastructure_types", methods=['GET'])
def get_infrastructure_types():
    """"Return all the available infrastrucutre types."""

    # TODO: Use DAOs to get all infrastructures

    return ApiResult(infrastructure_types=["type1", "type2"])


@bp.route("/damage_types", methods=['GET'])
def get_damage_types():
    # TODO: Use DAOs to get all damage types available.

    return ApiResult(damage_types=['damage1', 'damage2'])


@bp.route("/tags", methods=['GET'])
def get_tags():
    # TODO: Use DAOs to get all tags available.

    return ApiResult(damage_types=['tag1', 'tag2'])


