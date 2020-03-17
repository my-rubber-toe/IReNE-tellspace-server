# TODO: Add authentication decorator as needed

from flask import Blueprint, request, json
from utils.responses import ApiResult, ApiException
from utils.validators import *
from marshmallow import ValidationError
from uuid import uuid4


from utils.exceptions import TellSpaceApiError

bp = Blueprint('documents', __name__, url_prefix='/api/documents')


@bp.route('/', methods=['POST'])
def get_documents():
    """ Return a list of documents based on the body request parameters. The parameters will be used to filter the
           information within the metadata of the documents. Documents returned will be those from the res.
           User id will be retrieved from the session object.
    """
    # TODO: Check if user has a valid session token.

    # TODO: Validate the request body object.
    if request.json == {}:
        return ApiException(
            error_type='ApiError',
            message='No data in request body.',
            status=400
        )
    try:
        GetDocumentsValidator().load(request.json)
    except ValidationError as err:
        return ApiException(
            error_type='Validation Error',
            message=err.messages,
            status=400
        )

    # TODO: Use DAOs to retrieve the necessary information.

    return ApiResult(
        message='Valid Data'
    )


@bp.route('/create', methods=['GET', 'POST'])
def create_document():

    if not(request.method == 'POST'):
        return ApiException(error_type='UnauthorizedMethod', message='Method not allowed.', status=400)

    # TODO: Check if user has a valid session token.
    # TODO: Validate the request body object.

    if request.json == {}:
        return ApiException(error_type='Api Error', message='No data in request body.', status=400)

    try:
        body = CreateDocumentValidator().load(request.json)
        # TODO: Use DAOs to create a new document using the collaborator ID.
        return ApiResult(message='Valid Data. Document will be created with the given data', given_data=body)

    except ValidationError as err:
        return ApiException(error_type='Validation Error', message=err.messages, status=400)


@bp.route('/<doc_id>', methods=['GET'])
def get_document_by_id(doc_id):

    # TODO: Check if user has a valid session token.
    # TODO: Use DAOs to retrieve the document with doc_id and user id respectively.

    return ApiResult(response=f'Here is the document with doc_id = {doc_id}')


@bp.route('/<doc_id>/edit/title', methods=['PUT'])
def update_document_title(doc_id):

    # TODO: Check if user has a valid session token.

    if request.json == {}:
        return ApiException(error_type='Api Error', message='No data in request body.', status=400)

    try:
        body = UpdateDocumentTitleValidator().load(request.json)
        # TODO: Use DAOs to update the document.
        return ApiResult(message=f'Valid Data. Updated document {doc_id} title to: {body.get("title")}')

    except ValidationError as err:
        return ApiException(error_type='Validation Error', message=err.messages, status=400)


@bp.route('/<doc_id>/edit/description', methods=['PUT'])
def update_document_description(doc_id):

    # TODO: Check if user has a valid session token.

    if request.json == {}:
        return ApiException(error_type='Api Error', message='No data in request body.', status=400)

    try:
        body = UpdateDocumentDescriptionValidator().load(request.json)
        # TODO: Use DAOs to update the document.
        return ApiResult(message=f'Valid Data. Updated document {doc_id} description to: {body.get("description")}')

    except ValidationError as err:
        return ApiException(error_type='Validation Error', message=err.messages, status=400)


@bp.route('/<doc_id>/edit/timeline', methods=['PUT'])
def update_document_timeline(doc_id):
    # TODO: Check if user has a valid session token.

    if request.json == {}:
        return ApiException(error_type='Api Error', message='No data in request body.', status=400)

    try:
        body = UpdateDocumentTimelineValidator().load(request.json)
        # TODO: Use DAOs to update the document.
        return ApiResult(message=f'Valid Data. Updated document {doc_id} timeline.', new_timeline=body.get("timeline"))

    except ValidationError as err:
        return ApiException(error_type='Validation Error', message=err.messages, status=400)


@bp.route('/<doc_id>/edit/section', methods=['PUT'])
def update_document_section(doc_id):
    # TODO: Check if user has a valid session token.

    if request.json == {}:
        return ApiException(error_type='Api Error', message='No data in request body.', status=400)

    try:
        body = UpdateDocumentSectionValidator().load(request.json)
        # TODO: Use DAOs to update the document.
        return ApiResult(
            message=f'Valid Data. Updated document {doc_id}',
            given_data=body
        )

    except ValidationError as err:
        return ApiException(error_type='Validation Error', message=err.messages, status=400)


@bp.route('/<doc_id>/edit/infrastructure_types', methods=['PUT'])
def update_document_infrastructure_types(doc_id):
    # TODO: Check if user has a valid session token.

    if request.json == {}:
        return ApiException(error_type='Api Error', message='No data in request body.', status=400)

    try:
        body = UpdateDocumentInfrastructureTypesValidator().load(request.json)
        # TODO: Use DAOs to update the document.
        return ApiResult(
            message=f'Valid Data. Updated document {doc_id}',
            given_data=body
        )

    except ValidationError as err:
        return ApiException(error_type='Validation Error', message=err.messages, status=400)


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

