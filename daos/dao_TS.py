from mongoengine import *
from schema_DB import *
import datetime
import json

def post_create_doc_DAO (**docatr):
    # authorDoc = []
    # for author in docatr["authorList"]:
    #     auth = Author(author_FN = author.first_name, author_LN = author.last_name, author_email = author.email, 
    #     author_faculty = author.faculty)
    #     authorDoc.append(auth)
    # actorDoc = []
    # for actor in docatr["actorList"]:
    #     act = Actor(actor_FN = actor.first_name, actor_LN = actor.last_name, role = actor.role)
    #     actorDoc.append(act)
    # timelineDoc = []
    # for tl in docatr["timelineList"]:
    #     timel = Timeline(event = tl.event, eventDate = tl.eventDate)
    #     timelineDoc.append(timel)
    # sectionDoc = []
    # for sec in docatr["sectionList"]:
    #     secdoc = Section(secTitle = sec.title, content = sec.content)
    #     timelineDoc.append(secdoc)
    doc1 = DocumentCase(creatoriD = docatr["creatoriD"],title = docatr["title"], description = docatr["description"],
    incidentDate = docatr["incidentDate"], creationDate = docatr["creationDate"],
    tagsDoc = docatr["tagsDoc"], infrasDocList = docatr["infrasDocList"], damageDocList = docatr["damageDocList"],
    location = docatr["location"], author = docatr["author"], actor = docatr["actor"], 
    section = docatr["section"], timeline = docatr["timeline"])
    for tag in docatr["tagsDoc"]:
        if not Tag.objects(tagItem=tag):
            newTag = Tag(tagItem=tag)
            newTag.save()
    doc1.save()


def get_me(email_collab):
    get_collab = Collaborator.objects.get(email = email_collab)
    return json.loads(get_collab.to_json())

def get_doc_collab(collabid):
    get_docs = Document.objects.filter(creatoriD= collabid)
    return json.loads(get_docs.to_json())

def get_doc(docid):
    get_doc = DocumentCase.objects.get(id = docid)
    return json.loads(get_doc.to_json())

def put_doc_title(docid, title):
    DocumentCase.objects(id = docid).update_one(set__title = title)

def put_doc_des(docid, des):
    DocumentCase.objects(id = docid).update_one(set__description = des)

def put_doc_timeline(docid, timeline):
    DocumentCase.objects(id = docid).update_one(set__timeline = timeline)

def put_doc_section(docid, sec):
    DocumentCase.objects(id = docid).update_one(set__section = sec)

def put_doc_damageType(docid, damType):
    DocumentCase.objects(id = docid).update_one(set__damageDocList = damType)
   
def put_doc_infrasType(docid,infrasType):
    DocumentCase.objects(id = docid).update_one(set__infrasDocList = infrasType)

def put_doc_locations(docid,loc):
    DocumentCase.objects(id = docid).update_one(set__location = loc)

def put_doc_actors(docid, actors):
    DocumentCase.objects(id = docid).update_one(set__actor = actors)

def put_doc_authors(docid, authors):
    DocumentCase.objects(id = docid).update_one(set__author = authors)

def put_doc_tags(docid, tags):
    DocumentCase.objects(id = docid).update_one(set__tagsDoc = tags)
    for tag in tags:
        if not Tag.objects(tagItem=tag):
            newTag = Tag(tagItem=tag)
            newTag.save()

def get_infrastructure_list():
    infra_objects = Infrastructure.objects()
    return json.loads(infra_objects.to_json())
   
def get_damage_list():
    damage_objects = Damage.objects()
    return json.loads(damage_objects.to_json())

def get_tags_list():
    tag_objects = Tag.objects()
    return json.loads(tag_objects.to_json())

def post_doc_section(docid,section):
    post_sec = DocumentCase.objects.get(id = docid)
    post_sec.section.append(section)
    post_sec.save()

def remove_doc(docid):
    doc_del = DocumentCase.objects.get(id = docid)
    doc_del.delete() 

def remove_doc_section(docid, section_title):
    DocumentCase.objects(id = docid).update(pull__section__secTitle= section_title)

def get_doc_damage_type(damage):
    get_docs = DocumentCase.objects.filter(damageDocList__contains = damage)
    return json.loads(get_docs.to_json())

def get_doc_infrastructure_type(infras):
    get_docs = DocumentCase.objects.filter(infrasDocList__contains = infras)
    return json.loads(get_docs.to_json())

def get_doc_tag_type(tag):
    get_docs = DocumentCase.objects.filter(tagsDoc__contains = tag)
    return json.loads(get_docs.to_json()) 
