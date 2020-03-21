from mongoengine import *
from schema_DB import *
from dao_TS import *
import datetime

#returns collaborator object
collab = "aurora.black@upr.edu"
get = get_me(collab)
print(get.first_name)

#return list doc object
doc = "The great Flooding"
get_doc = get_doc(doc)
for x in get_doc: 
    print(x.title)

change_title = "The final countdown"
put_doc_title(doc, change_title)
update_title = DocumentCase.objects.get(title = "The final countdown")
print(update_title.title)

change_des = "uff, it was bad"
put_doc_des(change_title, change_des)
update_des = DocumentCase.objects.get(title = "The final countdown")
update_des.reload()
print(update_des.description)

# change_timel = "uff, it was bad"
# put_doc_des(change_title, change_des)
# update_des = DocumentCase.objects.get(title = "The final countdown")
# update_des.reload()
# print(update_des.description)