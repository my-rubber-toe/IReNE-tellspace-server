from flask import Blueprint, request, json
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.responses import ApiResult, ApiException
from utils.validators import *
from utils.exceptions import TellSpaceApiError, TellSpaceAuthError
from database.schema_DB import *
from daos.dao_TS import *
from datetime import datetime

bp = Blueprint('documents', __name__, url_prefix='/documents')


@bp.route('/', methods=['GET'])
@jwt_required
def get_documents():
    """ Return a list of documents' metadata belonging to the collabID"""

    # Get user identity
    email = get_jwt_identity()

    # Extract collaborator with identity
    collab: Collaborator = Collaborator.objects.get(email=email)

    if not collab.banned:
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

    raise TellSpaceAuthError(msg='Banned collaborator.')


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

    if not collab.banned:
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

    raise TellSpaceAuthError(msg='Banned collaborator.')


@bp.route('/remove/<doc_id>', methods=['DELETE'])
@jwt_required
def remove_document(doc_id: str):
    """ Removes a document using the information from the request body and the user id."""

    # Get user identity
    email = get_jwt_identity()

    # Extract collaborator with identity
    collab: Collaborator = Collaborator.objects.get(email=email)

    if not collab.banned:
        doc = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))
        doc.delete()

        return ApiResult(docId=str(doc.id))

    raise TellSpaceAuthError(msg='Banned collaborator.')


@bp.route('/<doc_id>', methods=['GET'])
@jwt_required
def get_document_by_id(doc_id: str):
    """Get all document information using the doc_id."""
    email = get_jwt_identity()
    collab: Collaborator = Collaborator.objects.get(email=email)

    if not collab.banned:
        doc = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))

        return ApiResult(content=json.loads(doc.to_json()), id=doc_id)

    raise TellSpaceAuthError(msg='Banned collaborator.')


@bp.route('/<doc_id>/edit/title', methods=['PUT'])
@jwt_required
def edit_document_title(doc_id: str):
    """Edit the document title using doc_id and valid request body values."""

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    email = get_jwt_identity()
    body = TitleValidator().load(request.json)

    collab: Collaborator = Collaborator.objects.get(email=email)
    if not collab.banned:
        doc = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))

        doc.title = body['title']
        doc.save()
        return ApiResult(message=f'Valid Data. Updated document {doc.id} title to: {doc.title}')

    raise TellSpaceAuthError(msg='Banned collaborator.')


@bp.route('/<doc_id>/edit/description', methods=['PUT'])
@jwt_required
def edit_document_description(doc_id):
    """Edit the document description using doc_id and valid request body values."""

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    email = get_jwt_identity()
    body = DescriptionValidator().load(request.json)

    collab: Collaborator = Collaborator.objects.get(email=email)

    if not collab.banned:
        doc = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))
        doc.description = body['description']
        doc.save()

        return ApiResult(id=str(doc.id))

    raise TellSpaceAuthError(msg='Banned collaborator.')



@bp.route('/<doc_id>/edit/timeline', methods=['PUT'])
@jwt_required
def edit_document_timeline(doc_id):
    """Edit the document timeline using doc_id and valid request body values."""

    email = get_jwt_identity()

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = TimelineValidator().load(request.json)

    collab: Collaborator = Collaborator.objects.get(email=email)

    # If collaborator is NOT banned, do the thing
    if not collab.banned:
        doc : DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))
        new_timeline = []
        for timeline_pair in body['timeline']:
            t = Timeline()
            t.eventDate = timeline_pair['event_date']
            t.event = timeline_pair['event_description']
            new_timeline.append(t)

        doc.timeline = new_timeline
        doc.save()

        return ApiResult(id=str(doc.id))

    raise TellSpaceApiError(msg='Banned collaborator.')


@bp.route('/<doc_id>/edit/section/create', methods=['POST'])
@jwt_required
def create_document_section(doc_id):
    """Append new document section using doc_id. Section is appended at the end of document with empty values.
        Return the new section number.
    """
    email = get_jwt_identity()
    collab: Collaborator = Collaborator.objects.get(email=email)
    if not collab.banned:
        doc : DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))
        new_section = Section()
        new_section.secTitle = f'Section No. {len(doc.section) + 1}'
        new_section.content = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod...'
        doc.section.append(new_section)
        doc.save()
        return ApiResult(id=str(doc.id), section_nbr=len(doc.section))

    raise TellSpaceApiError(msg='Banned collaborator.')



@bp.route('/<doc_id>/edit/section/remove/<section_nbr>', methods=['DELETE'])
@jwt_required
def remove_document_section(doc_id: str, section_nbr: str):
    """Remove a section from a document using doc_id and section number."""
    email = get_jwt_identity()
    collab: Collaborator = Collaborator.objects.get(email=email)

    # No such thing as a negative section or section 0
    if int(section_nbr) <= 0:
        raise TellSpaceApiError(msg='Section No. does not exist.')

    if not collab.banned:
        doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))

        # Remember that lists start with index 0
        doc.section.pop(int(section_nbr) - 1)
        doc.save()
        return ApiResult(id=str(doc.id))

    raise TellSpaceApiError(msg='Banned collaborator.')


@bp.route('/<doc_id>/edit/section/<section_nbr>', methods=['PUT'])
@jwt_required
def edit_document_section(doc_id, section_nbr):
    """Edit the document section using doc_id and valid request body values."""

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    # No such thing as section 0 or negative
    if int(section_nbr) <= 0:
        raise TellSpaceApiError(msg='No section found.')

    email = get_jwt_identity()
    body: EditSectionValidator = EditSectionValidator().load(request.json)
    collab: Collaborator = Collaborator.objects.get(email=email)

    if not collab.banned:
        doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))

        # Create section to replace existent one
        section = Section()
        section.secTitle = body['section_title']
        section.content = body['section_text']

        # Remember that lists start with index 0
        doc.section[int(section_nbr) - 1] = section
        doc.save()

        return ApiResult(id=str(doc.id))

    raise TellSpaceApiError(msg='Banned collaborator.')


@bp.route('/<doc_id>/edit/infrastructure_types', methods=['PUT'])
@jwt_required
def edit_document_infrastructure_types(doc_id):
    """Edit the document infrastructure_types using doc_id and valid request body values."""

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    # Get user identity
    email = get_jwt_identity()

    # Verify request parameters
    body = InfrastructureTypesValidator().load(request.json)

    # Extract collaborator with identity
    collab: Collaborator = Collaborator.objects.get(email=email)

    # Double check if the given infrastrucutres are in the Infrastrucutre Collection
    for infra in body['infrastructure_types']:
        Infrastructure.objects.get(infrastructureType=infra)

    if not collab.banned:
        doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))
        doc.infrasDocList = body['infrastructure_types']
        doc.save()

        return ApiResult(id=str(doc.id))

    raise TellSpaceApiError(msg='Banned collaborator.')


@bp.route('/<doc_id>/edit/damage_types', methods=['PUT'])
@jwt_required
def edit_document_damage_types(doc_id):
    """Edit the document damage_types using doc_id and valid request body values."""
    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    # Get user identity
    email = get_jwt_identity()

    # Verify request parameters
    body = DamageTypesValidator().load(request.json)

    # Extract collaborator with identity
    collab: Collaborator = Collaborator.objects.get(email=email)

    for damage in body['damage_types']:
        Damage.objects.get(damageType=damage)

    if not collab.banned:
        doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))
        doc.damageDocList = body['damage_types']
        doc.save()
        return ApiResult(id=str(doc.id))

    raise TellSpaceApiError(msg='Banned collaborator.')


@bp.route('/<doc_id>/edit/actors', methods=['PUT'])
@jwt_required
def edit_document_actors(doc_id):
    """Edit the document actors using doc_id and valid request body values."""

    # Get user identity
    email = get_jwt_identity()

    # Verify request parameters
    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)
    body = ActorsValidator().load(request.json)

    # Extract collaborator with identity
    collab: Collaborator = Collaborator.objects.get(email=email)

    if not collab.banned:
        doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))
        actor_list = []
        for a in body['actors']:
            actor = Actor()
            actor.actor_FN = a['first_name']
            actor.actor_LN = a['last_name']
            actor.role = a['role']
            actor_list.append(actor)

        doc.actor = actor_list
        doc.save()
        return ApiResult(id=str(doc.id))

    raise TellSpaceApiError(msg='Banned collaborator.')


@bp.route('/<doc_id>/edit/locations', methods=['PUT'])
@jwt_required
def edit_document_locations(doc_id):
    """Edit the document locations using doc_id and valid request body values."""

    # Get user identity
    email = get_jwt_identity()

    # Verify request parameters
    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = LocationsValidator().load(request.json)

    # Extract collaborator with identity
    collab: Collaborator = Collaborator.objects.get(email=email)

    if not collab.banned:
        doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))
        doc.location = body.get('locations')
        doc.save()
        return ApiResult(id=str(doc.id))

    raise TellSpaceApiError(msg='Banned collaborator.')


@bp.route('/<doc_id>/edit/authors', methods=['PUT'])
@jwt_required
def edit_document_authors(doc_id):
    """Edit the document authors using doc_id and valid request body values."""

    # Get user identity
    email = get_jwt_identity()

    # Verify request parameters
    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = AuthorsValidator().load(request.json)

    # Extract collaborator with identity
    collab: Collaborator = Collaborator.objects.get(email=email)

    if not collab.banned:
        doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))
        authors_list = []
        for a in body['authors']:
            new_author = Author()
            new_author.author_FN = a['first_name']
            new_author.author_LN = a['last_name']
            new_author.author_email = a['email']
            new_author.author_faculty = a['faculty']
            authors_list.append(new_author)

        doc.author = authors_list
        doc.save()
        return ApiResult(id=str(doc.id))

    raise TellSpaceApiError(msg='Banned collaborator.')


@bp.route('/<doc_id>/edit/tags', methods=['PUT'])
@jwt_required
def edit_document_tags(doc_id):
    """Edit the document tags using doc_id and valid request body values."""

    # Get user identity
    email = get_jwt_identity()

    # Verify request parameters
    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = TagsValidator().load(request.json)

    # Extract collaborator with identity
    collab: Collaborator = Collaborator.objects.get(email=email)

    if not collab.banned:
        doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))

        # If tags exists DO NOT exist in the tags collection, add it
        for tag in body['tags']:
            if not Tag.objects(tagItem=tag):
                newTag = Tag(tagItem=tag)
                newTag.save()

        doc.tagsDoc = body['tags']
        doc.save()
        return ApiResult(id=str(doc.id))

    raise TellSpaceAuthError(msg='Banned collaborator.')


@bp.before_request
def before_requests():
    """Method to setup variables and route dependencies if needed."""
    pass

