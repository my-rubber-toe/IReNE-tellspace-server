"""
    Author: Jainel M. Torres Santos <jainel.torres@upr.edu>
"""
from database.daos.revision import *
import datetime
from utils.exceptions import TellSpaceApiError

def remove_doc(collab_id, doc_id):
    """
        DAO that removes a document
    """
    doc_del: document_case = document_case.objects(creatoriD=collab_id).get(id=doc_id)
    doc_del.delete()
    log_document_deletion(doc_del)
    return doc_del.id


def remove_doc_section(collab_id, doc_id, section_num):
    """
        DAO that deletes a section
    """
    doc: document_case = document_case.objects.get(id=doc_id, creatoriD=collab_id)

    # Section doesn't exist
    if section_num > len(doc.section) or section_num <= 0:
        raise TellSpaceApiError(err='SectionError', msg='Section No. does not exist.')

    # Remember that lists start with index 0
    removed_section = doc.section.pop(int(section_num) - 1)
    doc.lastModificationDate = datetime.datetime.today().strftime('%Y-%m-%d')
    doc.save()
    log_document_deletion_section(doc, removed_section)
    return doc.id