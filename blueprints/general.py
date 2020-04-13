
from flask import Blueprint
from utils.responses import ApiResult
from daos.dao_TS import get_infrastructure_list, get_tags_list, get_damage_list
from database.mock_db import *
from database.schema_DB import *
import json

bp = Blueprint('general', __name__, url_prefix='/general')


@bp.route("/infrastructure_types", methods=['GET'])
def get_infrastructure_types():
    """"Return all the available infrastructure types."""
    list = []
    for infra in Infrastructure.objects():
        list.append(infra.infrastructureType)
    return ApiResult(value=list)


@bp.route("/damage_types", methods=['GET'])
def get_damage_types():
    list = []
    for d in Damage.objects():
        list.append(d.damageType)
    return ApiResult(value=list)


@bp.route("/tags", methods=['GET'])
def get_tags():
    list = []
    for t in Tag.objects():
        list.append(t.tagItem)
    return ApiResult(value=list)


