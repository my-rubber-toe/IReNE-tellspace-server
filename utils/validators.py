

from marshmallow import Schema, fields, validate

"""Nested Schemas"""


class Authors(Schema):
    """Nested Schema"""
    first_name = fields.String(required=True, validate=validate.Length(min=1))
    last_name = fields.String(required=True, validate=validate.Length(min=1))
    email = fields.Email(
        required=True,
        validate=validate.Regexp("^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$")
    )
    faculty = fields.String(required=True, validate=validate.Length(min=1))


class Actors(Schema):
    """Nested Schema"""
    first_name = fields.String(required=True, validate=validate.Length(min=1))
    last_name = fields.String(required=True, validate=validate.Length(min=1))
    role = fields.String(required=True, validate=validate.Length(min=1))


class TimeLineEvent(Schema):
    """Nested Schema"""
    event_date = fields.String(required=True, format="%Y-%m-%d")
    event_description = fields.String(required=True, validate=validate.Length(min=1))


"""Request Body Schemas"""


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

    incident_date = fields.String(required=True, format="%Y-%m-%d")

class RemoveDocumentValidator(Schema):
    doc_id=fields.String(required=True, validate=validate.Length(min=1))


class TitleValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/title"""
    title = fields.String(required=True, validate=validate.Length(min=1))


class DescriptionValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/description"""
    description = fields.String(required=True, validate=validate.Length(min=1))


class TimelineValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/timeline"""
    timeline = fields.List( fields.Nested(TimeLineEvent), required=True, validate=validate.Length(min=1))


class RemoveSectionValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/section"""
    section_nbr = fields.Integer(required=True)


class EditSectionValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/section"""
    section_nbr = fields.Integer(required=True)
    section_title = fields.String(required=False, validate=validate.Length(min=1))
    section_text = fields.String(required=False, validate=validate.Length(min=1))


class InfrastructureTypesValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/infrastructure_types"""
    infrastructure_types = fields.List(
        fields.String(required=True, validate=validate.Length(min=1)),
        required=True,
        validate=validate.Length(min=1)
    )


class DamageTypesValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/damage_types"""
    damage_types = fields.List(
        fields.String(required=True, validate=validate.Length(min=1)),
        required=True,
        validate=validate.Length(min=1)
    )


class ActorsValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/actors"""
    actors = fields.List(
        fields.Nested(Actors),
        required=True,
        validate=validate.Length(min=1)
    )


class LocationsValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/locations"""
    locations = fields.List(
        fields.String(required=True, validate=validate.Length(min=1, max=50)),
        required=True,
        validate=validate.Length(min=1)
    )


class AuthorsValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/authors"""
    authors = fields.List(
        fields.Nested(Authors),
        required=True,
        validate=validate.Length(min=1)
    )


class TagsValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/tags"""
    tags = fields.List(
        fields.String(required=True, validate=[validate.Length(min=1)]),
        required=True,
        validate=validate.Length(min=1)
    )
