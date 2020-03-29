
from flask import Blueprint
from utils.responses import ApiResult
from daos.dao_TS import get_infrastructure_list, get_tags_list, get_damage_list
from database.mock_db import *

bp = Blueprint('general', __name__, url_prefix='/general')


@bp.route("/infrastructure_types", methods=['GET'])
def get_infrastructure_types():
    """"Return all the available infrastructure types."""
    return ApiResult(infrastructure_types=get_infrastructure_list())


@bp.route("/damage_types", methods=['GET'])
def get_damage_types():
    return ApiResult(damage_types=get_damage_list())


@bp.route("/tags", methods=['GET'])
def get_tags():
    return ApiResult(tags=get_tags_list())


