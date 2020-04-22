from mongoengine import *
from database.schema_DB import *
import datetime
import json


def post_create_doc_DAO(**docatr):
    """
        DAO that posts a Doc into the DB & any new Tag is added to Tag Document
    """
    doc1 = DocumentCase(
        creatoriD=docatr["creatoriD"],
        title=docatr["title"],
        description=docatr["description"],
        incidentDate=docatr["incidentDate"],
        creationDate=docatr["creationDate"],
        lastModificationDate=docatr["lastModificationDate"],
        tagsDoc=docatr["tagsDoc"],
        infrasDocList=docatr["infrasDocList"],
        damageDocList=docatr["damageDocList"],
        location=docatr["location"],
        author=docatr["author"],
        actor=docatr["actor"],
        section=docatr["section"],
        timeline=docatr["timeline"],
        language=docatr["language"]
    )
    for tag in docatr["tagsDoc"]:
        if not Tag.objects(tagItem=tag):
            newTag = Tag(tagItem=tag)
            newTag.save()
    doc1.save()
    print('Document created successfully')


def get_me(email_collab):
    """
        DAO that returns a json object with the information about a collaborator
    """
    get_collab = Collaborator.objects.get(email=email_collab)
    return json.loads(get_collab.to_json())


def get_doc_collab(collabid):
    """
        DAO that returns a json object with the information about documents
        created by a collaborator
    """
    get_docs = DocumentCase.objects.filter(creatoriD=collabid)
    return json.loads(get_docs.to_json())


def get_doc(docid):
    """
        DAO that returns a json object with the information about a specific document
    """
    get_doc = DocumentCase.objects.get(id=docid)
    return json.loads(get_doc.to_json())


def current_date():
    """
        This is not a DAO, the purpose is to get current date to change lastModificationDate
    """
    d = datetime.datetime.today()
    if (d.month < 10 and d.day > 9):
        current_date = str(d.year) + "-0" + str(d.month) + "-" + str(d.day)
    elif (d.day < 10 and d.month > 9):
        current_date = str(d.year) + "-" + str(d.month) + "-0" + str(d.day)
    elif (d.day < 10 and d.month < 10):
        current_date = str(d.year) + "-0" + str(d.month) + "-0" + str(d.day)
    else:
        current_date = str(d.year) + "-" + str(d.month) + "-" + str(d.day)
    return current_date


def put_doc_title(docid, title):
    """
        DAO that updates the title of a document
    """
    DocumentCase.objects(id=docid).update_one(set__title=title)
    DocumentCase.objects(id=docid).update_one(set__lastModificationDate=current_date())


def put_doc_des(docid, des):
    """
        DAO that updates the description of a document
    """
    DocumentCase.objects(id=docid).update_one(set__description=des)
    DocumentCase.objects(id=docid).update_one(set__lastModificationDate=current_date())


def put_doc_timeline(docid, timeline):
    """
        DAO that updates the timeline of a document
    """
    DocumentCase.objects(id=docid).update_one(set__timeline=timeline)
    DocumentCase.objects(id=docid).update_one(set__lastModificationDate=current_date())


def put_doc_section(docid, sec):
    """
        DAO that updates the section of a document
    """
    DocumentCase.objects(id=docid).update_one(set__section=sec)
    DocumentCase.objects(id=docid).update_one(set__lastModificationDate=current_date())


def put_doc_damageType(docid, damType):
    """
        DAO that updates the damagelist of a document
    """
    DocumentCase.objects(id=docid).update_one(set__damageDocList=damType)
    DocumentCase.objects(id=docid).update_one(set__lastModificationDate=current_date())


def put_doc_infrasType(docid, infrasType):
    """
        DAO that updates the infrastructure list of a document
    """
    DocumentCase.objects(id=docid).update_one(set__infrasDocList=infrasType)
    DocumentCase.objects(id=docid).update_one(set__lastModificationDate=current_date())


def put_doc_tags(docid, tags):
    """
        DAO that updates the tags list of a document
    """
    DocumentCase.objects(id=docid).update_one(set__tagsDoc=tags)
    DocumentCase.objects(id=docid).update_one(set__lastModificationDate=current_date())
    for tag in tags:
        if not Tag.objects(tagItem=tag):
            newTag = Tag(tagItem=tag)
            newTag.save()


def put_doc_locations(docid, loc):
    """
        DAO that updates the location list of a document
    """
    DocumentCase.objects(id=docid).update_one(set__location=loc)
    DocumentCase.objects(id=docid).update_one(set__lastModificationDate=current_date())


def put_doc_actors(docid, actors):
    """
        DAO that updates the actors list of a document
    """
    DocumentCase.objects(id=docid).update_one(set__actor=actors)
    DocumentCase.objects(id=docid).update_one(set__lastModificationDate=current_date())


def put_doc_authors(docid, authors):
    """
        DAO that updates the authors list of a document
    """
    DocumentCase.objects(id=docid).update_one(set__author=authors)
    DocumentCase.objects(id=docid).update_one(set__lastModificationDate=current_date())


def get_infrastructure_list():
    """
        DAO that returns the list of infras
    """
    infra_objects = Infrastructure.objects()
    return json.loads(infra_objects.to_json())


def get_damage_list():
    """
        DAO that returns the list of damages
    """
    damage_objects = Damage.objects()
    return json.loads(damage_objects.to_json())


def get_tags_list():
    """
        DAO that returns the list of tags
    """
    tag_objects = Tag.objects()
    return json.loads(tag_objects.to_json())


def post_doc_section(docid, section):
    post_sec = DocumentCase.objects.get(id=docid)
    post_sec.section.append(section)
    post_sec.save()


def remove_doc(docid):
    """
        DAO that removes a document
    """
    doc_del = DocumentCase.objects.get(id=docid)
    doc_del.delete()


def remove_doc_section(docid, section_title):
    """
        DAO that deletes a section
    """
    DocumentCase.objects(id=docid).update(pull__section__secTitle=section_title)


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
