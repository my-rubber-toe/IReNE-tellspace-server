

from marshmallow import Schema, fields, validate
from datetime import datetime


"""Nested Schemas"""


class Authors(Schema):
    """Nested Schema"""
    first_name = fields.String(required=True, validate=validate.Length(min=1))
    last_name = fields.String(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)


class Actors(Schema):
    """Nested Schema"""
    first_name = fields.String(required=True, validate=validate.Length(min=1))
    last_name = fields.String(required=True, validate=validate.Length(min=1))
    role = fields.String(
        required=True,
        allow_none=False,
        validate=validate.Length(min=1)
    )


class TimeLineEvent(Schema):
    """Nested Schema"""
    event_date = fields.Date(required=True)
    event_description = fields.String(required=True, validate=validate.Length(min=1))


"""Request Body Schemas"""


class GetDocumentsValidator(Schema):
    """ Request body schema for the endpoint /api/documents"""
    general = fields.String(required=False)

    publication_date = fields.List(
        fields.Date(),
        required=False,
        allow_none=False,
        validate=validate.Length(min=2)
    )

    tags = fields.List(
        fields.String(),
        required=False,
        validate=validate.Length(min=1)
    )


class CreateDocumentValidator(Schema):
    """ Request body schema for the endpoint /api/documents/create"""
    title = fields.String(required=True)

    description = fields.String(required=False)

    authors = fields.List(
        fields.Nested(Authors),
        required=True,
        validate=validate.Length(min=1)
    )

    actors = fields.List(
        fields.Nested(Actors),
        required=True,
        validate=validate.Length(min=1)
    )

    infrastructure_type = fields.List(
        fields.String(),
        required=True,
        validate=validate.Length(min=1)
    )

    damage_type = fields.List(
        fields.String(),
        required=True,
        validate=validate.Length(min=1)
    )

    incident_date = fields.Date(required=True)

    language = fields.String(
        default='English'
    )


class UpdateDocumentTitleValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/title"""
    title = fields.String(required=True, validate=validate.Length(min=1))


class UpdateDocumentDescriptionValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/description"""
    description = fields.String(required=True, validate=validate.Length(min=1))


class UpdateDocumentTimelineValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/timeline"""
    timeline = fields.List( fields.Nested(TimeLineEvent), required=True, validate=validate.Length(min=1)
    )


class UpdateDocumentSectionValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/section"""
    section_nbr = fields.Integer(required=True)
    section_title = fields.String(required=False, validate=validate.Length(min=1))
    section_text = fields.String(required=False, validate=validate.Length(min=1))


class UpdateDocumentInfrastructureTypesValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/infrastructure_types"""
    infrastructure_types = fields.List(
        fields.String(required=True, validate=validate.Length(min=1)),
        required=True,
        validate=validate.Length(min=1)
    )


if __name__ == '__main__':
    data = {
        'general': 'testingdata',
        'publication_date': [datetime.now(), datetime.now()],
        'tags': ['tag1', 'tag2']
    }

    v = GetDocumentsValidator().dumps(data)

    print(v)









