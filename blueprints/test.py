"""
general.py
====================================
Blueprint class that holds the endpoints that allows the retrieval of non sensitive information. Holds a blueprint object
 that is used to create the routes for this module.
"""

from flask import Blueprint, jsonify
from utils.responses import ApiResult
# from database.mock_db import *
from TS_DAOs.schema_DB import *
from TS_DAOs.dao_TS import *
import json


bp = Blueprint('general', __name__, url_prefix='/general')


@bp.route("/infrastructure_types", methods=['GET'])
def get_infrastructure_types():
    """
        Get the list of the available infrastructure types within the database.
        Returns
        -------
              Response
                JSON Object containing the list of infrastructure types.
        Example
        -------
            ["Infra1", "Infra2", ...]
    """
    list = []
    for infra in get_infrastructure_list():
        list.append(infra.infrastructureType)
    return jsonify(list)


@bp.route("/damage_types", methods=['GET'])
def get_damage_types():
    """
        Get the list of the available damage types within the database.
        Returns
        -------
            Response
                JSON Object containing the list of damage types.
        Example
        -------
            ["damage1","damage2", ...]
    """
    list = []
    for d in get_damage_list():
        list.append(d.damageType)
    return jsonify(list)


@bp.route("/tags", methods=['GET'])
def get_tags():
    """
        Get the list of all the available tags within the database. (Tags are created by collaborators.)
        Returns
        -------
            ApiResult
                JSON Object containing the list of tags.
        Example
        -------
            ["Tag1", "Tag2", ...]
    """
    list = []
    for t in get_tags_list():
        list.append(t.tagItem)
    return jsonify(list)
    