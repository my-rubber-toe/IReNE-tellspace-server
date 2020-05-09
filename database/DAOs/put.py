from database.schemas import *
from database.DAOs.revision import *
import datetime
import json
from utils.exceptions import TellSpaceApiError

def put_doc_title(collab_id, doc_id, title):
    """
        DAO that updates the title of a document
    """
    doc: document_case = document_case.objects.get(id=doc_id, creatoriD=collab_id)
    previous_title = doc.title
    doc.title = title
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
    log_document_edit_title(doc, previous_title)
    return doc.id


def put_doc_des(collab_id, doc_id, des):
    """
        DAO that updates the description of a document
    """
    doc: document_case = document_case.objects.get(id=doc_id, creatoriD=collab_id)
    previous_description = doc.description
    doc.description = des
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
    log_document_edit_description(doc, previous_description)
    return doc.id


def put_doc_timeline(collab_id, doc_id, timeline):
    """
        DAO that updates the timeline of a document
    """
    new_timeline_list = []
    for timel in timeline:
        timelineBody = timeline(event=timel['event'],
                                eventStartDate=str(timel['event_start_date']),
                                eventEndDate=str(timel['event_end_date']))
        new_timeline_list.append(timelineBody)

    doc: document_case = document_case.objects.get(id=doc_id, creatoriD=collab_id)
    previous_timeline = doc.timeline
    doc.timeline = new_timeline_list
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
    log_document_edit_timeline(doc, previous_timeline)
    return doc.id


def put_doc_section(collab_id, doc_id, sec_title, sec_content, sec_num):
    """
        DAO that updates the section of a document
    """

    doc: document_case = document_case.objects.get(id=doc_id, creatoriD=collab_id)

    # Section doesn't exist
    if sec_num > len(doc.section) or sec_num <= 0:
        raise TellSpaceApiError(err='SectionError', msg='Section No. does not exist.')

    new_section_content = section(secTitle=sec_title, content=sec_content)
    previous_section = doc.section[sec_num - 1]
    doc.section[sec_num - 1] = new_section_content
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
    log_document_edit_section(doc, previous_section, sec_num)
    return doc.id


def put_doc_incidentDate(collab_id, doc_id, inDate):
    """
        DAO that updates the incident of a document
    """

    doc: document_case = document_case.objects.get(id=doc_id, creatoriD=collab_id)
    previous_incidentDate = doc.incidentDate
    doc.incidentDate = str(inDate)
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
    log_document_edit_incident(doc, previous_incidentDate)
    return doc.id


def put_doc_damageType(collab_id, doc_id, damType):
    """
        DAO that updates the damagelist of a document
    """
    doc: document_case = document_case.objects.get(id=doc_id, creatoriD=collab_id)
    previous_damages = doc.damageDocList
    doc.damageDocList = damType
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
    log_document_edit_damage(doc, previous_damages)
    return doc.id


def put_doc_infrasType(collab_id, doc_id, infrasType):
    """
        DAO that updates the infrastructure list of a document
    """
    doc: document_case = document_case.objects.get(id=doc_id, creatoriD=collab_id)
    previous_infrastructure = doc.infrasDocList
    doc.infrasDocList = infrasType
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
    log_document_edit_infrastructure(doc, previous_infrastructure)
    return doc.id


def put_doc_tags(collab_id, doc_id, tags):
    """
        DAO that updates the tags list of a document
    """
    doc: document_case = document_case.objects.get(id=doc_id, creatoriD=collab_id)

    # Create tag if it doesnt exist in the database
    for tagdoc in tags:
        if not tag.objects(tagItem=tagdoc):
            newTag = tag(tagItem=tagdoc)
            newTag.save()
    previous_tags = doc.tagsDoc
    doc.tagsDoc = tags
    doc.save()
    log_document_edit_tags(doc, previous_tags)
    return doc.id


def put_doc_locations(collab_id, doc_id, locations_list):
    """
        DAO that updates the location list of a document
    """

    repeated_hash = dict()
    new_locations = []
    for location in locations_list:
        # Check repeated locations
        if repeated_hash.__contains__(location):
            raise TellSpaceApiError('RepeatedContentError', msg='One of the given locations is repeated')

        city_pr = city_pr.objects.get(city=location)
        loc_body = location(address=city_pr.city, latitude=city_pr.latitude, longitude=city_pr.longitude)
        new_locations.append(loc_body)

    doc: document_case = document_case.objects.get(id=doc_id, creatoriD=collab_id)
    # previous_locations = doc.location
    doc.location = new_locations
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
    # log_document_edit_location(doc, previous_locations)
    return doc.id


def put_doc_actors(collab_id, doc_id, actors):
    """
        DAO that updates the actors list of a document
    """
    new_actors = []
    for actorDoc in actors:
        actor_body = actor(actor_FN=actorDoc["first_name"], actor_LN=actorDoc["last_name"], role=actorDoc["role"])
        new_actors.append(actor_body)

    doc: document_case = document_case.objects.get(id=doc_id, creatoriD=collab_id)
    previous_actors = doc.actor
    doc.actor = new_actors
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
    log_document_edit_actor(doc, previous_actors)
    return doc.id


def put_doc_authors(collab_id, doc_id, authors):
    """
        DAO that updates the authors list of a document
    """
    new_author_list = []
    for authorDoc in authors:
        author_body = author(author_FN=authorDoc["first_name"], author_LN=authorDoc["last_name"],
                             author_email=authorDoc["email"], author_faculty=authorDoc["faculty"])
        new_author_list.append(author_body)

    doc: document_case = document_case.objects.get(id=doc_id, creatoriD=collab_id)
    previous_authors = doc.author
    doc.author = new_author_list
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
    log_document_edit_author(doc, previous_authors)
    return doc.id