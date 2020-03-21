from mongoengine import *
from schema_DB import *
import datetime

def post_create_doc_DAO (**docatr):
    authorDoc = []
    for author in docatr["authorList"]:
        auth = Author(author_FN = author.first_name, author_LN = author.last_name, author_email = author.email, 
        author_faculty = author.faculty)
        authorDoc.append(auth)
    actorDoc = []
    for actor in docatr["actorList"]:
        act = Actor(actor_FN = actor.first_name, actor_LN = actor.last_name, role = actor.role)
        actorDoc.append(act)
    timelineDoc = []
    for tl in docatr["timelineList"]:
        timel = Timeline(event = tl.event, eventDate = tl.eventDate)
        timelineDoc.append(timel)
    sectionDoc = []
    for sec in docatr["sectionList"]:
        secdoc = Section(secTitle = sec.title, content = sec.content)
        timelineDoc.append(secdoc)
    doc1 = DocumentCase(title = docatr["title"], description = docatr["des"],
    incidentDate = docatr["inDate"], creationDate = docatr["crDate"],
    tagsDoc = docatr["tags"], infrasDocList = docatr["infraList"], damageDocList = docatr["damList"],
    location = docatr["locList"], author = authorDoc, actor = actorDoc, section = sectionDoc,
    timeline = timelineDoc)
    doc1.save()
    
def get_me(idcollab):
    return Collaborator.objects.get(email = idcollab)

def get_doc(idcolab):
    return DocumentCase.objects.filter(title = idcolab)

def put_doc_title(docid, title):
    DocumentCase.objects(title = docid).update_one(set__title = title)

def put_doc_des(docid, des):
    DocumentCase.objects(title = docid).update_one(set__description = des)

def put_doc_timeline( docid, timeline):
    DocumentCase.objects(title = docid).update_one(set__timeline = timeline)

def put_doc_section(docid, sec):
    DocumentCase.objects(title = docid).update_one(set__section = sec)

def put_doc_damageType(docid, damType):
    DocumentCase.objects(title = docid).update_one(set__damageDocList = damType)
   
def put_doc_infrasType(docid,infrasType):
    DocumentCase.objects(title = docid).update_one(set__infrasDocList = infrasType)

def put_doc_locations(docid,loc):
    DocumentCase.objects(title = docid).update_one(set__location = loc)

def put_doc_actors(docid, actors):
    DocumentCase.objects(title = docid).update_one(set__actor = actors)

def pit_doc_authors(docid, authors):
    DocumentCase.objects(title = docid).update_one(set__author = authors)

def pit_doc_tags(docid, tags):
    DocumentCase.objects(title = docid).update_one(set__tagsDoc = tags)
    

