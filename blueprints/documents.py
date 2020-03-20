# TODO: Add authentication decorator as needed

from flask import Blueprint, request, json
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.responses import ApiResult, ApiException
from utils.validators import *



from utils.exceptions import TellSpaceApiError

bp = Blueprint('documents', __name__, url_prefix='/documents')


@bp.route('/', methods=['GET'])
def get_documents():
    """ Return a list of documents' metadata belonging to the collabID"""
    # TODO: Check if user has a valid session token.
    # TODO: Use DAOs to retrieve the necessary information.

    return ApiResult(message='Return a list of documents that belong to the client.')


@bp.route('/create', methods=['GET', 'POST'])
def create_document():
    """ Create a new document using the information from the request body."""

    if not(request.method == 'POST'):
        raise TellSpaceApiError(msg='Method not allowed.', status=400)

    # TODO: Check if user has a valid session token.

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = CreateDocumentValidator().load(request.json)
    # TODO: Use user ID and DAOs to create a new document using the collaborator ID.
    return ApiResult(message='Valid Data. Document will be created with the given data', given_data=body)


@bp.route('/remove', methods=['DELETE'])
def create_document():
    """ Removes a document using the information from the request body and the user id."""

    # TODO: Check if user has a valid session token.

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = CreateDocumentValidator().load(request.json)
    # TODO: Use user ID and DAOs to create a new document using the collaborator ID.
    return ApiResult(message='Valid Data. Document will be created with the given data', given_data=body)


@bp.route('/<doc_id>', methods=['GET'])
def get_document_by_id(doc_id):
    """Get all document information using the doc_id."""
    # TODO: Check if user has a valid session token.
    # TODO: Use user ID and DAOs to return the document.
    return ApiResult(response=f'Here is the document with doc_id = {doc_id}')


@bp.route('/<doc_id>/edit/title', methods=['PUT'])
def edit_document_title(doc_id):
    """Edit the document title using doc_id and valid request body values."""

    # TODO: Check if user has a valid session token.

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = TitleValidator().load(request.json)
    # TODO: Use user ID and DAOs to update the document title.
    return ApiResult(message=f'Valid Data. Updated document {doc_id} title to: {body.get("title")}')


@bp.route('/<doc_id>/edit/description', methods=['PUT'])
def edit_document_description(doc_id):
    """Edit the document description using doc_id and valid request body values."""

    # TODO: Check if user has a valid session token.

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = DescriptionValidator().load(request.json)
    # TODO: Use user ID and DAOs to update document.
    return ApiResult(message=f'Valid Data. Updated document {doc_id} description to: {body.get("description")}')


@bp.route('/<doc_id>/edit/timeline', methods=['PUT'])
def edit_document_timeline(doc_id):
    """Edit the document timeline using doc_id and valid request body values."""

    # TODO: Check if user has a valid session token.
    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = TimelineValidator().load(request.json)
    # TODO: Use user ID and DAOs to update document.
    return ApiResult(message=f'Valid Data. Updated document {doc_id} timeline.', given_data=body)


@bp.route('/<doc_id>/edit/section', methods=['PUT'])
def edit_document_section(doc_id):
    """Edit the document section using doc_id and valid request body values."""

    # TODO: Check if user has a valid session token.

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = EditSectionValidator().load(request.json)
    # TODO: Use user ID and DAOs to update document..
    return ApiResult(message=f'Valid Data. Updated document {doc_id}', given_data=body)


@bp.route('/<doc_id>/edit/section/create', methods=['POST'])
def create_document_section(doc_id):
    """Create a new document section using doc_id. Section is appended at the end of document.
        Return the new section number.
    """

    # TODO: Check if user has a valid session token.
    # TODO: Use user ID and DAOs to create the document section.
    return ApiResult(message=f'Valid Data.Section created in document {doc_id}')


@bp.route('/<doc_id>/edit/section/remove', methods=['DELETE'])
def remove_document_section(doc_id):
    """Remove a section from a document using doc_id and section number."""
    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = RemoveSectionValidator().load(request.json)

    # TODO: Check if user has a valid session token.
    # TODO: Use user ID and DAOs to remove the document section.
    return ApiResult(message=f'Valid Data.  Section removed in document {doc_id}', given_data=body)


@bp.route('/<doc_id>/edit/infrastructure_types', methods=['PUT'])
def edit_document_infrastructure_types(doc_id):
    """Edit the document infrastructure_types using doc_id and valid request body values."""
    # TODO: Check if user has a valid session token.

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = InfrastructureTypesValidator().load(request.json)
    # TODO: Use user ID and DAOs to update the document.
    return ApiResult(message=f'Valid Data. Updated infrastructure types for {doc_id}', given_data=body)


@bp.route('/<doc_id>/edit/damage_types', methods=['PUT'])
def edit_document_damage_types(doc_id):
    """Edit the document damage_types using doc_id and valid request body values."""
    # TODO: Check if user has a valid session token.

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = DamageTypesValidator().load(request.json)
    # TODO: Use DAOs to update the document.
    return ApiResult(message=f'Valid Data. Updated damage types for document: {doc_id}', given_data=body)


@bp.route('/<doc_id>/edit/actors', methods=['PUT'])
def edit_document_actors(doc_id):
    """Edit the document actors using doc_id and valid request body values."""
    # TODO: Check if user has a valid session token.

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = ActorsValidator().load(request.json)
    # TODO: Use DAOs to update the document.
    return ApiResult(message=f'Valid Data. Updated actors for document: {doc_id}', given_data=body)


@bp.route('/<doc_id>/edit/locations', methods=['PUT'])
def edit_document_locations(doc_id):
    """Edit the document locations using doc_id and valid request body values."""

    # TODO: Check if user has a valid session token.

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = LocationsValidator().load(request.json)
    # TODO: Use DAOs to update the document.
    return ApiResult(message=f'Valid Data. Updated damage types for document: {doc_id}', given_data=body)


@bp.route('/<doc_id>/edit/authors', methods=['PUT'])
def edit_document_authors(doc_id):
    """Edit the document authors using doc_id and valid request body values."""

    # TODO: Check if user has a valid session token.

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = AuthorsValidator().load(request.json)
    # TODO: Use DAOs to update the document.
    return ApiResult(message=f'Valid Data. Updated authors for document: {doc_id}', given_data=body)


@bp.route('/<doc_id>/edit/tags', methods=['PUT'])
def edit_document_tags(doc_id):
    """Edit the document tags using doc_id and valid request body values."""

    # TODO: Check if user has a valid session token.

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = TagsValidator().load(request.json)
    # TODO: Use DAOs to update the document.
    return ApiResult(message=f'Valid Data. Updated tags for document: {doc_id}', given_data=body)


@bp.before_request
def before_requests():
    print(f'Before requests under routes /api/documents')

