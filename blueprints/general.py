"""
General Module: general.py
==========================
Holds the endpoints that allow the retrieval of non sensitive information. Holds a blueprint object
 that is used to create the routes for this module.
"""

from flask import Blueprint, jsonify
from utils.responses import ApiResult
from database.daos.get import get_infrastructure_list, get_damage_list, get_tags_list

bp = Blueprint('general', __name__, url_prefix='/general')
"""Instance of a Flask "Blueprint" class to implement a custom endpoint groups."""


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

    return jsonify(get_infrastructure_list()), 200


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
    return jsonify(get_damage_list()), 200


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
    return jsonify(get_tags_list()), 200
