from database.schema_DB import *
from datetime import  datetime

# Sample author
sample_author = Author()
sample_author.author_FN = "Author Name"
sample_author.author_LN = "Author Last Name"
sample_author.author_faculty = "ININ"
sample_author.author_email = "author@author.com"

# sample Actor
sample_actor = Actor()
sample_actor.actor_FN = "Actor FN"
sample_actor.actor_LN = "Actor LN"
sample_actor.role = "Gerente de Puertos"

# sample section
sample_section = Section()
sample_section.secTitle = 'Section Title'
sample_section.content = 'Section content here'

#sample timeline
sample_timeline_pair = Timeline()
sample_timeline_pair.event = 'Timeline event'
sample_timeline_pair.eventDate = datetime.utcnow()

# sample damage
sample_damage_type1 = Damage()
sample_damage_type1.damageType = "Superficial"

sample_damage_type2 = Damage()
sample_damage_type2.damageType = "Corrosivo"

# sample infrastructure
sample_infrastructure1 = Infrastructure()
sample_infrastructure1.infrastructureType = "Puertos"
sample_infrastructure2 = Infrastructure()
sample_infrastructure2 = "Alcantarillas"






# Collaborators
collaborators = [];

collaborator_1 = Collaborator()
collaborator_1.id = '13579'
collaborator_1.first_name = 'Roberto'
collaborator_1.last_name = 'Guzman'
collaborator_1.email = 'roberto.guzman3@upr.edu'
collaborator_1.banned = False
collaborator_1.approved = True
collaborator_1.documentsID = ['1']

## Pepito is banned
collaborator_2 = Collaborator()
collaborator_2.id = '2468'
collaborator_2.first_name = 'Pepito'
collaborator_2.last_name = 'Perez'
collaborator_2.email = 'pepito.perez@upr.edu'
collaborator_2.banned = True
collaborator_2.approved = False
collaborator_2.documentsID = ['2']

collaborators.append(collaborator_1)
collaborators.append(collaborator_2)


# Documents
doc1 = DocumentCase()
doc1.creatoriD = collaborator_1.id
doc1.title = 'Sample Case'
doc1.description = 'Sample Description'
doc1.published = True
doc1.location =["Ponce", "Juana Diaz"]
doc1.incidentDate = datetime.utcnow()
doc1.creationDate = datetime.utcnow()
doc1.tagsDoc = ["electricidad", "tuberias"]
doc1.infrasDocList = ["Puertos", "Alcantarillas"]
doc1.damageDocList=["Superficial", "Corrosivo"]

doc1.author = [sample_author, sample_actor]
doc1.actor = [sample_actor, sample_actor]
doc1.section = [sample_section, sample_section, sample_section]
doc1.timeline = [sample_timeline_pair, sample_timeline_pair]

doc2 = DocumentCase()
doc2.creatoriD = collaborator_2.id
doc2.title = 'Sample Case'
doc2.description = 'Sample Description'
doc2.published = False
doc2.location =["Ponce", "Juana Diaz"]
doc2.incidentDate = datetime.utcnow()
doc2.creationDate = datetime.utcnow()
doc2.tagsDoc = ["electricidad", "tuberias"]
doc2.infrasDocList = ["Puertos", "Alcantarillas"]
doc2.damageDocList=["Superficial", "Corrosivo"]

doc2.author = [sample_author, sample_actor]
doc2.actor = [sample_actor, sample_actor]
doc2.section = [sample_section, sample_section, sample_section]
doc2.timeline = [sample_timeline_pair, sample_timeline_pair]




