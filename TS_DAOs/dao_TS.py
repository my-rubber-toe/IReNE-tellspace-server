from mongoengine import *
from TS_DAOs.schema_DB import *
import datetime
import json
from utils.exceptions import TellSpaceApiError


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
    number_cases = DocumentCase.objects(collab_id).aggregate()
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
    doc.title = title
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
    return doc.id


def put_doc_des(collab_id, doc_id, des):
    """
        DAO that updates the description of a document
    """
    doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab_id))
    doc.description = des
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
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
    doc.timeline = new_timeline_list
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
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
    doc.section[sec_num - 1] = new_section_content
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
    return doc.id


def put_doc_incidentDate(collab_id, doc_id, inDate):
    """
        DAO that updates the incident of a document
    """

    doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab_id))
    doc.incidentDate = str(inDate)
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()

    return doc.id


def put_doc_damageType(collab_id, doc_id, damType):
    """
        DAO that updates the damagelist of a document
    """
    doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab_id))
    doc.damageDocList = damType
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
    return doc.id


def put_doc_infrasType(collab_id, doc_id, infrasType):
    """
        DAO that updates the infrastructure list of a document
    """
    doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab_id))
    doc.infrasDocList = infrasType
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
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

    doc.tagsDoc = tags
    doc.save()

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
    doc.location = new_locations
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()

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
    doc.actor = new_actors
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
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
    doc.author = new_author_list
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
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
    return DocumentCase.objects.get(id=docid)


def remove_doc(collab_id, doc_id):
    """
        DAO that removes a document
    """
    doc_del: DocumentCase = DocumentCase.objects(creatoriD=str(collab_id)).get(id=doc_id)
    doc_del.delete()
    return doc_id


def remove_doc_section(collab_id, doc_id, section_num):
    """
        DAO that deletes a section
    """

    doc: DocumentCase = DocumentCase.objects.get(id=doc_id, creatoriD=str(collab_id))

    # Section doesn't exist
    if section_num > len(doc.section) or section_num <= 0:
        raise TellSpaceApiError(err='SectionError', msg='Section No. does not exist.')

    # Remember that lists start with index 0
    doc.section.pop(int(section_num) - 1)
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
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
