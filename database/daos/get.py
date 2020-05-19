""""

This file contains all the GET related operations on the database.

Author: Jainel Torres <jainel.torres@upr.edu>
CoAuthor: Roberto Guzmán <roberto.guzman3@upr.edu>

"""

from database.daos.revision import *
import json

def get_me(email_collab):
    """
        DAO that returns a json object with the information about a collaborator
    """
    get_collab = collaborator.objects.get(email=email_collab)
    return get_collab


def get_doc_collab(collab_id):
    """
        DAO that returns a json object with the information about documents 
        created by a collaborator
    """
    get_docs = document_case.objects.filter(creatoriD=collab_id)
    response = []
    for doc in get_docs:
        doc: document_case
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
    doc: document_case = document_case.objects.get(id=docid, creatoriD=collabId)

    # Only return address names
    location_names = []
    for l in doc.location:
        location_names.append(l['address'])

    doc_json = json.loads(doc.to_json())
    doc_json['location'] = location_names

    return doc_json

def get_infrastructure_list():
    """
        DAO that returns the list of infras
    """
    infras = []
    for infra in infrastructure.objects():
        infras.append(infra.infrastructureType)
    return infras


def get_damage_list():
    """
        DAO that returns the list of damages
    """
    arr = []
    for d in damage.objects():
        d: damage
        arr.append(d.damageType)
    return arr


def get_tags_list():
    """
        DAO that returns the list of tags
    """
    arr = []
    for t in tag.objects():
        t: tag
        arr.append(t.tagItem)
    return arr

def get_doc_damage_type(damage):
    """
        DAO that returns the documents containing damage category
    """
    get_docs = document_case.objects.filter(damageDocList__contains=damage)
    return json.loads(get_docs.to_json())


def get_doc_infrastructure_type(infras):
    """
        DAO that returns the documents containing infras category
    """
    get_docs = document_case.objects.filter(infrasDocList__contains=infras)
    return json.loads(get_docs.to_json())


def get_doc_tag_type(tag):
    """
        DAO that returns the documents containing tag category
    """
    get_docs = document_case.objects.filter(tagsDoc__contains=tag)
    return json.loads(get_docs.to_json())