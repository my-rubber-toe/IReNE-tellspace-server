"""
document.py
Blueprint class that holds the endpoints that perform CRUD operations on the documents present in the database.
All operations performed on these endpoints must have a valid access token to proceed with a collaborator that has been
approved and is not banned.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.responses import ApiResult, ApiException
from utils.validators import *
from utils.exceptions import TellSpaceAuthError
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

    # Extract collaborator with identity
    collab: Collaborator = get_me(email)

    if (not collab.banned) and collab.approved:
        documents = get_doc_collab(str(collab.id))
        return jsonify(documents)

    raise TellSpaceAuthError(
        msg='Authorization Error. Collaborator is banned or has not been approved by the admin.',
        status=401
    )

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
        doc = get_doc(doc_id, str(collab.id))
        return jsonify(doc)

    raise TellSpaceAuthError(
        msg='Authorization Error. Collaborator is banned or has not been approved by the admin.',
        status=401
    )


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

    if not collab.banned and collab.approved:
        doc = post_create_doc_DAO(
            creatoriD=collab.id,
            author=body['authors'],
            actor=body['actors'],
            title=body['title'],
            language=body['language'],
            incidentDate=str(body['incident_date']),
            creationDate=datetime.datetime.today().strftime('%Y-%m-%d'),
            lastModificationDate=datetime.datetime.today().strftime('%Y-%m-%d'),
            tagsDoc=[],
            infrasDocList=body['infrastructure_type'],
            damageDocList=body['damage_type'])

        return ApiResult(docId=str(doc.id))

    raise TellSpaceAuthError(
        msg='Authorization Error. Collaborator is banned or has not been approved by the admin.',
        status=401
    )

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
        deleted_id = remove_doc(doc_id, collab.id)
        return ApiResult(message=f'Deleted document {deleted_id}')

    raise TellSpaceAuthError(
        msg='Authorization Error. Collaborator is banned or has not been approved by the admin.',
        status=401
    )

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
        saved_id = put_doc_title(collab.id, doc_id, body['title'])
        return ApiResult(message=f'Updated document: {saved_id}')

    raise TellSpaceAuthError(
        msg='Authorization Error. Collaborator is banned or has not been approved by the admin.',
        status=401
    )

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
        saved_id = put_doc_des(collab.id, doc_id, body['description'])
        return ApiResult(message=f'Updated document description.')

    raise TellSpaceAuthError(
        msg='Authorization Error. Collaborator is banned or has not been approved by the admin.',
        status=401
    )

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
        saved_id = put_doc_timeline(collab_id=collab.id, doc_id=doc_id, timeline=body['timeline'])
        return ApiResult(message=f'Updated document {saved_id} timeline.')

    raise TellSpaceAuthError(
        msg='Authorization Error. Collaborator is banned or has not been approved by the admin.',
        status=401
    )

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
        doc = post_doc_section(collab.id, doc_id)
        return ApiResult(message=f'Created new section for {doc.id}. Total No. of sections {len(doc.section)}')

    raise TellSpaceAuthError(
        msg='Authorization Error. Collaborator is banned or has not been approved by the admin.',
        status=401
    )

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

    if not collab.banned:
        saved_id = remove_doc_section(collab.id, doc_id, int(section_nbr))
        return ApiResult(message=f'Removed section from document {saved_id}.')

    raise TellSpaceAuthError(
        msg='Authorization Error. Collaborator is banned or has not been approved by the admin.',
        status=401
    )

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

    email = get_jwt_identity()
    body: EditSectionValidator = EditSectionValidator().load(request.json)
    collab: Collaborator = get_me(email)

    if not collab.banned:
        saved_id = put_doc_section(collab.id, doc_id, body['section_title'], body['section_text'], int(section_nbr))

        return ApiResult(message=f'Edited section from the document {saved_id}.')

    raise TellSpaceAuthError(
        msg='Authorization Error. Collaborator is banned or has not been approved by the admin.',
        status=401
    )

@bp.route('/<doc_id>/edit/infrastructure_types', methods=['PUT'])
@jwt_required
def edit_document_infrastructure_types(doc_id):
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

    # Verify if the given infrastrucutres are in the Infrastrucutre Collection
    try:
        for infra in body['infrastructure_types']:
            Infrastructure.objects.get(infrastructureType=infra)
    except:
        return ApiException(error_type='EditingError', message='Unable to find infrastructure', status=500)

    if not collab.banned:
        saved_id = put_doc_infrasType(str(collab.id), doc_id, body['infrastructure_types'])

        return ApiResult(
            message=f'Edited infrastructure types of the document {saved_id}.'
        )

    raise TellSpaceAuthError(
        msg='Authorization Error. Collaborator is banned or has not been approved by the admin.',
        status=401
    )

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

    try:
        for damage in body['damage_types']:
            Damage.objects.get(damageType=damage)
    except:
        return ApiException(error_type='EditingError', message='Unable to find damage type', status=500)

    if not collab.banned:
        saved_id = put_doc_damageType(collab.id, doc_id, body['damage_types'])
        return ApiResult(
            message=f'Edited damage types of the document {saved_id}.'
        )

    raise TellSpaceAuthError(
        msg='Authorization Error. Collaborator is banned or has not been approved by the admin.',
        status=401
    )

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
        saved_id = put_doc_locations(collab.id, doc_id, body['locations'])

        return ApiResult(message=f'Edited locations of the document {saved_id}.')

    raise TellSpaceAuthError(
        msg='Authorization Error. Collaborator is banned or has not been approved by the admin.',
        status=401
    )

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
        saved_id = put_doc_tags(collab.id, doc_id, body['tags'])

        return ApiResult(message=f'Edited tags of the document {saved_id}.')

    raise TellSpaceAuthError(
        msg='Authorization Error. Collaborator is banned or has not been approved by the admin.',
        status=401
    )

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
        saved_id = put_doc_incidentDate(collab.id, doc_id, body["incident_date"])

        return ApiResult(message=f'Edited incident date of the document {saved_id}.')

    raise TellSpaceAuthError(
        msg='Authorization Error. Collaborator is banned or has not been approved by the admin.',
        status=401
    )

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
        saved_id = put_doc_actors(collab.id, doc_id, body['actors'])
        return ApiResult(message=f'Updated actors on document {saved_id}.')

    raise TellSpaceAuthError(
        msg='Authorization Error. Collaborator is banned or has not been approved by the admin.',
        status=401
    )

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
        saved_id = put_doc_authors(collab.id, doc_id, body['authors'])

        return ApiResult(body=f'Updated authors on document: {saved_id}')

    raise TellSpaceAuthError(
        msg='Authorization Error. Collaborator is banned or has not been approved by the admin.',
        status=401
    )
