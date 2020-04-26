from mongoengine import *
from TS_DAOs.schema_DB import *
import datetime
import json
# from TS_DAOs.init_db_test import *


def post_create_doc_DAO (**docatr):
    """
        DAO that posts a Doc into the DB & any new Tag is added to Tag Document
    """
    authorList = []
    for author in docatr['author']:
        authorBody = Author(author_FN= author['first_name'] , author_LN= author['last_name'], 
            author_email= author['email'], author_faculty= author['faculty'])
        authorList.append(authorBody)
    actorList = []
    for actor in docatr['actor']:
        actorBody = Actor(actor_FN= actor['first_name'], actor_LN= actor['last_name'], 
            role= actor['role'])
        actorList.append(actorBody)
    doc1 = DocumentCase(creatoriD = docatr["creatoriD"],title = docatr["title"], description = docatr["description"],
    incidentDate = docatr["incidentDate"], creationDate = docatr["creationDate"], lastModificationDate = docatr["lastModificationDate"],
    tagsDoc = [], infrasDocList = docatr["infrasDocList"], damageDocList = docatr["damageDocList"],
    location = [], author = authorList, actor = actorList, 
    section = [], timeline = [], language=docatr["language"])
    # for tag in docatr["tagsDoc"]:
    #     if not Tag.objects(tagItem=tag):
    #         newTag = Tag(tagItem=tag)
    #         newTag.save()
    doc1.save()
    print('Document created successfully')
    return doc1


def get_me(email_collab):
    """
        DAO that returns a json object with the information about a collaborator
    """
    get_collab = Collaborator.objects.get(email = email_collab)
    return get_collab


def get_doc_collab(collabid):
    """
        DAO that returns a json object with the information about documents 
        created by a collaborator
    """
    get_docs = DocumentCase.objects.filter(creatoriD= collabid)
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
    get_doc = DocumentCase.objects.get(id = docid)
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
    DocumentCase.objects(id = docid).update_one(set__title = title)
    DocumentCase.objects(id = docid).update_one(set__lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d'))
    return DocumentCase.objects.get(id = docid)


def put_doc_des(docid, des):
    """
        DAO that updates the description of a document
    """
    DocumentCase.objects(id = docid).update_one(set__description = des)
    DocumentCase.objects(id = docid).update_one(set__lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d'))
    return DocumentCase.objects.get(id = docid)

def put_doc_timeline(**docatr):
    """
        DAO that updates the timeline of a document
    """
    timelineList = []
    for timel in docatr["timeline"]:
        timelineBody = Timeline(event= timel['event'], 
        eventStartDate= timel['event_start_date'], 
        eventEndDate= timel['event_end_date'])
        timelineList.append(timelineBody)
    DocumentCase.objects(id = docatr["docid"]).update_one(set__timeline = timelineList)
    DocumentCase.objects(id = docatr["docid"]).update_one(set__lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d'))
    return DocumentCase.objects.get(id = docatr["docid"])

def put_doc_section(docid, sec_title, sec_content, sec_num):
    """
        DAO that updates the section of a document
    """
    doc = DocumentCase.objects.get(id = docid)
    updateSection = Section(secTitle= sec_title, content= sec_content)
    doc.section[sec_num - 1] = section
    doc.save()
    # DocumentCase.objects(id = docid, section__secNum = i).update_one(set__section__S = updateSection)
    DocumentCase.objects(id = docid).update_one(set__lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d'))
    return DocumentCase.objects.get(id = docid)

def put_doc_incidentDate(docid, inDate):
    """
        DAO that updates the incident of a document
    """
    DocumentCase.objects(id = docid).update_one(set__incidentDate = inDate)
    DocumentCase.objects(id = docid).update_one(set__lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d'))
    return DocumentCase.objects.get(id = docid)

def put_doc_damageType(docid, damType):
    """
        DAO that updates the damagelist of a document
    """
    DocumentCase.objects(id = docid).update_one(set__damageDocList = damType)
    DocumentCase.objects(id = docid).update_one(set__lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d'))
    return DocumentCase.objects.get(id = docid)
   
def put_doc_infrasType(docid,infrasType):
    """
        DAO that updates the infrastructure list of a document
    """
    DocumentCase.objects(id = docid).update_one(set__infrasDocList = infrasType)
    DocumentCase.objects(id = docid).update_one(set__lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d'))
    return DocumentCase.objects.get(id = docid)

def put_doc_tags(docid, tags):
    """
        DAO that updates the tags list of a document
    """
    DocumentCase.objects(id = docid).update_one(set__tagsDoc = tags)
    DocumentCase.objects(id = docid).update_one(set__lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d'))
    for tag in tags:
        if not Tag.objects(tagItem=tag):
            newTag = Tag(tagItem=tag)
            newTag.save()
    return DocumentCase.objects.get(id = docid)

def put_doc_locations(docid,loc):
    """
        DAO that updates the location list of a document
    """
    DocumentCase.objects(id = docid).update_one(set__location = loc)
    DocumentCase.objects(id = docid).update_one(set__lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d'))
    return DocumentCase.objects.get(id = docid)

def put_doc_actors(docid, actors):
    """
        DAO that updates the actors list of a document
    """
    actorList = []
    for actor in actors:
        actorBody = Actor(actor_FN= actor["first_name"], actor_LN= actor["last_name"], 
            role= actor["role"])
        actorList.append(actorBody)
    DocumentCase.objects(id = docid).update_one(set__actor = actorList)
    DocumentCase.objects(id = docid).update_one(set__lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d'))
    return DocumentCase.objects.get(id = docid)

def put_doc_authors(docid, authors):
    """
        DAO that updates the authors list of a document
    """
    authorList = []
    for author in authors:
        authorBody = Author(author_FN= author["first_name"], author_LN= author["last_name"], 
            author_email= author["email"], author_faculty= author["faculty"])
        authorList.append(authorBody)
    DocumentCase.objects(id = docid).update_one(set__author = authorList)
    DocumentCase.objects(id = docid).update_one(set__lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d'))
    return DocumentCase.objects.get(id = docid)

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
    doc = DocumentCase.objects.get(id = docid)
    new_section = Section()
    new_section.secTitle = f'Section No. {len(doc.section) + 1}'
    new_section.content = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod...'
        
    post_sec = DocumentCase.objects.get(id = docid)
    post_sec.section.append(new_section)
    post_sec.save()
    DocumentCase.objects(id = docid).update_one(set__lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d'))
    return DocumentCase.objects.get(id = docid)
    
def remove_doc(docid):
    """
        DAO that removes a document
    """
    doc_del = DocumentCase.objects.get(id = docid)
    doc_del.delete() 
    return DocumentCase.objects.get(id = docid)

def remove_doc_section(docid, section_num):
    """
        DAO that deletes a section
    """
    doc = DocumentCase.objects.get(id = docid)
    if section_num > len(doc.section) or section_num <= 0:
        raise TellSpaceApiError(msg='Section No. does not exist.')
    DocumentCase.objects(id = docid).update(pull__section__secNum= (section_num - 1))
    DocumentCase.objects(id = docid).update_one(set__lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d'))
    return DocumentCase.objects.get(id = docid)

def get_doc_damage_type(damage):
    """
        DAO that returns the documents containing damage category
    """
    get_docs = DocumentCase.objects.filter(damageDocList__contains = damage)
    return json.loads(get_docs.to_json())

def get_doc_infrastructure_type(infras):
    """
        DAO that returns the documents containing infras category
    """
    get_docs = DocumentCase.objects.filter(infrasDocList__contains = infras)
    return json.loads(get_docs.to_json())

def get_doc_tag_type(tag):
    """
        DAO that returns the documents containing tag category
    """
    get_docs = DocumentCase.objects.filter(tagsDoc__contains = tag)
    return json.loads(get_docs.to_json()) 

