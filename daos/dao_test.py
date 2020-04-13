from mongoengine import *
from schema_DB import *
from dao_TS import *
import datetime

"""
    DAO_TS_1 (Dao which creates a Document)
"""
# auth1 = Author(author_FN = "author.first_name1", author_LN = "author.last_name1",
# author_email = "author.email1@upr.edu", author_faculty = "author.faculty1")
# auth2 = Author(author_FN = "author.first_name2", author_LN = "author.last_name2",
# author_email = "author.email2@upr.edu", author_faculty = "author.faculty2")
# authlist = [auth1,auth2]
# act1 = Actor(actor_FN = "actor.first_name", actor_LN = "actor.last_name", role = "actor.role")
# actlist = [act1]
# timel = Timeline(event = "The timeline title", eventStartDate='2010-09-12', eventEndDate='2010-09-20')
# timelineDoc = [timel]
# secdoc = Section(secTitle = "sec.title", content = "sec.content")
# sectionDoc = [secdoc]
# post_create_doc_DAO(creatoriD = "HEJB482ND9bbY9hYV",author = authlist,actor = actlist, timeline = timelineDoc,
# section = sectionDoc, title = "The", description = "Description about case study", language='English', 
# incidentDate = '2009-09-20',creationDate = '2011-07-12', lastModificationDate='2015-10-13',
# tagsDoc = ["tag1","tag2"], infrasDocList = ["infras10"], damageDocList = ["dam10"], location = ["loc10"])

"""
    DAO_TS_2 (Dao returns a json object with the information of a collaborator)
"""
# collab = "jainel.torres@upr.edu"
# get = get_me(collab)
# print(get)

"""
    DAO_TS_5 (Dao returns a json object with the information of a document created by 
    the collaborator provided as argument)
"""
# collabID = Collaborator.objects()
# ids = []
# for x in collabID:
#     id_string = str(x.id)
#     ids.append(id_string)
# print(ids)
# collab = ''
# list_docs = get_doc_collab(collab)
# print(list_docs)

"""
    DAO_TS_6 (Dao returns a json object with the information of a specific document
"""
# docID = DocumentCase.objects()
# ids = []
# for x in docID:
#     id_string = str(x.id)
#     ids.append(id_string)
# print(ids)
# doc = "5e93df65d5a7e105bb954dda"
# get_doc = get_doc(doc)
# print(get_doc)


"""
    DAO_TS_7 (Dao updates the title of a doc)
"""
# docID = DocumentCase.objects()
# ids = []
# for x in docID:
#     id_string = str(x.id)
#     ids.append(id_string)
# print(ids)
# change_title = "Into the unknown"
# doc_id = "5e93df65d5a7e105bb954dda"
# current_title = get = DocumentCase.objects.get(id =doc_id)
# print("old title: " + current_title.title)
# put_doc_title(doc_id, change_title)
# new_title = DocumentCase.objects.get(id =doc_id)
# print("new title: " + new_title.title)
# print("new mod date: " + new_title.lastModificationDate)

"""
    DAO_TS_8 (Dao updates the description of a doc)
"""
# docID = DocumentCase.objects()
# ids = []
# for x in docID:
#     id_string = str(x.id)
#     ids.append(id_string)
# print(ids)
# change_description = "It was really bad what happened"
# doc_id = "5e93df65d5a7e105bb954dda"
# current = DocumentCase.objects.get(id =doc_id)
# print("old des: " + current.description)
# put_doc_des(doc_id, change_description)
# new = DocumentCase.objects.get(id =doc_id)
# print("new des: " + new.description)
# print("new mod date: " + new.lastModificationDate)


"""
    DAO_TS_9 (Dao updates the timeline of a doc)
"""
# docID = DocumentCase.objects()
# ids = []
# for x in docID:
#     id_string = str(x.id)
#     ids.append(id_string)
# print(ids)
# doc_id = "5e93df65d5a7e105bb954dda"
# change_timel1 = Timeline(event = "this is the event1", eventStartDate = "2018-09-19", eventEndDate= '2018-10-01')
# change_timel2 = Timeline(event = "this is the event2", eventStartDate = "2019-09-19", eventEndDate= '2019-10-01')
# change_list_timel = [change_timel1, change_timel2]
# current = DocumentCase.objects.get(id =doc_id)
# for x in range(0, len(current.timeline)):
#     print('old timeline ',x, ': ', current.timeline[x].event, current.timeline[x].eventStartDate, current.timeline[x].eventEndDate )
# put_doc_timeline(doc_id, change_list_timel)
# new = DocumentCase.objects.get(id =doc_id)
# for x in range(0, len(new.timeline)):
#     print('new timeline ',x, ': ', new.timeline[x].event, new.timeline[x].eventStartDate, new.timeline[x].eventEndDate )
# print("new mod date: " + new.lastModificationDate)

"""
    DAO_TS_10 (Dao updates the section of a doc)
"""
# docID = DocumentCase.objects()
# ids = []
# for x in docID:
#     id_string = str(x.id)
#     ids.append(id_string)
# print(ids)
# doc_id = "5e93df65d5a7e105bb954dda"
# change_section1 = Section(secTitle = "Title", content = "content1")
# change_section2 = Section(secTitle = "title2", content = "content2")
# change_list_section = [change_section1, change_section2]
# current = DocumentCase.objects.get(id =doc_id)
# for x in range(0, len(current.section)):
#     print('old section ',x,': ',current.section[x].secTitle, current.section[x].content)
# put_doc_section(doc_id, change_list_section)
# new = DocumentCase.objects.get(id =doc_id)
# for x in range(0, len(new.section)):
#     print('new section ',x,': ',new.section[x].secTitle, new.section[x].content)
# print("new mod date: " + new.lastModificationDate)

"""
    DAO_TS_11 (Dao updates the damagelist of a doc)
"""
# docID = DocumentCase.objects()
# ids = []
# for x in docID:
#     id_string = str(x.id)
#     ids.append(id_string)
# print(ids)
# doc_id = "5e93df65d5a7e105bb954dda"
# change_list_damage = ["change_damage1", "change_damage2"]
# current = DocumentCase.objects.get(id =doc_id)
# print('old damagelist ', current.damageDocList)
# put_doc_damageType(doc_id, change_list_damage)
# new = DocumentCase.objects.get(id =doc_id)
# print('new damagelist ', new.damageDocList)
# print("new mod date: " + new.lastModificationDate)

"""
    DAO_TS_12 (Dao updates the infraslist of a doc)
"""
# docID = DocumentCase.objects()
# ids = []
# for x in docID:
#     id_string = str(x.id)
#     ids.append(id_string)
# print(ids)
# doc_id = "5e93df65d5a7e105bb954dda"
# change_list_infra = ["infra1", "infra2"]
# current = DocumentCase.objects.get(id =doc_id)
# print('old infraslist ', current.infrasDocList)
# put_doc_infrasType(doc_id, change_list_infra)
# new = DocumentCase.objects.get(id =doc_id)
# print('new infraslist ', new.infrasDocList)
# print("new mod date: " + new.lastModificationDate)

"""
    DAO_TS_13 (Dao updates the tags of a doc)
"""
# docID = DocumentCase.objects()
# ids = []
# for x in docID:
#     id_string = str(x.id)
#     ids.append(id_string)
# print(ids)
# doc_id = "5e93df65d5a7e105bb954dda"
# change_list_tags = ["tag1", "tag2"]
# current = DocumentCase.objects.get(id =doc_id)
# print('old tagslist ', current.tagsDoc)
# put_doc_tags(doc_id, change_list_tags)
# new = DocumentCase.objects.get(id =doc_id)
# print('new tagslist ', new.tagsDoc)
# print("new mod date: " + new.lastModificationDate)


"""
    DAO_TS_14 (Dao updates the locationlist of a doc)
"""
# docID = DocumentCase.objects()
# ids = []
# for x in docID:
#     id_string = str(x.id)
#     ids.append(id_string)
# print(ids)
# doc_id = "5e93df65d5a7e105bb954dda"
# change_list_loc = ["loc1", "loc2"]
# current = DocumentCase.objects.get(id =doc_id)
# print('old locations ', current.location)
# put_doc_locations(doc_id, change_list_loc)
# new = DocumentCase.objects.get(id =doc_id)
# print('new locations ', new.location)
# print("new mod date: " + new.lastModificationDate)

"""
    DAO_TS_15 (Dao updates the actors of a doc)
"""
# docID = DocumentCase.objects()
# ids = []
# for x in docID:
#     id_string = str(x.id)
#     ids.append(id_string)
# print(ids)
# doc_id = "5e93df65d5a7e105bb954dda"
# change_actor1 = Actor(actor_FN = "name1", actor_LN = "lname1", role = "role1")
# change_actor2 = Actor(actor_FN = "name2", actor_LN = "lname2", role = "role2")
# change_list_actor = [change_actor1, change_actor2]
# current = DocumentCase.objects.get(id = doc_id)
# for x in range(0, len(current.actor)):
#     print('old actor ',x, ': ',current.actor[x].actor_FN, current.actor[x].actor_LN, current.actor[x].role)
# put_doc_actors(doc_id, change_list_actor)
# update_actor = DocumentCase.objects.get(id = doc_id)
# for x in range(0, len(update_actor.actor)):
#     print('new actor ',x, ': ',update_actor.actor[x].actor_FN, update_actor.actor[x].actor_LN, update_actor.actor[x].role)
# print("new mod date: " + update_actor.lastModificationDate)

"""
    DAO_TS_16 (Dao updates the authors of a doc)
"""
# docID = DocumentCase.objects()
# ids = []
# for x in docID:
#     id_string = str(x.id)
#     ids.append(id_string)
# print(ids)
# doc_id = "5e93df65d5a7e105bb954dda"
# current = DocumentCase.objects.get(id = doc_id)
# for x in range(0, len(current.author)):
#     print('old author ',x, ': ',current.author[x].author_FN, current.author[x].author_LN,
#     current.author[x].author_email,current.author[x].author_faculty)
# change_author1 = Author(author_FN = "auname1", author_LN = "aulname1", 
# author_email = "au.email1@upr.edu", author_faculty = "aufaculty1")
# change_author2 = Author(author_FN = "auname2", author_LN = "aulname2", 
# author_email = "au.email2@upr.edu",author_faculty = "aufaculty2")
# change_list_author = [change_author1, change_author2]
# put_doc_authors(doc_id, change_list_author)
# update_author = DocumentCase.objects.get(id=doc_id)
# for x in range(0, len(update_author.author)):
#     print('new author ',x, ': ',update_author.author[x].author_FN, update_author.author[x].author_LN, 
#     update_author.author[x].author_email, update_author.author[x].author_faculty)
# print("new mod date: " + update_author.lastModificationDate)

"""
    DAO_TS_17 (Dao return lists of different categories)
"""
# print(get_infrastructure_list())
# print(get_damage_list())
# print(get_tags_list())

"""
    DAO_TS_18 (Dao deletes a document)
"""
# docID = DocumentCase.objects()
# ids = []
# for x in docID:
#     id_string = str(x.id)
#     ids.append(id_string)
# print(ids)
# doc_id = '5e9400bea9de4e0d0ba11f37'
# current_titles = DocumentCase.objects()
# print('current titles:')
# for x in current_titles:
#     print(x.title)
# remove_doc(doc_id)
# new_titles = DocumentCase.objects()
# print('new titles:')
# for x in new_titles:
#     print(x.title)

""" 
    DAO_TS_19 (DAO that returns a list of documents based on a category infras given)
"""
# category = 'Structure'
# print(get_doc_infrastructure_type(category))

