"""
documents.py
====================================
Blueprint class that holds the endpoints that perform CRUD operations on the documents present in the database.
All operations performed on these endpoints must have a valid access token to proceed with a collaborator that has been
approved and is not banned.
"""

from flask import Blueprint, request, json, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.responses import ApiResult, ApiException
from utils.validators import *
from utils.exceptions import TellSpaceApiError, TellSpaceAuthError
from TS_DAOs.schema_DB import *
from datetime import datetime
from TS_DAOs.dao_TS import *

bp = Blueprint('documents', __name__, url_prefix='/documents')


@bp.route('/', methods=['GET'])
@jwt_required
def get_documents():
    """
        Return a list of documents' metadata belonging to a collaborator. The collaborator ID is extracted from the
        access token.
        Returns
        -------
             Response
                JSON object with the list of documents belonging to the collaborator.
             TellSpaceAuthError
                Exception Class with authorization error message. Raised when the collaborator is banned or not
                approved.
    """

    # Get user identity
    email = get_jwt_identity()

    # # Extract collaborator with identity
    collab: Collaborator = get_me(email)

    # print("collab id:" , collab.id)
    if (not collab.banned) and collab.approved:
        documents = get_doc_collab(str(collab.id))
        return jsonify(documents)
        # documents = DocumentCase.objects.filter(creatoriD=str(collab.id))
        response = []
        # for doc in documents:
        #         doc: DocumentCase
        #         response.append({
        #             "id": str(doc.id),
        #             "title": doc.title,
        #             "description": doc.description,
        #             "published": doc.published,
        #             "incidentDate": doc.incidentDate,
        #             "creationDate": doc.creationDate,
        #             "lastModificationDate": doc.lastModificationDate
        #         })
        # return jsonify(response)

    raise TellSpaceAuthError(msg='Authorization Error. Collaborator is banned or has not been approved by the admin.')


@bp.route('/<doc_id>', methods=['GET'])
@jwt_required
def get_document_by_id(doc_id: str):
    """
        Get the information from a specific document using the document id.
        Parameters
        ----------
            doc_id
                the document id string to be searched for
        Returns
        -------
            Response
                JSON object with all the information from a document.
            TellSpaceAuthError
                Exception Class with authorization error message. Raised when the collaborator is banned or not
                approved.
    """
    email = get_jwt_identity()
    collab: Collaborator = get_me(email)

    if not collab.banned and collab.approved:
        doc = get_doc(doc_id)
        return doc, 200
        # doc = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))

        # return json.loads(doc.to_json()), 200

    raise TellSpaceAuthError(msg='Authorization Error. Collaborator is banned or has not been approved by the admin.')


@bp.route('/create', methods=['POST'])
@jwt_required
def create_document():
    """
        Create a new document using the information from the request body.
        Returns
        -------
            ApiResult
                JSON object with the id of the newly created document.
            TellSpaceAuthError
                Exception Class with authorization error message. Raised when the collaborator is banned or not
                approved.
    """

    if not (request.method == 'POST'):
        raise TellSpaceApiError(msg='Method not allowed.', status=400)

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body: CreateDocumentValidator = CreateDocumentValidator().load(request.json)
    email = get_jwt_identity()
    collab: Collaborator = get_me(email)

    # TODO: Verify that the infrastrucutres and damage types exist in the database
    # TODO: Verify if tags exist in the database, if not... add them and create document.
    
    if not collab.banned and collab.approved:
        # authorList = []
        # for author in body['authors']:
        #     authorBody = Author(author_FN= author['first_name'] , author_LN= author['last_name'], 
        #         author_email= author['email'], author_faculty= author['faculty'])
        #     authorList.append(authorBody)
        # actorList = []
        # for actor in body['actors']:
        #     actorBody = Actor(actor_FN= actor['first_name'], actor_LN= actor['last_name'], 
        #         role= actor['role'])
        #     actorList.append(actorBody)
        doc = post_create_doc_DAO(creatoriD = str(collab.id), author = body['authors'], 
        actor = body['actors'], title = body['title'], description = body['description'], 
        language=body['language'], incidentDate = str(body['incident_date']), 
        creationDate = datetime.datetime.today().strftime('%Y-%m-%d'), 
        lastModificationDate=datetime.datetime.today().strftime('%Y-%m-%d'),
        tagsDoc = [], infrasDocList=body['infrastructure_type'], damageDocList = body['damage_type'])
        return ApiResult(docId=str(doc.id))

    raise TellSpaceAuthError(msg='Authorization Error. Collaborator is banned or has not been approved by the admin.')


@bp.route('/remove/<doc_id>', methods=['DELETE'])
@jwt_required
def remove_document(doc_id: str):
    """
        Removes a document using the document id from the route parameters.
        Parameters
        ----------
            doc_id
                the document id string
        Returns
        -------
            ApiResult
                JSON Object containing the id of the removed document.
            TellSpaceAuthError
                Exception Class with authorization error message. Raised when the collaborator is banned or not
                approved.
    """

    # Get user identity
    email = get_jwt_identity()

    # Extract collaborator with identity
    collab: Collaborator = get_me(email)

    if not collab.banned and collab.approved:
        doc = remove_doc(doc_id)
        # doc = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))
        # doc.delete()

        return ApiResult(id=str(doc_id))

    raise TellSpaceAuthError(msg='Authorization Error. Collaborator is banned or has not been approved by the admin.')


@bp.route('/<doc_id>/edit/title', methods=['PUT'])
@jwt_required
def edit_document_title(doc_id: str):
    """
        Edit the document title using doc_id and valid request body values.
        Parameters
        ----------
            doc_id
                the document id string
        Returns
        -------
            ApiResult
                JSON Object with message of the updated document with the new title.
            TellSpaceAuthError
                Exception Class with authorization error message. Raised when the collaborator is banned or not
                approved.
    """

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    email = get_jwt_identity()
    body = TitleValidator().load(request.json)

    collab: Collaborator = get_me(email)
    if not collab.banned and collab.approved:
        doc = put_doc_title(doc_id, body['title'])
        # doc = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))
        # doc.title = body['title']
        # doc.save()
        return ApiResult(message=f'Updated document {doc.id} title to: {doc.title}')

    raise TellSpaceAuthError(msg='Authorization Error. Collaborator is banned or has not been approved by the admin.')


@bp.route('/<doc_id>/edit/description', methods=['PUT'])
@jwt_required
def edit_document_description(doc_id: str):
    """
        Edit the document description using doc_id and valid request body values.
        Parameters
        ----------
            doc_id
                the document id string
        Returns
        -------
            ApiResult
                JSON Object with message of the updated document with the new description.
            TellSpaceAuthError
                Exception Class with authorization error message. Raised when the collaborator is banned or not
                approved.
    """

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    email = get_jwt_identity()
    body = DescriptionValidator().load(request.json)

    collab: Collaborator = get_me(email)

    if not collab.banned and collab.approved:
        doc = put_doc_des(doc_id, body['description'])
        # doc = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))
        # doc.description = body['description']
        # doc.save()

        return ApiResult(message=f'Updated document {doc.id} description to: {doc.description}')

    raise TellSpaceAuthError(msg='Banned collaborator.')


@bp.route('/<doc_id>/edit/timeline', methods=['PUT'])
@jwt_required
def edit_document_timeline(doc_id: str):
    """
        Edit the document timeline using doc_id and valid request body values. Verifies if for all given timeline pairs
        the start date is NOT larger than the end-date.
        Parameters
        ----------
            doc_id
                the document id string
        Returns
        -------
            ApiResult
                JSON Object with message of the updated document and its id.
            TellSpaceAuthError
                Exception Class with authorization error message. Raised when the collaborator is banned or not
                approved.
    """
    email = get_jwt_identity()

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = TimelineValidator().load(request.json)

    # Check that event_start_date is NOT larger than event_end_date
    for time_pair in body['timeline']:
        if time_pair['event_start_date'] > time_pair['event_end_date']:
            raise TellSpaceApiError(
                msg='Invalid Timeline Pair. '
                    'Start Date is larger than the end date. One of the dates is larger than today.',
                status=500
            )

    collab: Collaborator = get_me(email)

    # If collaborator is NOT banned and its approved, then do the thing
    if not collab.banned and collab.approved:
        # timelineList = []
        # for timeline in body['timeline']:
        #     timelineBody = Timeline(event= time_pair['event'], 
        #     eventStartDate= str(time_pair['event_start_date']), 
        #     eventEndDate= str(time_pair['event_end_date']))
        #     timelineList.append(timelineBody)

        doc = put_doc_timeline(docid= doc_id, timeline = body['timeline'])
        # doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))
        # new_timeline = []
        # new_time_pair = Timeline()
        # for time_pair in body['timeline']:
        #     new_time_pair.eventStartDate = str(time_pair['event_start_date'])
        #     new_time_pair.eventEndDate = str(time_pair['event_end_date'])
        #     new_time_pair.event = time_pair['event']
        #     new_timeline.append(new_time_pair)
        # doc.timeline = new_timeline
        # doc.save()

        return ApiResult(message=f'Updated document {doc.id} timeline.')

    raise TellSpaceAuthError(msg='Authorization Error. Collaborator is banned or has not been approved by the admin.')


@bp.route('/<doc_id>/edit/section/create', methods=['POST'])
@jwt_required
def create_document_section(doc_id: str):
    """
        Append new document section using doc_id. Section is appended at the end of document with empty values.
        Return the new section number.
        Parameters
        ----------
            doc_id
                the document id string
        Returns
        -------
            ApiResult
                JSON Object with message of the updated document id and the new number of sections.
            TellSpaceAuthError
                Exception Class with authorization error message. Raised when the collaborator is banned or not
                approved.
    """
    email = get_jwt_identity()
    collab: Collaborator = get_me(email)
    if not collab.banned:
        
        # new_section = Section()
        # new_section.secTitle = f'Section No. {len(doc.section) + 1}'
        # new_section.content = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod...'
        doc = post_doc_section(doc_id)
        # doc.reload()
        return ApiResult(message=f'Created new section for {doc.id}. Total No. of sections {len(doc.section)}')

    raise TellSpaceAuthError(msg='Authorization Error. Collaborator is banned or has not been approved by the admin.')


@bp.route('/<doc_id>/edit/section/remove/<section_nbr>', methods=['DELETE'])
@jwt_required
def remove_document_section(doc_id: str, section_nbr: str):
    """
        Remove a section from a document using doc_id and section number. Section number must be 1 <= x <= len(sections)
        Parameters
        ----------
            doc_id
                the document id string
            section_nbr
                the document section number to be removed
        Returns
        -------
            ApiResult
                JSON Object with message that show the removed section number, the document id and the number of
                sections left.
            TellSpaceAuthError
                Exception Class with authorization error message. Raised when the collaborator is banned or not
                approved.
    """
    email = get_jwt_identity()
    collab: Collaborator = get_me(email)

    # No such thing as a negative section or section 0
    #TODO: consult this with Roberto
    if not collab.banned:
        
        doc = remove_doc_section(doc_id, int(section_nbr))
        # Check if section to pop is larger that the total number of sections
        # if int(section_nbr) > len(doc.section) or int(section_nbr) <= 0:
        #     raise TellSpaceApiError(msg='Section No. does not exist.')

        # Remember that lists start with index 0
        # doc.section.pop(int(section_nbr) - 1)
        # doc.save()
        return ApiResult(
            message=f'Removed section {section_nbr} from {doc.id}. Total No. of sections left {len(doc.section)}'
        )

    raise TellSpaceAuthError(msg='Authorization Error. Collaborator is banned or has not been approved by the admin.')


@bp.route('/<doc_id>/edit/section/<section_nbr>', methods=['PUT'])
@jwt_required
def edit_document_section(doc_id, section_nbr):
    """
        Edit the document section with valid request body values.
        Parameters
        ----------
            doc_id
                the document id string
            section_nbr
                the document section number to be updated
        Returns
        -------
            ApiResult
                JSON Object with message of the updated section and the document id.
            TellSpaceAuthError
                Exception Class with authorization error message. Raised when the collaborator is banned or not
                approved.
    """

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    # No such thing as section 0 or negative
    if int(section_nbr) <= 0:
        raise TellSpaceApiError(msg='No section found.')

    email = get_jwt_identity()
    body: EditSectionValidator = EditSectionValidator().load(request.json)
    collab: Collaborator = get_me(email)

    if not collab.banned:
        doc = put_doc_section(doc_id, body['section_title'], body['section_text'], int(section_nbr))

        # # TODO: verify dao
        # doc: DocumentCase = get_doc(doc_id)

        # # Create section to replace existent one
        # section = Section()
        # section.secTitle = body['section_title']
        # section.content = body['section_text']

        # # Remember that lists start with index 0
        # doc.section[int(section_nbr) - 1] = section
        # doc.save()

        return ApiResult(
            message=f'Edited section {section_nbr} from the document {doc.id}.'
        )

    raise TellSpaceAuthError(msg='Authorization Error. Collaborator is banned or has not been approved by the admin.')


@bp.route('/<doc_id>/edit/infrastructure_types', methods=['PUT'])
@jwt_required
def edit_document_infrastructure_types(doc_id: str):
    """
        Edit the document infrastructure_types using doc_id and valid request body values.
        Parameters
        ----------
            doc_id
                the document id string
        Returns
        -------
            ApiResult
                JSON Object with message containing the id of the updated document.
            TellSpaceAuthError
                Exception Class with authorization error message. Raised when the collaborator is banned or not
                approved.
    """

    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    # Get user identity
    email = get_jwt_identity()

    # Verify request parameters
    body = InfrastructureTypesValidator().load(request.json)

    # Extract collaborator with identity
    collab: Collaborator = get_me(email)

    # Double check if the given infrastrucutres are in the Infrastrucutre Collection
    for infra in body['infrastructure_types']:
        Infrastructure.objects.get(infrastructureType=infra)

    if not collab.banned:
        doc = put_doc_infrasType(doc_id,body['infrastructure_types'])
        # doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))
        # doc.infrasDocList = body['infrastructure_types']
        # doc.save()

        return ApiResult(
            message=f'Edited infrastructure types of the document {doc.id}.'
        )

    raise TellSpaceAuthError(msg='Authorization Error. Collaborator is banned or has not been approved by the admin.')


@bp.route('/<doc_id>/edit/damage_types', methods=['PUT'])
@jwt_required
def edit_document_damage_types(doc_id: str):
    """
        Edit the document damage_types using doc_id and valid request body values.
        Parameters
        ----------
            doc_id
                the document id string
        Returns
        -------
            ApiResult
                JSON Object with message containing the id of the updated document.
            TellSpaceAuthError
                Exception Class with authorization error message. Raised when the collaborator is banned or not
                approved.
    """
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
        doc  = put_doc_damageType(doc_id,body['damage_types'])

        # doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))
        # doc.damageDocList = body['damage_types']
        # doc.save()
        return ApiResult(
            message=f'Edited damage types of the document {doc.id}.'
        )

    raise TellSpaceAuthError(msg='Authorization Error. Collaborator is banned or has not been approved by the admin.')


@bp.route('/<doc_id>/edit/locations', methods=['PUT'])
@jwt_required
def edit_document_locations(doc_id: str):
    """
        Edit the document locations using doc_id and valid request body values.
        Parameters
        ----------
            doc_id
                the document id string
        Returns
        -------
            ApiResult
                JSON Object with message containing the id of the updated document.
            TellSpaceAuthError
                Exception Class with authorization error message. Raised when the collaborator is banned or not
                approved.
    """

    # Get user identity
    email = get_jwt_identity()

    # Verify request parameters
    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = LocationsValidator().load(request.json)

    # Extract collaborator with identity
    collab: Collaborator = get_me(email)

    if not collab.banned:
        doc = put_doc_locations(doc_id,body.get('locations'))
        # doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))
        # doc.location = body.get('locations')
        # doc.save()
        return ApiResult(
            message=f'Edited locations of the document {doc.id}.'
        )

    raise TellSpaceAuthError(msg='Authorization Error. Collaborator is banned or has not been approved by the admin.')


@bp.route('/<doc_id>/edit/tags', methods=['PUT'])
@jwt_required
def edit_document_tags(doc_id: str):
    """
        Edit the document tags using doc_id and valid request body values.
        Parameters
        ----------
            doc_id
                the document id string
        Returns
        -------
            ApiResult
                JSON Object with message containing the id of the updated document.
            TellSpaceAuthError
                Exception Class with authorization error message. Raised when the collaborator is banned or not
                approved.
    """

    # Get user identity
    email = get_jwt_identity()

    # Verify request parameters
    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = TagsValidator().load(request.json)

    # Extract collaborator with identity
    collab: Collaborator = get_me(email)

    if not collab.banned:
        doc = put_doc_tags(doc_id, body['tags'])
        # doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))

        # # If tags exists DO NOT exist in the tags collection, add it
        # for tag in body['tags']:
        #     if not Tag.objects(tagItem=tag):
        #         newTag = Tag(tagItem=tag)
        #         newTag.save()

        # doc.tagsDoc = body['tags']
        # doc.save()
        return ApiResult(message=f'Edited tags of the document {doc.id}.')

    raise TellSpaceAuthError(msg='Authorization Error. Collaborator is banned or has not been approved by the admin.')


@bp.route('/<doc_id>/edit/incident_date', methods=['PUT'])
@jwt_required
def edit_document_incident_date(doc_id: str):
    """
        Edit the document tags using doc_id and valid request body values.
        Parameters
        ----------
            doc_id
                the document id string
        Returns
        -------
            ApiResult
                JSON Object with message containing the id of the updated document.
            TellSpaceAuthError
                Exception Class with authorization error message. Raised when the collaborator is banned or not
                approved.
    """

    # Get user identity
    email = get_jwt_identity()

    # Verify request parameters
    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = IncidentDateValidator().load(request.json)

    # Verify that the date of the incident date is not in the future
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    if str(body['incident_date']) > today:
        raise TellSpaceApiError(msg='Incident date is in the future.')

    # Extract collaborator with identity
    collab: Collaborator = get_me(email)

    if not collab.banned:

        doc = put_doc_incidentDate(doc_id, body["incident_date"])
        # doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))
        # doc.incidentDate = str(body['incident_date'])
        # doc.save()
        return ApiResult(message=f'Edited incident date of the document {doc.id}.')

    raise TellSpaceAuthError(msg='Authorization Error. Collaborator is banned or has not been approved by the admin.')


@bp.route('/<doc_id>/edit/actors', methods=['PUT'])
@jwt_required
def edit_document_actors(doc_id: str):
    """
        Edit the document actors using doc_id and valid request body values.
        Parameters
        ----------
            doc_id
                the document id string
        Returns
        -------
            ApiResult
                JSON Object with message containing the id of the updated document.
            TellSpaceAuthError
                Exception Class with authorization error message. Raised when the collaborator is banned or not
                approved.
    """

    # Get user identity
    email = get_jwt_identity()

    # Verify request parameters
    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)
    body = ActorsValidator().load(request.json)

    # Extract collaborator with identity
    collab: Collaborator = get_me(email)

    if not collab.banned:
        
        # actorList = []
        # for actor in body['actors']:
        #     actorBody = Actor(actor_FN= actor.first_name, actor_LN= actor.last_name, 
        #         role= actor.role)
        # actorList.append(actorBody)
        doc = put_doc_actors(doc_id, body['actors'])

        # doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))
        # actor_list = []
        # for a in body['actors']:
        #     actor = Actor()
        #     actor.actor_FN = a['first_name']
        #     actor.actor_LN = a['last_name']
        #     actor.role = a['role']
        #     actor_list.append(actor)

        # doc.actor = actor_list
        # doc.save()
        return ApiResult(
            message=f'Edited actors of the document {doc.id}.'
        )

    raise TellSpaceAuthError(msg='Authorization Error. Collaborator is banned or has not been approved by the admin.')


@bp.route('/<doc_id>/edit/authors', methods=['PUT'])
@jwt_required
def edit_document_authors(doc_id: str):
    """
        Edit the document authors using doc_id and valid request body values.
        Parameters
        ----------
            doc_id
                the document id string
        Returns
        -------
            ApiResult
                JSON Object with message containing the id of the updated document.
            TellSpaceAuthError
                Exception Class with authorization error message. Raised when the collaborator is banned or not
                approved.
    """

    # Get user identity
    email = get_jwt_identity()

    # Verify request parameters
    if request.json == {}:
        raise TellSpaceApiError(msg='No request body data.', status=400)

    body = AuthorsValidator().load(request.json)

    # Extract collaborator with identity
    collab: Collaborator = get_me(email)

    if not collab.banned:

        # authorList = []
        # for author in body['authors']:
        #     authorBody = Author(author_FN= author.first_name, author_LN= author.last_name, 
        #         author_email= author.email, author_faculty= author.faculty)
        # authorList.append(authorBody)
        doc = put_doc_authors(doc_id, body['authors'])

        # doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab.id))
        # authors_list = []
        # for a in body['authors']:
        #     new_author = Author()
        #     new_author.author_FN = a['first_name']
        #     new_author.author_LN = a['last_name']
        #     new_author.author_email = a['email']
        #     new_author.author_faculty = a['faculty']
        #     authors_list.append(new_author)

        # doc.author = authors_list
        # doc.save()
        return ApiResult(id=str(doc.id))

    raise TellSpaceAuthError(msg='Authorization Error. Collaborator is banned or has not been approved by the admin.')


@bp.before_request
def before_requests():
    """Method to setup variables and route dependencies if needed."""
    pass