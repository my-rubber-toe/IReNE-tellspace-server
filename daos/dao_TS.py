from mongoengine import *
from daos.schema_DB import *
import datetime

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
    return Collaborator.objects.get(email = email_collab)

def get_doc(title_doc):
    return DocumentCase.objects.filter(title = title_doc)

def put_doc_title(title_doc, title):
    DocumentCase.objects(title = title_doc).update_one(set__title = title)

def put_doc_des(title_doc, des):
    DocumentCase.objects(title = title_doc).update_one(set__description = des)

def put_doc_timeline( title_doc, timeline):
    DocumentCase.objects(title = title_doc).update_one(set__timeline = timeline)

def put_doc_section(title_doc, sec):
    DocumentCase.objects(title = title_doc).update_one(set__section = sec)

def put_doc_damageType(title_doc, damType):
    DocumentCase.objects(title = title_doc).update_one(set__damageDocList = damType)
   
def put_doc_infrasType(title_doc,infrasType):
    DocumentCase.objects(title = title_doc).update_one(set__infrasDocList = infrasType)

def put_doc_locations(title_doc,loc):
    DocumentCase.objects(title = title_doc).update_one(set__location = loc)

def put_doc_actors(title_doc, actors):
    DocumentCase.objects(title = title_doc).update_one(set__actor = actors)

def put_doc_authors(title_doc, authors):
    DocumentCase.objects(title = title_doc).update_one(set__author = authors)

def put_doc_tags(title_doc, tags):
    DocumentCase.objects(title = title_doc).update_one(set__tagsDoc = tags)
    for tag in tags:
        if not Tag.objects(tagItem=tag):
            newTag = Tag(tagItem=tag)
            newTag.save()

def get_infrastructure_list ():
    infra_list = []
    infra_objects = Infrastructure.objects()
    for infra in infra_objects:
        infra_list.append(infra.infrastructureType)
    return infra_list

def get_damage_list():
    damage_list = []
    damage_objects = Damage.objects()
    for damage in damage_objects:
        damage_list.append(damage.damageType)
    return damage_list

def get_tags_list():
    tag_list = []
    tag_objects = Tag.objects()
    for tag in tag_objects:
        tag_list.append(tag.tagItem)
    return tag_list

def post_doc_section(title_doc,section):
    post_sec = DocumentCase.objects.get(title = title_doc)
    post_sec.section.append(section)
    post_sec.save()

def remove_doc(title_doc):
    doc_del = DocumentCase.objects.get(title = title_doc)
    doc_del.delete() 

def remove_doc_section(title_doc, section_title):
    DocumentCase.objects(title = title_doc).update(pull__section__secTitle= section_title)
