# TODO: Add authentication decorator as needed

from flask import Blueprint, g, current_app, request, session, make_response, jsonify
from utils.responses import ApiResult, ApiException
from uuid import uuid4

from utils.exceptions import TellSpaceMethodNotAllowed

bp = Blueprint('documents', __name__, url_prefix='/api/documents')


@bp.route('/', methods=['GET'])
def get_documents():
    """ Objective:
           Return a list of documents based on the body request parameters. The parameters will be used to filter the
           information within the metadata of the documents. Documents returned will be those from the res.
           User id will be retrieved from the session object.

        Pre-conditions:
           Client has valid session token.
           Request body must be valid.


        Args:
           None

        Returns:
          ApiResult where value is a list of documents metadata fitting the criteria in the request body.

        Author:
           Roberto Y. Guzman

        Date:
          March 16, 2020
    """
    temp_response = {
        "response": 'List of documents metadata fitting the criteria in the request body.'
    }
    return ApiResult(
        value=temp_response
    )


@bp.route('/create', methods=['GET', 'POST'])
def create_document():
    if not(request.method == 'POST'):
        raise TellSpaceMethodNotAllowed()

    temp_response = {
        "response": f'Hi this is a test. The document you created is {uuid4()}',
        "method": request.method
    }
    return ApiResult(
        value=temp_response
    )


@bp.route('/<doc_id>', methods=['GET'])
def get_document_by_id(doc_id):
    temp_response = {
        "response":{
            "doc_id": doc_id,
            "message": 'Here is the doc_id param that you gave me'
        }
    }
    return ApiResult(value=temp_response)


@bp.route('/<doc_id>/edit/title', methods=['PUT'])
def update_document_title(doc_id):
    temp_response = {
        "response":{
            "doc_id": doc_id,
            "message": 'You will edit the title for the document with the given doc_id'
        }
    }
    return ApiResult(value=temp_response)


@bp.route('/<doc_id>/edit/description', methods=['PUT'])
def update_document_description(doc_id):
    temp_response = {
        "response":{
            "doc_id": doc_id,
            "message": 'You will edit the description for the document with the given doc_id.'
        }
    }
    return ApiResult(value=temp_response)


@bp.route('/<doc_id>/edit/timeline', methods=['PUT'])
def update_document_timeline(doc_id):
    temp_response = {
        "response":{
            "doc_id": doc_id,
            "message": 'You will edit the timeline for the document with the given doc_id.'
        }
    }
    return ApiResult(value=temp_response)


@bp.route('/<doc_id>/edit/section', methods=['PUT'])
def update_document_section(doc_id):
    temp_response = {
        "response":{
            "doc_id": doc_id,
            "message": 'You will edit a section of the document with the given doc_id.'
        }
    }
    return ApiResult(value=temp_response)


@bp.route('/<doc_id>/edit/infrastructure_types', methods=['PUT'])
def update_document_infrastructure_types(doc_id):
    temp_response = {
        "response":{
            "doc_id": doc_id,
            "message": 'You will edit the infrastructure types of the document with the given doc_id.'
        }
    }
    return ApiResult(value=temp_response)


@bp.route('/<doc_id>/edit/damage_types', methods=['PUT'])
def update_document_damage_types(doc_id):
    temp_response = {
        "response":{
            "doc_id": doc_id,
            "message": 'You will edit the damage types of the document with the given doc_id.'
        }
    }
    return ApiResult(value=temp_response)


@bp.route('/<doc_id>/edit/actors', methods=['PUT'])
def update_document_actors(doc_id):
    temp_response = {
        "response":{
            "doc_id": doc_id,
            "message": 'You will edit the actors of the document with the given doc_id.'
        }
    }
    return ApiResult(value=temp_response)


@bp.route('/<doc_id>/edit/locations', methods=['PUT'])
def update_document_locations(doc_id):
    temp_response = {
        "response":{
            "doc_id": doc_id,
            "message": 'You will edit the locations of the document with the given doc_id.'
        }
    }
    return ApiResult(value=temp_response)


@bp.route('/<doc_id>/edit/authors', methods=['PUT'])
def update_document_authors(doc_id):
    temp_response = {
        "response":{
            "doc_id": doc_id,
            "message": 'You will edit the authors of the document with the given doc_id.'
        }
    }
    return ApiResult(value=temp_response)


@bp.route('/<doc_id>/edit/tags', methods=['PUT'])
def update_document_tags(doc_id):
    temp_response = {
        "response":{
            "doc_id": doc_id,
            "message": 'You will edit the tags of the document with the given doc_id.'
        }
    }
    return ApiResult(value=temp_response)


@bp.before_request
def before_requests():
    print(f'Before requests in /api/documents')

