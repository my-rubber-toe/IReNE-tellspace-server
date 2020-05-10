from database.schemas import *
import datetime
import json
from utils.exceptions import TellSpaceApiError


def create_revision_document(updated_document, revision_type):
    """
        Revision function for creating a revision document, 
        it will serve as a notification that a revision document was created.
    """
    return document_case_revision(
        creatorId=updated_document.creatoriD,
        docId=updated_document.id,
        creator_name=updated_document.creatoriD.first_name + " " + updated_document.creatoriD.last_name,
        creator_email=updated_document.creatoriD.email,
        document_title=updated_document.title,
        revision_date=datetime.datetime.today().strftime('%Y-%m-%d'),
        revision_number= document_case_revision.objects(creatorId=updated_document.creatoriD, docId=updated_document.id).count(),
        revision_type=revision_type
    )


def log_document_edit_author(updated_document, old_authors):
    """
        Revision function for editing an author, 
        it will serve as a notification that a document's authors was updated.
    """
    revDoc = create_revision_document(updated_document, 'author')
    revDoc.field_changed = fields_embedded(
        new=author_embedded(author=updated_document.author),
        old=author_embedded(author=old_authors))
    revDoc.save()


def log_document_edit_actor(updated_document, old_actors):
    """
        Revision function for editing an actor, 
        it will serve as a notification that a document's actors was updated.
    """
    revDoc = create_revision_document(updated_document, 'actor')
    revDoc.field_changed = fields_embedded(
        new=actor_embedded(actor=updated_document.actor),
        old=actor_embedded(actor=old_actors))
    revDoc.save()


def log_document_edit_incident(updated_document, old_incident_dates):
    """
        Revision function for editing the incident date, 
        it will serve as a notification that a document's incident date was updated.
    """
    revDoc = create_revision_document(updated_document, 'incident_date')
    revDoc.field_changed = fields_embedded(
        new=incident_embedded(incidentDate=updated_document.incidentDate),
        old=incident_embedded(incidentDate=old_incident_dates))
    revDoc.save()


def log_document_edit_tags(updated_document, old_tags):
    """
        Revision function for editing the tags of a document, 
        it will serve as a notification that a document's tags was updated.
    """
    revDoc = create_revision_document(updated_document, 'tag')
    revDoc.field_changed = fields_embedded(
        new=tag_embedded(tagsDoc=updated_document.tagsDoc),
        old=tag_embedded(tagsDoc=old_tags))
    revDoc.save()


def log_document_edit_location(updated_document, old_locations):
    """
        Revision function for editing the locations, 
        it will serve as a notification that a document's locations was updated.
    """
    revDoc = create_revision_document(updated_document, 'location')
    revDoc.field_changed = fields_embedded(
        new=location_embedded(location=updated_document.location),
        old=location_embedded(location=old_locations))
    revDoc.save()


def log_document_edit_damage(updated_document, old_damages):
    """
        Revision function for editing the categories selected for damage type, 
        it will serve as a notification that a document's categories for damage type was updated.
    """
    revDoc = create_revision_document(updated_document, 'damage')
    revDoc.field_changed = fields_embedded(
        new=damage_embedded(damageDocList=updated_document.damageDocList),
        old=damage_embedded(damageDocList=old_damages))
    revDoc.save()


def log_document_edit_infrastructure(updated_document, old_infrastructures):
    """
        Revision function for editing the infrastructure types, 
        it will serve as a notification that a document's categories for infrastructure types was updated.
    """
    revDoc = create_revision_document(updated_document, 'infrastructure')
    revDoc.field_changed = fields_embedded(
        new=infrastructure_embedded(infrasDocList=updated_document.infrasDocList),
        old=infrastructure_embedded(infrasDocList=old_infrastructures))
    revDoc.save()


def log_document_edit_section(updated_document, old_section, sec_num):
    """
        Revision function for editing the sections, 
        it will serve as a notification that a document's sections was updated.
    """
    revDoc = create_revision_document(updated_document, 'section')
    revDoc.field_changed = fields_embedded(
        new=section_embedded(section=updated_document.section[sec_num - 1]),
        old=section_embedded(section=old_section))
    revDoc.save()


def log_document_deletion_section(updated_document, old_section):
    """
        Revision function for deleting a section, 
        it will serve as a notification that a section was deleted from a document.
    """
    revDoc = create_revision_document(updated_document, 'section')
    revDoc.field_changed = fields_embedded(
        new=section_embedded(section=None),
        old=section_embedded(section=old_section))
    revDoc.save()


def log_document_creation_section(updated_document, new_section):
    """
        Revision function for creating a section, 
        it will serve as a notification that a section was added to a document.
    """
    revDoc = create_revision_document(updated_document, 'section')
    revDoc.field_changed = fields_embedded(
        new=section_embedded(section=new_section),
        old=section_embedded(section=None))
    revDoc.save()


def log_document_edit_timeline(updated_document, oldDates):
    """
        Revision function for editing the timeline, 
        it will serve as a notification that a document's timeline was updated.
    """
    revDoc = create_revision_document(updated_document, 'timeline')
    revDoc.field_changed = fields_embedded(
        new=timeline_embedded(timeline=updated_document.timeline),
        old=timeline_embedded(timeline=oldDates))
    revDoc.save()


def log_document_edit_description(updated_document, previousDescription):
    """
        Revision function for editing the description, 
        it will serve as a notification that a document's description was updated.
    """
    revDoc = create_revision_document(updated_document, 'description')
    revDoc.field_changed = fields_embedded(
        new=description_embedded(description=updated_document.description),
        old=description_embedded(description=previousDescription))
    revDoc.save()


def log_document_edit_title(updated_document, previousTitle):
    """
        Revision function for editing the title, 
        it will serve as a notification that a document's title was updated.
    """
    revDoc = create_revision_document(updated_document, 'title')
    revDoc.field_changed = fields_embedded(
        new=title_embedded(title=updated_document.title),
        old=title_embedded(title=previousTitle))
    revDoc.save()
    document_case_revision.objects(docId=updated_document.id, creatorId=updated_document.creatoriD).update(
        document_title=updated_document.title)


def log_document_creation(document):
    """
        Revision function for creating a case study, 
        it will serve as a notification that a case study was created.
    """
    revDoc = create_revision_document(document, 'creation')
    revDoc.field_changed = fields_embedded(
        new=creation_embedded(creatoriD=document.creatoriD, title=document.title, description=document.description,
                             incidentDate=document.incidentDate, creationDate=document.creationDate,
                             lastModificationDate=document.lastModificationDate,
                             tagsDoc=[], infrasDocList=document.infrasDocList, damageDocList=document.damageDocList,
                             location=[], author=document.author, actor=document.actor,
                             section=[], timeline=[], language=document.language),
        old=creation_embedded())
    revDoc.save()


def log_document_deletion(document):
    """
        Revision function for deleting a function, 
        it will serve as a notification that a document was deleted.
    """
    revDoc = create_revision_document(document, 'deletion')
    revDoc.field_changed = fields_embedded(
        new=creation_embedded(),
        old=creation_embedded(creatoriD=document.creatoriD, title=document.title, description=document.description,
                             incidentDate=document.incidentDate, creationDate=document.creationDate,
                             lastModificationDate=document.lastModificationDate,
                             tagsDoc=document.tagsDoc, infrasDocList=document.infrasDocList,
                             damageDocList=document.damageDocList,
                             location=document.location, author=document.author, actor=document.actor,
                             section=document.section, timeline=document.timeline, language=document.language))
    revDoc.save()