from mongoengine import *
from config.development import DB_HOST
import json

# Connection to the Database, make sure you place the correct container name for the database
#connect('IReNEdb')
# connect('IReNEdb', host="mongodb://testuser:testpassword@localhost:27017/?authSource=admin")
#connect('IReNEdb', host=DB_HOST)

disconnect()
# connec the db for testing purposes
#connect('IReNEdb', host='mongomock://localhost:27017')
connect('testdb')


class Collaborator(Document):
    """
        Document Class for Collaborators. 
        Collaborators are the users that will Create/Edit Case Studies.
        List of attributes:
            - documentsID: list<String>  of document ids that the Collaborator created.
            - first_name: <String> Collaborator's first name.
            - last_name: <String> Collaborator's last name.
            - email: <String> Collaborator's email. It must be a @upr.edu email.
                - email attribute follows this regex: '(.*)\.(.*)@upr\.edu'
            - banned: <Boolean> <Default=False> When set to true, the Collaborator looses access to Tellspace service.
            - approved: <Boolean> <Default=False>  When set to true, the Collaborator gains access to Tellspace service.     
    """
    documentsID = ListField(StringField(required=False))
    first_name = StringField(min_length=1, max_length=30, required=True)
    last_name = StringField(min_length=1, max_length=30, required=True)
    email = EmailField(required=True, max_length=50, unique=True, regex='(.*)\.(.*)@upr\.edu')
    banned = BooleanField(default=False, required=True)
    approved = BooleanField(default=False, required=True)


class Admin(Document):
    """
        Document Class for Admin. 
        Admin are the users that will have access to the Admin Dashboard.
        These attributes will be the credentials of the Admins for them to enter the Admin Dashboard.
        List of attributes:
            - username: <String>  Admin's username.
                - username attribute follows this regex: '(^(?=[a-zA-Z0-9])(?=.*[a-z])(?=.*[0-9])(?=.*[\.])(?=.*[A-Z])).*[^.]$' 
            - password: <String> Admin's  password.   
                - password attribute follows this regex: '([a-zA-Z0-9]+)*'
    """
    username = StringField(min_length=8, max_length=20, required=True, unique=True,
                           regex='(^(?=[a-zA-Z0-9])(?=.*[a-z])(?=.*[0-9])(?=.*[\.])(?=.*[A-Z])).*[^.]$')
    password = StringField(min_length=8, max_length=20, required=True, regex='([a-zA-Z0-9]+)*')


class Tag(Document):
    """
        Document Class for Tag. 
        Tag are the tags available for used as keywords for the DocumentCase.
        There will be some pre-defined by the Team, and the majority will be created by the
        Collaborators.
        List of attributes:
            - tagItem: <String>  Tag that can be used in a DocumentCase.   
    """
    tagItem = StringField(min_length=1, max_length=20, required=True, unique=True)


class Infrastructure(Document):
    """
        Document Class for Infrastructure. 
        These are going to be the categories available for the description of the
        infrastructure in the DocumentCase.
        All of them  will be pre-defined by the Team.
        List of attributes:
            - infrastructureType: <String>  category that can be used in a DocumentCase.   
    """
    infrastructureType = StringField(min_length=1, max_length=30, required=True, unique=True)


class Damage(Document):
    """
        Document Class for Damage. 
        These are going to be the categories available for the description of the
        Damage in the DocumentCase.
        All of them  will be pre-defined by the Team.
        List of attributes:
            - damageType: <String>  category that can be used in a DocumentCase.   
    """
    damageType = StringField(min_length=1, max_length=30, required=True, unique=True)


class Author(EmbeddedDocument):
    """
        EmbeddedDocument Class for Author. 
        These are going to be the authors of a DocumentCase, the ones who wrote it.
        An EmbeddedDocument is a Document Class that is defined inside another document.
        This one is going to be defined, and stored inside the DocumentCase Class. 
        The reason for this technique is that the Author Class has its own schema.
        List of attributes:
            - author_FN: <String>  Author's First Name. 
            - author_LN: <String>  Author's Last Name.
            - author_email: <String>  Author's Email.
            - author_faculty: <String>  Author's Faculty.  
    """
    author_FN = StringField(min_length=0, max_length=30, required=False)
    author_LN = StringField(min_length=0, max_length=30, required=False)
    author_email = EmailField(min_length=0, max_length=50, required=False, regex='(.*)\.(.*)@upr\.edu')
    author_faculty = StringField(min_length=0, max_length=30, required=False)


class Actor(EmbeddedDocument):
    """
        EmbeddedDocument Class for Actor. 
        These are going to be the Actor of a DocumentCase, the ones having a role in the DocumentCase.
        An EmbeddedDocument is a Document Class that is defined inside another document.
        This one is going to be defined, and stored inside the DocumentCase Class. 
        The reason for this technique is that the Actor Class has its own schema.
        List of attributes:
            - actor_FN: <String>  Actor's First Name. 
            - actor_LN: <String>  Actor's Last Name.
            - role: <String>  Actor's role in the DocumentCase. 
    """
    actor_FN = StringField(min_length=0, max_length=30, required=False)
    actor_LN = StringField(min_length=0, max_length=30, required=False)
    role = StringField(min_length=0, max_length=30, required=False)


class Timeline(EmbeddedDocument):
    """
        EmbeddedDocument Class for Timeline. 
        These will consist of the Timeline of a DocumentCase, describing the events followed.
        An EmbeddedDocument is a Document Class that is defined inside another document.
        This one is going to be defined, and stored inside the DocumentCase Class. 
        The reason for this technique is that the Timeline Class has its own schema.
        List of attributes:
            - event: <String>  Event happend within the DocumentCase. 
            - eventStartDate: <String>  Date when the event started, it has to have the following format: 'YYYY-MM-DD'.
                 - eventStartDate attribute follows this regex: '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
            - eventEndDate: <String>  Date when the event ended, it has to have the following format: 'YYYY-MM-DD'.
                - eventEndDate attribute follows this regex: '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
    """
    event = StringField(min_length=0, max_length=250, required=False)
    eventStartDate = StringField(min_length=0, required=False, regex='[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')
    eventEndDate = StringField(min_length=0, required=False, regex='[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')


class Section(EmbeddedDocument):
    """
        EmbeddedDocument Class for Section. 
        These are going to be the body of the Document Case.
        An EmbeddedDocument is a Document Class that is defined inside another document.
        This one is going to be defined, and stored inside the DocumentCase Class. 
        The reason for this technique is that the Section Class has its own schema.
        List of attributes:
            - secTitle: <String>  Section's title. 
            - content: <String>  Section's body.  
    """
    secTitle = StringField(min_length=0, max_length=250, required=False)
    content = StringField(required=False)


class Location(EmbeddedDocument):
    """
        EmbeddedDocument Class for Location. 
        These are going to be the body of the Document Case.
        An EmbeddedDocument is a Document Class that is defined inside another document.
        This one is going to be defined, and stored inside the DocumentCase Class. 
        The reason for this technique is that the Location Class has its own schema.
        List of attributes:
            - address: <String>  Location's address. 
            - latitude: <Number>  Location's latitude.
            - longitude: <Number> Location's Longitude.  
    """
    address = StringField(min_length=0, required=True)
    latitude = DecimalField(min_value=17.86, max_value=18.54, required=True)
    longitude = DecimalField(min_value=-67.29, max_value=-65.22, required=True)

class DocumentCase(Document):
    """
        Document Class for DocumentCase. 
        DocumentCase will consist of a Case Study created by a Collaborator.
        List of attributes:
            - creatoriD: <String>  the Collaborator's id which created the Case study.
            - title: <String> The case study's title .
            - language: <String> The language which the case study is written.
            - location: List<String> of addresses where the case study took place.
            - description: <String> Case study's description.
            - published: <Boolean> <Default=False> When set to true, the case study will be visible in SearchSpace service.
            - incidentDate: <String>  Date when the incident happened, it has to have the following format: 'YYYY-MM-DD'.
                 - incidentDate attribute follows this regex: '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
            - creationDate: <String>  Date when the case study was created, it has to have the following format: 'YYYY-MM-DD'.
                - creationDate attribute follows this regex: '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]' 
            - lastModificationDate: <String>  Last date when the case study was modified, it has to have the following format: 'YYYY-MM-DD'.
                - lastModificationDate attribute follows this regex: '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'  
            - tagsDoc: List<String> of tags from the case study. 
            - infrasDocList: List<String> of infrastructure categories from the case study. 
            - damageDocList: List<String> of damage categories from the case study. 
            - author: List<Author> of author objects, the ones who wrote the case study.
            - section: List<Section> of section objects, this will consist the body of the case study.
            - timeline: List<Timeline> of timeline objects, this will consist of the events that happened within the case study.
                
    """
    creatoriD = ReferenceField('Collaborator')
    title = StringField(min_length=10, max_length=250, required=True, unique=True)
    language = StringField(min_length=0, required=False)
    location = ListField(StringField(min_length=0, required=False))
    description = StringField(min_length=0, max_length=500, required=False)
    published = BooleanField(default=True, required=True)
    incidentDate = StringField(min_length=1, required=True, regex='[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')
    creationDate = StringField(min_length=1, required=True, regex='[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')
    lastModificationDate = StringField(min_length=1, required=True, regex='[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')
    tagsDoc = ListField(StringField(min_length=0, max_length=30, required=False))
    infrasDocList = ListField(StringField(min_length=1, max_length=30, required=True))
    damageDocList = ListField(StringField(min_length=1, max_length=30, required=True))
    author = ListField(EmbeddedDocumentField(Author))
    actor = ListField(EmbeddedDocumentField(Actor))
    section = ListField(EmbeddedDocumentField(Section))
    timeline = ListField(EmbeddedDocumentField(Timeline))


class CreationEmbedded(EmbeddedDocument):
    creatoriD = ReferenceField('Collaborator')
    title = StringField(min_length=10, max_length=250, required=False, unique=True, default=None)
    language = StringField(min_length=0, required=False)
    location = ListField(StringField(min_length=0, required=False))
    description = StringField(min_length=0, max_length=500, required=False)
    published = BooleanField(default=True, required=False)
    incidentDate = StringField(min_length=1, required=False, regex='[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')
    creationDate = StringField(min_length=1, required=False, regex='[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')
    lastModificationDate = StringField(min_length=1, required=False, regex='[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')
    tagsDoc = ListField(StringField(min_length=0, max_length=30, required=False))
    infrasDocList = ListField(StringField(min_length=1, max_length=30, required=False))
    damageDocList = ListField(StringField(min_length=1, max_length=30, required=False))
    author = ListField(EmbeddedDocumentField(Author))
    actor = ListField(EmbeddedDocumentField(Actor))
    section = ListField(EmbeddedDocumentField(Section))
    timeline = ListField(EmbeddedDocumentField(Timeline))

    def _author_to_json(self):
        auth = []
        for author in self.author:
            auth.append(json.loads(author.to_json()))
        return auth
    
    def _actor_to_json(self):
        actor = []
        for act in self.actor:
            actor.append(json.loads(act.to_json()))
        return actor

    def _timeline_to_json(self):
        timeline = []
        for timeL in self.timeline:
            timeline.append({
                'event': timeL.event,
                'eventStartDate': timeL.eventStartDate,
                'eventEndDate': timeL.eventEndDate
            })
        return timeline

    def _location_to_json(self):
        locations = []
        for location in self.location:
            locations.append(location.address)
        return locations
    
    def _section_to_json(self):
        sections = []
        for section in self.section:
            sections.append(
                {
                    'secTitle': section.secTitle,
                    'content': section.content
                }
            )
        return sections
    
    def to_json(self):
        if(self.title is None):
            return {}
        else:
           return {
                'creatoriD': str(self.creatoriD.id),
                'title': self.title,
                'language': self.language,
                'location': self._location_to_json(),
                'description': self.description,
                'published': self.published,
                'incidentDate': self.incidentDate,
                'creationDate': self.creationDate,
                'lastModificationDate': self.lastModificationDate,
                'tagsDoc': self.tagsDoc,
                'infrasDocList': self.infrasDocList,
                'damageDocList': self.damageDocList,
                'author': self._author_to_json(),
                'actor': self._actor_to_json(),
                'section': self._section_to_json(),
                'timeline': self._timeline_to_json()
            }

class TitleEmbedded(EmbeddedDocument):
    title = StringField(min_length=10, max_length = 100, required=True, unique=True)

    def to_json(self):
        return self.title

class DescriptionEmbedded(EmbeddedDocument):
    description = StringField(min_length=0, max_length=500, required=False)
    
    def to_json(self):
        return self.description

class InfrastructureEmbedded(EmbeddedDocument):
    infrasDocList =  ListField(StringField(min_length=1,max_length=50,required=True))

    def to_json(self):
        return self.infrasDocList

class TimelineEmbedded(EmbeddedDocument):
    timeline = ListField(EmbeddedDocumentField(Timeline))

    def to_json(self):
        timeline = []
        for timeL in self.timeline:
            timeline.append({
                'event': timeL.event,
                'eventStartDate': timeL.eventStartDate,
                'eventEndDate': timeL.eventEndDate
            })
        return timeline

class SectionEmbedded(EmbeddedDocument):
    section = EmbeddedDocumentField(Section)

    def to_json(self):
        if(self.section == None):
            return {}
        return {
                'secTitle': self.section.secTitle,
                'content': self.section.content
            }

class DamageEmbedded(EmbeddedDocument):
    damageDocList =  ListField(StringField(min_length=1,max_length=50,required=True))

    def to_json(self):
        return self.damageDocList

class ActorEmbedded(EmbeddedDocument):
    actor = ListField(EmbeddedDocumentField(Actor))

    def to_json(self):
        actors = []
        for actor in self.actor:
            actors.append(
                {'actor_FN': actor.actor_FN,
                'actor_LN': actor.actor_LN,
                'role': actor.role})
        return actors

class AuthorEmbedded(EmbeddedDocument):
    author = ListField(EmbeddedDocumentField(Author))

    def to_json(self):
        authors = []
        for author in self.author:
            authors.append(
                {'author_FN': author.author_FN,
                'author_LN': author.author_LN,
                'author_email': author.author_email,
                'author_faculty': author.author_faculty})
        return authors

class IncidentEmbedded(EmbeddedDocument):
    incidentDate = StringField(min_length=1, required=True, regex='[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')

    def to_json(self):
        return self.incidentDate

class TagEmbedded(EmbeddedDocument):
    tagsDoc = ListField(StringField(min_length=1,max_length=50,required=False))

    def to_json(self):
        return self.tagsDoc

class LocationEmbedded(EmbeddedDocument):
    location = ListField(EmbeddedDocumentField(Location), max_length=5, required=False)
    
    def to_json(self):
        locations = []
        for location in self.location:
            locations.append(location.address)
        return locations

class FieldsEmbedded(EmbeddedDocument):
    new = GenericEmbeddedDocumentField(required=True)
    old = GenericEmbeddedDocumentField(required=True)

class DocumentCaseRevision(Document):
    creatorId = ReferenceField('Collaborator')
    docId = ReferenceField('DocumentCase')
    creator_name = StringField(min_length=1, required=True)
    creator_email = StringField(min_length=1, required=True)
    document_title = StringField(min_length=1, required=True)
    revision_date = StringField(min_length=1, required=True, regex='[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')
    revision_number = StringField(required=True)
    revision_type = StringField(required=True)
    field_changed = EmbeddedDocumentField(FieldsEmbedded, required=True)