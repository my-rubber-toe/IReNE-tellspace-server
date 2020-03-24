from mongoengine import *
from schema_DB import *
from dao_TS import *
import datetime

# Testing Dao get collaborator 
# col = Collaborator( first_name = "Aurora", 
# last_name = "Black", email = "aurora.black@upr.edu", faculty = "ICOM")
# col.save()
# collab = "aurora.black@upr.edu"
# get = get_me(collab)
# print(get)

# tesing DAO get list docs
doc = "The great Flooding"
get_doc = get_doc(doc)
print(get_doc)

#testing DAO update title
change_title = "The final countdown"
# put_doc_title(doc, change_title)
# update_title = DocumentCase.objects.get(title = "The final countdown")
# print(update_title.title)

#testing DAO update description
# change_des = "uff, it was bad"
# put_doc_des(change_title, change_des)
# update_des = DocumentCase.objects.get(title = "The final countdown")
# update_des.reload()
# print(update_des.description)

#testing DAO update timeline
# change_timel1 = Timeline(event = "event1", eventDate = datetime.datetime(2016,9,9))
# change_timel2 = Timeline(event = "event2", eventDate = datetime.datetime(2015,5,5))
# change_list_timel = [change_timel1, change_timel2]
# put_doc_timeline(change_title, change_list_timel)
# update_timel = DocumentCase.objects.get(title = "The final countdown")
# update_timel.reload()
# for x in range(0, len(update_timel.timeline)):
#     print(update_timel.timeline[x].event, update_timel.timeline[x].eventDate)

# testing DAO update section
# change_section1 = Section(secTitle = "Title", content = "content1")
# change_section2 = Section(secTitle = "title2", content = "content2")
# change_list_section = [change_section1, change_section2]
# put_doc_section(change_title, change_list_section)
# update_section = DocumentCase.objects.get(title = "The final countdown")
# update_section.reload()
# for x in range(0, len(update_section.section)):
#     print(update_section.section[x].secTitle, update_section.section[x].content)

# testing DAO update damagetype
# change_list_damage = ["change_damage1", "change_damage2"]
# put_doc_damageType(change_title, change_list_damage)
# update_damage = DocumentCase.objects.get(title = "The final countdown")
# update_damage.reload()
# for x in range(0, len(update_damage.damageDocList)):
#     print(update_damage.damageDocList[x])

# testing DAO update infrastructureType
# change_list_infra = ["infra1", "infra2"]
# put_doc_infrasType(change_title, change_list_infra)
# update_infra = DocumentCase.objects.get(title = "The final countdown")
# update_infra.reload()
# for x in range(0, len(update_infra.infrasDocList)):
#     print(update_infra.infrasDocList[x])

# testing DAO update locations
# change_list_loc = ["loc1", "loc2"]
# put_doc_locations(change_title, change_list_loc)
# update_loc = DocumentCase.objects.get(title = "The final countdown")
# update_loc.reload()
# for x in range(0, len(update_loc.location)):
#     print(update_loc.location[x])

# testing DAO update actor
# change_actor1 = Actor(actor_FN = "name1", actor_LN = "lname1", role = "role1")
# change_actor2 = Actor(actor_FN = "name2", actor_LN = "lname2", role = "role2")
# change_list_actor = [change_actor1, change_actor2]
# put_doc_actors(change_title, change_list_actor)
# update_actor = DocumentCase.objects.get(title = "The final countdown")
# update_actor.reload()
# for x in range(0, len(update_actor.actor)):
#     print(update_actor.actor[x].actor_FN, update_actor.actor[x].actor_LN, update_actor.actor[x].role)

#testing DAO update author
# change_author1 = Author(author_FN = "auname1", author_LN = "aulname1", 
# author_email = "auemail1@upr.edu", author_faculty = "aufaculty1")
# change_author2 = Author(author_FN = "auname2", author_LN = "aulname2", 
# author_email = "auemail2@upr.edu",author_faculty = "aufaculty2")
# change_list_author = [change_author1, change_author2]
# put_doc_authors(change_title, change_list_author)
# update_author = DocumentCase.objects.get(title = "The final countdown")
# update_author.reload()
# for x in range(0, len(update_author.author)):
#     print(update_author.author[x].author_FN, update_author.author[x].author_LN, 
#     update_author.author[x].author_email, update_author.author[x].author_faculty)

# testing DAO update tags
# change_list_tags = ["tag1", "tag2"]
# put_doc_tags(change_title, change_list_tags)
# update_tag = DocumentCase.objects.get(title = "The final countdown")
# update_tag.reload()
# for x in range(0, len(update_tag.tagsDoc)):
#     print(update_tag.tagsDoc[x])

# testing DAO post doc
# auth1 = Author(author_FN = "author.first_name1", author_LN = "author.last_name1",
# author_email = "author.email1@upr.edu", author_faculty = "author.faculty1")
# auth2 = Author(author_FN = "author.first_name2", author_LN = "author.last_name2",
# author_email = "author.email2@upr.edu", author_faculty = "author.faculty2")
# authlist = [auth1,auth2]
# act1 = Actor(actor_FN = "actor.first_name", actor_LN = "actor.last_name", role = "actor.role")
# actlist = [act1]
# timel = Timeline(event = "tl.event", eventDate = datetime.datetime(2010,2,2))
# timelineDoc = [timel]
# secdoc = Section(secTitle = "sec.title", content = "sec.content")
# sectionDoc = [secdoc]
# post_create_doc_DAO(creatoriD = "s",author = authlist,actor = actlist, timeline = timelineDoc,
# section = sectionDoc, title = "title10", description = "des10",
# incidentDate = datetime.datetime(2010,2,2),creationDate = datetime.datetime(2010,2,2),
# tagsDoc = ["tag1","tag2"], infrasDocList = ["infras10"], damageDocList = ["dam10"], location = ["loc10"])

#Testing DAO get Tag list, same process for Damage & Infrastructure list
# change the string, it will give an error if the tag already exist
# t = Tag(tagItem = "Hurricane")
# t.save()
# t1 = Tag(tagItem = "Flood")
# t1.save()
# print(get_tags_list())

#testing DAO post section
# sec1 = Section(secTitle = "Body", content="lol")
# post_doc_section("title10", sec1)
# test_sec = DocumentCase.objects.get(title = "title10")
# sec = 0
# for sec in range(0,len(test_sec.section)):
#     print(test_sec.section[sec].secTitle, test_sec.section[sec].content)