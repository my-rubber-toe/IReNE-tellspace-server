dao\_test module
================

- DAO_TS_1 (Dao which creates a Document)
   - post_create_doc_DAO(creatoriD = creatoriD,author = authlist,actor = actlist, timeline = timelineDoc,
   section = sectionDoc, title = title, description = description, language= language, 
   incidentDate = incidentDate,creationDate = creationDate, lastModificationDate=lastModificationDate,
   tagsDoc = tagsDoclist, infrasDocList = infrasDocList, damageDocList = infrasDocList, location = location)
- DAO_TS_2 (Dao returns a json object with the information of a collaborator)
   - get_me(collab)
- DAO_TS_5 (Dao returns a json object with the information of a document created by the collaborator provided as argument)
   - get_doc_collab(collab)
- DAO_TS_6 (Dao returns a json object with the information of a specific document
   - get_doc(docID)
- DAO_TS_7 (Dao updates the title of a doc)
   - put_doc_title(doc_id, change_title)
- DAO_TS_8 (Dao updates the description of a doc)
   - put_doc_des(doc_id, change_description)
- DAO_TS_9 (Dao updates the timeline of a doc)
   - put_doc_timeline(doc_id, change_list_timel)
- DAO_TS_10 (Dao updates the section of a doc)
   - put_doc_section(doc_id, change_list_section)
- DAO_TS_11 (Dao updates the damagelist of a doc)
   - put_doc_damageType(doc_id, change_list_damage)
- DAO_TS_12 (Dao updates the infraslist of a doc)
   - put_doc_infrasType(doc_id, change_list_infra)
- DAO_TS_13 (Dao updates the tags of a doc)
   - put_doc_tags(doc_id, change_list_tags)
- DAO_TS_14 (Dao updates the locationlist of a doc)
   - put_doc_locations(doc_id, change_list_loc)
- DAO_TS_15 (Dao updates the actors of a doc)
   - put_doc_actors(doc_id, change_list_actor)
- DAO_TS_16 (Dao updates the authors of a doc)
   - put_doc_authors(doc_id, change_list_author)
- DAO_TS_17 (Dao return lists of different categories)
   - get_infrastructure_list()
   - get_damage_list()
   - get_tags_list()
- DAO_TS_18 (Dao deletes a document)
   - remove_doc(doc_id)
- DAO_TS_19 (DAO that returns a list of documents based on a category infras given)
   - get_doc_infrastructure_type(category)

.. automodule:: dao_test
   :members:

