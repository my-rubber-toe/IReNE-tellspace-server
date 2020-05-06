from mongoengine import *
from TS_DAOs.schema_DB import *
import datetime
import json
from utils.exceptions import TellSpaceApiError


# from TS_DAOs.init_db_test import *

#Revision history

def create_revision_document(updated_document, revision_type):
    return DocumentCaseRevision(
        creatorId = updated_document.creatoriD,
        docId = updated_document.id,
        creator_name = updated_document.creatoriD.first_name + " " + updated_document.creatoriD.last_name,
        creator_email = updated_document.creatoriD.email,
        document_title = updated_document.title,
        revision_date = datetime.datetime.today().strftime('%Y-%m-%d'),
        revision_number = str(DocumentCaseRevision.objects(creatorId = updated_document.creatoriD, docId = updated_document.id).count()),
        revision_type = revision_type
    )


def log_document_edit_author(updated_document, old_authors):
    revDoc = create_revision_document(updated_document, 'Author')
    revDoc.field_changed = FieldsEmbedded(
        new = AuthorEmbedded(author = updated_document.author),
        old = AuthorEmbedded(author = old_authors))
    revDoc.save()
    print(revDoc.field_changed.to_json())

def log_document_edit_actor(updated_document, old_actors):
    revDoc = create_revision_document(updated_document, 'Actor')
    revDoc.field_changed = FieldsEmbedded(
        new = ActorEmbedded(actor = updated_document.actor),
        old = ActorEmbedded(actor = old_actors))
    revDoc.save()
    print(revDoc.field_changed.to_json())

def log_document_edit_incident(updated_document, old_incident_dates):
    revDoc = create_revision_document(updated_document, 'Incident Date')
    revDoc.field_changed = FieldsEmbedded(
        new = IncidentEmbedded(incidentDate = updated_document.incidentDate),
        old = IncidentEmbedded(incidentDate = old_incident_dates))
    revDoc.save()
    print(revDoc.field_changed.to_json())


def log_document_edit_tags(updated_document, old_tags):
    revDoc = create_revision_document(updated_document, 'Tag')
    revDoc.field_changed = FieldsEmbedded(
        new = TagEmbedded(tagsDoc = updated_document.tagsDoc),
        old = TagEmbedded(tagsDoc = old_tags))
    revDoc.save()
    print(revDoc.field_changed.to_json())

def log_document_edit_location(updated_document, old_locations):
    revDoc = create_revision_document(updated_document, 'Location')
    revDoc.field_changed = FieldsEmbedded(
        new = LocationEmbedded(location = updated_document.location),
        old = LocationEmbedded(location = old_locations))
    revDoc.save()
    print(revDoc.field_changed.to_json())

def log_document_edit_damage(updated_document, old_damages):
    revDoc = create_revision_document(updated_document, 'Damage')
    revDoc.field_changed = FieldsEmbedded(
        new = DamageEmbedded(damageDocList = updated_document.damageDocList),
        old = DamageEmbedded(damageDocList = old_damages))
    revDoc.save()
    print(revDoc.field_changed.to_json())

def log_document_edit_infrastructure(updated_document, old_infrastructures):
    revDoc = create_revision_document(updated_document, 'Infrastructure')
    revDoc.field_changed = FieldsEmbedded(
        new = InfrastructureEmbedded(infrasDocList = updated_document.infrasDocList),
        old = InfrastructureEmbedded(infrasDocList = old_infrastructures))
    revDoc.save()
    print(revDoc.field_changed.to_json())

def log_document_edit_section(updated_document, old_section, sec_num):
    revDoc = create_revision_document(updated_document, 'Section')
    revDoc.field_changed = FieldsEmbedded(
        new = SectionEmbedded(section = updated_document.section[sec_num-1]),
        old = SectionEmbedded(section = old_section))
    revDoc.save()
    print(revDoc.field_changed.to_json())

def log_document_deletion_section(updated_document, old_section):
    revDoc = create_revision_document(updated_document, 'Section')
    revDoc.field_changed = FieldsEmbedded(
        new = SectionEmbedded(section = None),
        old = SectionEmbedded(section = old_section))
    revDoc.save()
    print(revDoc.field_changed.to_json())

def log_document_creation_section(updated_document, new_section):
    revDoc = create_revision_document(updated_document, 'Section')
    revDoc.field_changed = FieldsEmbedded(
        new = SectionEmbedded(section = new_section),
        old = SectionEmbedded(section = None))
    revDoc.save()
    print(revDoc.field_changed.to_json())


def log_document_edit_timeline(updated_document, oldDates):
    revDoc = create_revision_document(updated_document, 'Timeline')
    revDoc.field_changed = FieldsEmbedded(
        new = TimelineEmbedded(timeline = updated_document.timeline),
        old = TimelineEmbedded(timeline = oldDates))
    revDoc.save()
    print(revDoc.field_changed.to_json())

def log_document_edit_description(updated_document, previousDescription):
    revDoc = create_revision_document(updated_document, 'Description')
    revDoc.field_changed = FieldsEmbedded(
        new = DescriptionEmbedded(description = updated_document.description),
        old = DescriptionEmbedded(description = previousDescription))
    revDoc.save()
    print(revDoc.field_changed.to_json())

def log_document_edit_title(updated_document, previousTitle):
    revDoc = create_revision_document(updated_document, 'Title')
    revDoc.field_changed = FieldsEmbedded(
        new = TitleEmbedded(title = updated_document.title),
        old = TitleEmbedded(title = previousTitle))
    revDoc.save()
    DocumentCaseRevision.objects(docId = updated_document.id, creatorId = updated_document.creatoriD).update(document_title = updated_document.title )
    print(revDoc.field_changed.to_json())

def log_document_creation(document):
    revDoc = create_revision_document(document, 'Creation')
    revDoc.field_changed = FieldsEmbedded(
        new = CreationEmbedded(creatoriD=document.creatoriD, title=document.title, description=document.description,
                        incidentDate=document.incidentDate, creationDate=document.creationDate,
                        lastModificationDate=document.lastModificationDate,
                        tagsDoc=[], infrasDocList=document.infrasDocList, damageDocList=document.damageDocList,
                        location=[], author=document.author, actor=document.actor,
                        section=[], timeline=[], language=document.language),
        old = CreationEmbedded())
    revDoc.save()
    print(revDoc.field_changed.to_json())

def log_document_deletion(document):
    revDoc = create_revision_document(document, 'Deletion')
    revDoc.field_changed = FieldsEmbedded(
        new = CreationEmbedded(),
        old = CreationEmbedded(creatoriD=document.creatoriD, title=document.title, description=document.description,
                        incidentDate=document.incidentDate, creationDate=document.creationDate,
                        lastModificationDate=document.lastModificationDate,
                        tagsDoc=document.tagsDoc, infrasDocList=document.infrasDocList, damageDocList=document.damageDocList,
                        location=document.location, author=document.author, actor=document.actor,
                        section=document.section, timeline=document.timeline, language=document.language))
    revDoc.save()
    print(revDoc.field_changed.to_json())

#End Document Revision__________________________________________________________________


def post_create_doc_DAO(**docatr):
    """
        DAO that posts a Doc into the DB & any new Tag is added to Tag Document
    """
    authorList = []
    for author in docatr['author']:
        authorBody = Author(author_FN=author['first_name'], author_LN=author['last_name'],
                            author_email=author['email'], author_faculty=author['faculty'])
        authorList.append(authorBody)
    actorList = []
    for actor in docatr['actor']:
        actorBody = Actor(actor_FN=actor['first_name'], actor_LN=actor['last_name'],
                          role=actor['role'])
        actorList.append(actorBody)
    doc1 = DocumentCase(creatoriD=docatr["creatoriD"], title=docatr["title"], description=docatr["description"],
                        incidentDate=docatr["incidentDate"], creationDate=docatr["creationDate"],
                        lastModificationDate=docatr["lastModificationDate"],
                        tagsDoc=[], infrasDocList=docatr["infrasDocList"], damageDocList=docatr["damageDocList"],
                        location=[], author=authorList, actor=actorList,
                        section=[], timeline=[], language=docatr["language"])
    # for tag in docatr["tagsDoc"]:
    #     if not Tag.objects(tagItem=tag):
    #         newTag = Tag(tagItem=tag)
    #         newTag.save()
    doc1.save()
    #Revision History
    log_document_creation(doc1)
    print('Document created successfully')
    return doc1


def get_me(email_collab):
    """
        DAO that returns a json object with the information about a collaborator
    """
    get_collab = Collaborator.objects.get(email=email_collab)
    return get_collab


def get_doc_collab(collabid):
    """
        DAO that returns a json object with the information about documents 
        created by a collaborator
    """
    get_docs = DocumentCase.objects.filter(creatoriD=collabid)
    response = []
    for doc in get_docs:
        doc: DocumentCase
        response.append({
            "id": str(doc.id),
            "title": doc.title,
            "description": doc.description,
            "published": doc.published,
            "incidentDate": doc.incidentDate,
            "creationDate": doc.creationDate,
            "lastModificationDate": doc.lastModificationDate
        })
    return response
    # return json.loads(response.to_json())


def get_doc(docid):
    """
        DAO that returns a json object with the information about a specific document
    """
    get_doc = DocumentCase.objects.get(id=docid)
    return json.loads(get_doc.to_json())


# def current_date():
#     """
#         This is not a DAO, the purpose is to get current date to change lastModificationDate
#     """
#     d = datetime.datetime.today()
#     if(d.month < 10 and d.day > 9):
#         current_date =  str(d.year) + "-0" + str(d.month) + "-" + str(d.day)
#     elif(d.day < 10 and d.month > 9):
#         current_date =  str(d.year) + "-" + str(d.month) + "-0" + str(d.day)
#     elif(d.day < 10 and d.month < 10):
#         current_date =  str(d.year) + "-0" + str(d.month) + "-0" + str(d.day)
#     else:
#         current_date =  str(d.year) + "-" + str(d.month) + "-" + str(d.day)
#     return current_date

def put_doc_title(docid, title):
    """
        DAO that updates the title of a document
    """
    previousTitle = DocumentCase.objects.get(id=docid).title
    DocumentCase.objects(id=docid).update_one(set__title=title)
    DocumentCase.objects(id=docid).update_one(set__lastModificationDate=datetime.datetime.today().strftime('%Y-%m-%d'))
    updatedDoc = DocumentCase.objects.get(id=docid)
    log_document_edit_title(updatedDoc, previousTitle)
    return updatedDoc


def put_doc_des(docid, des):
    """
        DAO that updates the description of a document
    """
    previousDescription = DocumentCase.objects.get(id=docid).description
    DocumentCase.objects(id=docid).update_one(set__description=des)
    DocumentCase.objects(id=docid).update_one(set__lastModificationDate=datetime.datetime.today().strftime('%Y-%m-%d'))
    updatedDoc = DocumentCase.objects.get(id=docid)
    log_document_edit_description(updatedDoc, previousDescription)
    return updatedDoc


def put_doc_timeline(**docatr):
    """
        DAO that updates the timeline of a document
    """
    oldTimeline = DocumentCase.objects.get(id=docatr["docid"]).timeline
    timelineList = []
    for timel in docatr["timeline"]:
        timelineBody = Timeline(
            event=timel['event'],
            eventStartDate=timel['event_start_date'].strftime('%Y-%m-%d'),
            eventEndDate=timel['event_end_date'].strftime('%Y-%m-%d')
        )
        timelineList.append(timelineBody)
    DocumentCase.objects(id=docatr["docid"]).update_one(set__timeline=timelineList)
    DocumentCase.objects(id=docatr["docid"]).update_one(
        set__lastModificationDate=datetime.datetime.today().strftime('%Y-%m-%d'))
    updatedDoc = DocumentCase.objects.get(id=docatr["docid"])
    log_document_edit_timeline(updatedDoc, oldTimeline)
    return updatedDoc


def put_doc_section(docid, sec_title, sec_content, sec_num):
    """
        DAO that updates the section of a document
    """
    doc = DocumentCase.objects.get(id=docid)
    old_section = doc.section[sec_num - 1]
    updateSection = Section(secTitle=sec_title, content=sec_content)
    doc.section[sec_num - 1] = updateSection
    doc.save()
    # DocumentCase.objects(id = docid, section__secNum = i).update_one(set__section__S = updateSection)
    DocumentCase.objects(id=docid).update_one(set__lastModificationDate=datetime.datetime.today().strftime('%Y-%m-%d'))
    log_document_edit_section(doc, old_section, sec_num)
    return DocumentCase.objects.get(id=docid)


def put_doc_incidentDate(docid, inDate):
    """
        DAO that updates the incident of a document
    """
    old_incident_dates = DocumentCase.objects.get(id=docid).incidentDate
    DocumentCase.objects(id=docid).update_one(set__incidentDate=inDate)
    DocumentCase.objects(id=docid).update_one(set__lastModificationDate=datetime.datetime.today().strftime('%Y-%m-%d'))
    updated_document = DocumentCase.objects.get(id=docid)
    log_document_edit_incident(updated_document, old_incident_dates)
    return updated_document


def put_doc_damageType(docid, damType):
    """
        DAO that updates the damagelist of a document
    """
    old_damages = DocumentCase.objects.get(id=docid).damageDocList
    DocumentCase.objects(id=docid).update_one(set__damageDocList=damType)
    DocumentCase.objects(id=docid).update_one(set__lastModificationDate=datetime.datetime.today().strftime('%Y-%m-%d'))
    updated_document = DocumentCase.objects.get(id=docid)
    log_document_edit_damage(updated_document, old_damages)
    return updated_document


def put_doc_infrasType(docid, infrasType):
    """
        DAO that updates the infrastructure list of a document
    """
    old_infrastructures = DocumentCase.objects.get(id=docid).infrasDocList
    DocumentCase.objects(id=docid).update_one(set__infrasDocList=infrasType)
    DocumentCase.objects(id=docid).update_one(set__lastModificationDate=datetime.datetime.today().strftime('%Y-%m-%d'))
    updated_doc = DocumentCase.objects.get(id=docid)
    log_document_edit_infrastructure(updated_doc, old_infrastructures)
    return updated_doc


def put_doc_tags(docid, tags):
    """
        DAO that updates the tags list of a document
    """
    old_tags = DocumentCase.objects.get(id=docid).tagsDoc
    DocumentCase.objects(id=docid).update_one(set__tagsDoc=tags)
    DocumentCase.objects(id=docid).update_one(set__lastModificationDate=datetime.datetime.today().strftime('%Y-%m-%d'))
    for tag in tags:
        if not Tag.objects(tagItem=tag):
            newTag = Tag(tagItem=tag)
            newTag.save()
    updated_document = DocumentCase.objects.get(id=docid)
    log_document_edit_tags(updated_document, old_tags)
    return updated_document


def put_doc_locations(docid, loc):
    """
        DAO that updates the location list of a document
    """
    old_locations = DocumentCase.objects.get(id=docid).location
    DocumentCase.objects(id=docid).update_one(set__location=loc)
    DocumentCase.objects(id=docid).update_one(set__lastModificationDate=datetime.datetime.today().strftime('%Y-%m-%d'))
    updated_document = DocumentCase.objects.get(id=docid)
    log_document_edit_location(updated_document, old_locations)
    return updated_document


def put_doc_actors(docid, actors):
    """
        DAO that updates the actors list of a document
    """
    old_actors = DocumentCase.objects.get(id=docid).actor
    actorList = []
    for actor in actors:
        actorBody = Actor(actor_FN=actor["first_name"], actor_LN=actor["last_name"],
                          role=actor["role"])
        actorList.append(actorBody)
    DocumentCase.objects(id=docid).update_one(set__actor=actorList)
    DocumentCase.objects(id=docid).update_one(set__lastModificationDate=datetime.datetime.today().strftime('%Y-%m-%d'))
    updated_document = DocumentCase.objects.get(id=docid)
    log_document_edit_actor(updated_document, old_actors)
    return updated_document


def put_doc_authors(docid, authors):
    """
        DAO that updates the authors list of a document
    """
    old_authors = DocumentCase.objects.get(id=docid).author
    authorList = []
    for author in authors:
        authorBody = Author(author_FN=author["first_name"], author_LN=author["last_name"],
                            author_email=author["email"], author_faculty=author["faculty"])
        authorList.append(authorBody)
    DocumentCase.objects(id=docid).update_one(set__author=authorList)
    DocumentCase.objects(id=docid).update_one(set__lastModificationDate=datetime.datetime.today().strftime('%Y-%m-%d'))
    updated_document = DocumentCase.objects.get(id=docid)
    log_document_edit_author(updated_document, old_authors)
    return updated_document


def get_infrastructure_list():
    """
        DAO that returns the list of infras
    """
    infras = []
    for infra in Infrastructure.objects():
        infras.append(infra.infrastructureType)
    return infras


def get_damage_list():
    """
        DAO that returns the list of damages
    """
    arr = []
    for d in Damage.objects():
        d: Damage
        arr.append(d.damageType)
    return arr


def get_tags_list():
    """
        DAO that returns the list of tags
    """
    arr = []
    for t in Tag.objects():
        t: Tag
        arr.append(t.tagItem)
    return arr


def post_doc_section(docid):
    """
        DAO that creates a new section 
    """
    doc = DocumentCase.objects.get(id=docid)
    new_section = Section()
    new_section.secTitle = f'Section No. {len(doc.section) + 1}'
    new_section.content = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod...'

    post_sec = DocumentCase.objects.get(id=docid)
    post_sec.section.append(new_section)
    post_sec.save()
    DocumentCase.objects(id=docid).update_one(set__lastModificationDate=datetime.datetime.today().strftime('%Y-%m-%d'))
    updated_doc = DocumentCase.objects.get(id=docid)
    log_document_creation_section(updated_doc, new_section)
    return updated_doc


def remove_doc(doc_id, collab_id):
    """
        DAO that removes a document
    """
    doc_del = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab_id)).delete()
    #Revision History
    log_document_deletion(doc_del)
    return doc_del


def remove_doc_section(docid, section_num):
    """
        DAO that deletes a section
    """
    doc = DocumentCase.objects.get(id=docid)
    if int(section_num) > len(doc.section) or int(section_num) <= 0:
        raise TellSpaceApiError(msg='Section No. does not exist.')
    section = doc.section.pop(int(section_num) - 1)
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
    log_document_deletion_section(doc, section)
    return doc


def get_doc_damage_type(damage):
    """
        DAO that returns the documents containing damage category
    """
    get_docs = DocumentCase.objects.filter(damageDocList__contains=damage)
    return json.loads(get_docs.to_json())


def get_doc_infrastructure_type(infras):
    """
        DAO that returns the documents containing infras category
    """
    get_docs = DocumentCase.objects.filter(infrasDocList__contains=infras)
    return json.loads(get_docs.to_json())


def get_doc_tag_type(tag):
    """
        DAO that returns the documents containing tag category
    """
    get_docs = DocumentCase.objects.filter(tagsDoc__contains=tag)
    return json.loads(get_docs.to_json())


