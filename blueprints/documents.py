from flask import Blueprint, request, json
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.responses import ApiResult, ApiException
from utils.validators import *
from utils.exceptions import TellSpaceApiError
from database.schema_DB import *
from daos.dao_TS import *
from datetime import datetime

bp = Blueprint('documents', __name__, url_prefix='/documents')


@bp.route('/', methods=['GET'])
@jwt_required
def get_documents():
    """ Return a list of documents' metadata belonging to the collabID"""
    email = get_jwt_identity()
    collab: Collaborator = Collaborator.objects.get(email=email)
    documents = DocumentCase.objects.filter(creatoriD=str(collab.id))

    response = []
    for doc in documents:
        response.append({
            "id": str(doc.id),
            "title": doc.title,
            "desctription":  doc.description,
            "published": doc.published,
            "incidentDate": doc.incidentDate,
            "creationDate": doc.creationDate
        })

    return ApiResult(response=response)


@bp.route('/create', methods=['GET', 'POST'])
@jwt_required
def create_document():
    """ Create a new document using the information from the request body."""
    if not(request.method == 'POST'):
        raise TellSpaceApiError(msg='Method not allowed.', status=400)

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body: CreateDocumentValidator = CreateDocumentValidator().load(request.json)
    email = get_jwt_identity()
    collab: Collaborator = Collaborator.objects.get(email=email)

    doc = DocumentCase()
    doc.creatoriD = str(collab.id)
    doc.title = body['title']
    doc.location = []
    doc.description = body['description']
    doc.incidentDate = datetime.today().strftime('%Y-%m-%d')
    doc.creationDate = datetime.today().strftime('%Y-%m-%d')
    doc.tagsDoc = []
    doc.infrasDocList = body['infrastructure_type']
    doc.damageDocList = []
    doc.author = []
    doc.actor = []
    doc.section = []
    doc.timeline = []
    doc.published = True
    doc.save()

    return ApiResult(docId=str(doc.id))


@bp.route('/remove/<doc_id>', methods=['DELETE'])
@jwt_required
def remove_document(doc_id: str):
    """ Removes a document using the information from the request body and the user id."""

    email = get_jwt_identity()
    collab: Collaborator = Collaborator.objects.get(email=email)

    doc = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))
    doc.delete()

    return ApiResult(docId=str(doc.id))


@bp.route('/<doc_id>', methods=['GET'])
@jwt_required
def get_document_by_id(doc_id: str):
    """Get all document information using the doc_id."""
    email = get_jwt_identity()
    collab: Collaborator = Collaborator.objects.get(email=email)
    doc = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))

    return ApiResult(content=json.loads(doc.to_json()), id=doc_id)


@bp.route('/<doc_id>/edit/title', methods=['PUT'])
@jwt_required
def edit_document_title(doc_id: str):
    """Edit the document title using doc_id and valid request body values."""

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    email = get_jwt_identity()
    body = TitleValidator().load(request.json)

    collab: Collaborator = Collaborator.objects.get(email=email)
    doc = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))

    doc.title = body['title']
    doc.save()
    return ApiResult(message=f'Valid Data. Updated document {doc.id} title to: {doc.title}')


@bp.route('/<doc_id>/edit/description', methods=['PUT'])
@jwt_required
def edit_document_description(doc_id):
    """Edit the document description using doc_id and valid request body values."""

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    email = get_jwt_identity()
    body = DescriptionValidator().load(request.json)

    collab: Collaborator = Collaborator.objects.get(email=email)
    doc = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))
    doc.description = body['description']
    doc.save()

    return ApiResult(message=f'Valid Data. Updated document {doc.id} description to: {doc.description}')


@bp.route('/<doc_id>/edit/timeline', methods=['PUT'])
def edit_document_timeline(doc_id):
    """Edit the document timeline using doc_id and valid request body values."""

    # TODO: Check if user has a valid session token.
    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = TimelineValidator().load(request.json)
    # TODO: Use user ID and DAOs to update document.
    return ApiResult(message=f'Valid Data. Updated document {doc_id} timeline.', given_data=body)


@bp.route('/<doc_id>/edit/section/create', methods=['POST'])
def create_document_section(doc_id):
    """Create a new document section using doc_id. Section is appended at the end of document.
        Return the new section number.
    """

    # TODO: Check if user has a valid session token.
    # TODO: Use user ID and DAOs to create the document section.
    return ApiResult(message=f'Valid Data.Section created in document {doc_id}')


@bp.route('/<doc_id>/edit/section/remove/<section_nbr>', methods=['DELETE'])
def remove_document_section(doc_id):
    """Remove a section from a document using doc_id and section number."""
    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = RemoveSectionValidator().load(request.json)

    # TODO: Check if user has a valid session token.
    # TODO: Use user ID and DAOs to remove the document section.
    return ApiResult(message=f'Valid Data.  Section removed in document {doc_id}', given_data=body)


@bp.route('/<doc_id>/edit/section', methods=['PUT'])
def edit_document_section(doc_id):
    """Edit the document section using doc_id and valid request body values."""

    # TODO: Check if user has a valid session token.

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = EditSectionValidator().load(request.json)
    # TODO: Use user ID and DAOs to update document..
    return ApiResult(message=f'Valid Data. Updated document {doc_id}', given_data=body)



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

