# TODO: Add authentication decorator as needed

from flask import Blueprint, request, json
from utils.responses import ApiResult, ApiException
from utils.validators import *
from marshmallow import ValidationError
from uuid import uuid4


from utils.exceptions import TellSpaceApiError

bp = Blueprint('documents', __name__, url_prefix='/api/documents')


@bp.route('/', methods=['GET'])
def get_documents():
    """ Return a list of documents based on the body request parameters. The parameters will be used to filter the
           information within the metadata of the documents. Documents returned will be those from the res.
           User id will be retrieved from the session object.
    """
    # TODO: Check if user has a valid session token.

    # Request validation
    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = GetDocumentsValidator().load(request.json)
    # TODO: Use DAOs to retrieve the necessary information.

    return ApiResult(message='Valid Data', given_data=body)


@bp.route('/create', methods=['GET', 'POST'])
def create_document():

    if not(request.method == 'POST'):
        return TellSpaceApiError(msg='Method not allowed.', status=400)

    # TODO: Check if user has a valid session token.

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = CreateDocumentValidator().load(request.json)
    # TODO: Use user ID and DAOs to create a new document using the collaborator ID.
    return ApiResult(message='Valid Data. Document will be created with the given data', given_data=body)


@bp.route('/<doc_id>', methods=['GET'])
def get_document_by_id(doc_id):

    # TODO: Check if user has a valid session token.

    return ApiResult(response=f'Here is the document with doc_id = {doc_id}')


@bp.route('/<doc_id>/edit/title', methods=['PUT'])
def update_document_title(doc_id):

    # TODO: Check if user has a valid session token.

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = TitleValidator().load(request.json)
    # TODO: Use DAOs to update the document.
    return ApiResult(message=f'Valid Data. Updated document {doc_id} title to: {body.get("title")}')


@bp.route('/<doc_id>/edit/description', methods=['PUT'])
def update_document_description(doc_id):

    # TODO: Check if user has a valid session token.

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = DescriptionValidator().load(request.json)
    # TODO: Use DAOs to update the document.
    return ApiResult(message=f'Valid Data. Updated document {doc_id} description to: {body.get("description")}')


@bp.route('/<doc_id>/edit/timeline', methods=['PUT'])
def update_document_timeline(doc_id):
    # TODO: Check if user has a valid session token.

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = TimelineValidator().load(request.json)
    # TODO: Use DAOs to update the document.
    return ApiResult(message=f'Valid Data. Updated document {doc_id} timeline.', given_data=body)


@bp.route('/<doc_id>/edit/section', methods=['PUT'])
def update_document_section(doc_id):
    # TODO: Check if user has a valid session token.

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = SectionValidator().load(request.json)
    # TODO: Use DAOs to update the document.
    return ApiResult(message=f'Valid Data. Updated document {doc_id}', given_data=body)


@bp.route('/<doc_id>/edit/infrastructure_types', methods=['PUT'])
def update_document_infrastructure_types(doc_id):
    # TODO: Check if user has a valid session token.

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = InfrastructureTypesValidator().load(request.json)
    # TODO: Use DAOs to update the document.
    return ApiResult(message=f'Valid Data. Updated infrastructure types for {doc_id}', given_data=body)


@bp.route('/<doc_id>/edit/damage_types', methods=['PUT'])
def update_document_damage_types(doc_id):
    # TODO: Check if user has a valid session token.

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = DamageTypesValidator().load(request.json)
    # TODO: Use DAOs to update the document.
    return ApiResult(message=f'Valid Data. Updated damage types for document: {doc_id}', given_data=body)


@bp.route('/<doc_id>/edit/actors', methods=['PUT'])
def update_document_actors(doc_id):
    # TODO: Check if user has a valid session token.

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = ActorsValidator().load(request.json)
    # TODO: Use DAOs to update the document.
    return ApiResult(message=f'Valid Data. Updated actors for document: {doc_id}', given_data=body)


@bp.route('/<doc_id>/edit/locations', methods=['PUT'])
def update_document_locations(doc_id):
    # TODO: Check if user has a valid session token.

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = LocationsValidator().load(request.json)
    # TODO: Use DAOs to update the document.
    return ApiResult(message=f'Valid Data. Updated damage types for document: {doc_id}', given_data=body)


@bp.route('/<doc_id>/edit/authors', methods=['PUT'])
def update_document_authors(doc_id):
    # TODO: Check if user has a valid session token.

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = AuthorsValidator().load(request.json)
    # TODO: Use DAOs to update the document.
    return ApiResult(message=f'Valid Data. Updated authors for document: {doc_id}', given_data=body)


@bp.route('/<doc_id>/edit/tags', methods=['PUT'])
def update_document_tags(doc_id):
    # TODO: Check if user has a valid session token.

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = TagsValidator().load(request.json)
    # TODO: Use DAOs to update the document.
    return ApiResult(message=f'Valid Data. Updated tags for document: {doc_id}', given_data=body)


@bp.before_request
def before_requests():
    print(f'Before requests under routes /api/documents')

