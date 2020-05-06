from mongoengine import *
from TS_DAOs.schema_DB import *
import datetime
import json
from utils.exceptions import TellSpaceApiError


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

#END OF REVISION

def post_create_doc_DAO(**docatr):
    """
        DAO that posts a Doc into the DB & any new Tag is added to Tag Document
    """
    author_list = []
    for author in docatr['author']:
        author_list.append(Author(author_FN=author['first_name'], author_LN=author['last_name'],
                                  author_email=author['email'], author_faculty=author['faculty']))
    actor_list = []
    for actor in docatr['actor']:
        actor_list.append(Actor(actor_FN=actor['first_name'], actor_LN=actor['last_name'], role=actor['role']))

    doc1 = DocumentCase(
        creatoriD=docatr["creatoriD"],
        title=docatr["title"],
        incidentDate=docatr["incidentDate"],
        creationDate=docatr["creationDate"],
        lastModificationDate=docatr["lastModificationDate"],
        tagsDoc=[],
        infrasDocList=docatr["infrasDocList"],
        damageDocList=docatr["damageDocList"],
        location=[], author=author_list, actor=actor_list,
        section=[],
        timeline=[],
        language=docatr["language"]
    )
    doc1.save()
    log_document_creation(doc1)
    return doc1


def get_me(email_collab):
    """
        DAO that returns a json object with the information about a collaborator
    """
    get_collab = Collaborator.objects.get(email=email_collab)
    return get_collab


def get_doc_collab(collab_id):
    """
        DAO that returns a json object with the information about documents 
        created by a collaborator
    """
    get_docs = DocumentCase.objects.filter(creatoriD=collab_id)
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


def get_doc(docid, collabId):
    """
        DAO that returns a json object with the information about a specific document
    """
    doc = DocumentCase.objects.get(id=docid, creatoriD=collabId)

    # Only return address names
    location_names = []
    for l in doc.location:
        location_names.append(l['address'])

    doc_json = json.loads(doc.to_json())
    doc_json['location'] = location_names

    return doc_json


def put_doc_title(collab_id, doc_id, title):
    """
        DAO that updates the title of a document
    """
    doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab_id))
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
    doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab_id))
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
        timelineBody = Timeline(event=timel['event'],
                                eventStartDate=str(timel['event_start_date']),
                                eventEndDate=str(timel['event_end_date']))
        new_timeline_list.append(timelineBody)

    doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab_id))
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

    doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab_id))

    # Section doesn't exist
    if sec_num > len(doc.section) or sec_num <= 0:
        raise TellSpaceApiError(err='SectionError', msg='Section No. does not exist.')

    new_section_content = Section(secTitle=sec_title, content=sec_content)
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

    doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab_id))
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
    doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab_id))
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
    doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab_id))
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
    doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab_id))

    # Create tag if it doesnt exist in the database
    for tag in tags:
        if not Tag.objects(tagItem=tag):
            newTag = Tag(tagItem=tag)
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

        # Todo: Change to only get location instance with one query search
        city_pr = CityPR.objects.get(city=location)
        loc_body = Location(address=city_pr.city, latitude=city_pr.latitude, longitude=city_pr.longitude)
        new_locations.append(loc_body)

    doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab_id))
    previous_locations = doc.location
    doc.location = new_locations
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
    log_document_edit_location(doc, previous_locations)
    return doc.id


def put_doc_actors(collab_id, doc_id, actors):
    """
        DAO that updates the actors list of a document
    """
    new_actors = []
    for actor in actors:
        actor_body = Actor(actor_FN=actor["first_name"], actor_LN=actor["last_name"], role=actor["role"])
        new_actors.append(actor_body)

    doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab_id))
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
    for author in authors:
        author_body = Author(author_FN=author["first_name"], author_LN=author["last_name"],
                             author_email=author["email"], author_faculty=author["faculty"])
        new_author_list.append(author_body)

    doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab_id))
    previous_authors = doc.author
    doc.author = new_author_list
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
    log_document_edit_author(doc, previous_authors)
    return doc.id


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


def post_doc_section(collab_id, docid):
    """
        DAO that creates a new section 
    """
    doc: DocumentCase = DocumentCase.objects.get(id=docid, creatoriD=str(collab_id))

    # Section limit reached
    if len(doc.section) == 10:
        raise TellSpaceApiError(err='SectionError', msg='Section limit reached')

    new_section = Section()
    new_section.secTitle = f'Section No. {len(doc.section) + 1}'
    new_section.content = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod...'
    doc.section.append(new_section)
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
    log_document_creation_section(doc, new_section)
    return DocumentCase.objects.get(id=docid)


def remove_doc(collab_id, doc_id):
    """
        DAO that removes a document
    """
    doc_del: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=collab_id)
    doc_del.delete()
    log_document_deletion(doc_del)
    return doc_del.id


def remove_doc_section(collab_id, doc_id, section_num):
    """
        DAO that deletes a section
    """

    doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab_id))

    # Section doesn't exist
    if section_num > len(doc.section) or section_num <= 0:
        raise TellSpaceApiError(err='SectionError', msg='Section No. does not exist.')

    # Remember that lists start with index 0
    removed_section = doc.section.pop(int(section_num) - 1)
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
    log_document_deletion_section(doc, removed_section)
    return doc.id


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
