from database.daos.revision import *
import datetime
from utils.exceptions import TellSpaceApiError
from pymongo.errors import DocumentTooLarge

def post_create_doc_DAO(**docatr):
    """
        DAO that posts a Doc into the DB & any new Tag is added to Tag Document
    """
    author_list = []
    for authorDoc in docatr['author']:
        author_list.append(author(author_FN=authorDoc['first_name'], author_LN=authorDoc['last_name'],
                                  author_email=authorDoc['email'], author_faculty=authorDoc['faculty']))
    actor_list = []
    for actorDoc in docatr['actor']:
        actor_list.append(actor(actor_FN=actorDoc['first_name'], actor_LN=actorDoc['last_name'], role=actorDoc['role']))

    doc1 = document_case(
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
    try:
        doc1.save()
    except DocumentTooLarge as db_error:
        raise TellSpaceApiError(err=db_error, msg='Document limit reached', status=507)
    log_document_creation(doc1)
    return doc1


def post_doc_section(collab_id, docid):
    """
        DAO that creates a new section 
    """
    doc: document_case = document_case.objects.get(id=docid, creatoriD=collab_id)

    # Section limit reached
    if len(doc.section) == 10:
        raise TellSpaceApiError(err='SectionError', msg='Section limit reached')

    new_section = section()
    new_section.secTitle = f'Section Number {len(doc.section) + 1}'
    new_section.content = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod...'
    doc.section.append(new_section)
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    try:
        doc.save()
    except DocumentTooLarge as db_error:
        raise TellSpaceApiError(err=db_error, msg='Document limit reached', status=507)
    log_document_creation_section(doc, new_section)
    return document_case.objects.get(id=docid)
