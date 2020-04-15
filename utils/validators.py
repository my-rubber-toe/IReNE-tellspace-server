"""
responses.py
====================================
Classes that perfom the request body validation process. These classes throw messages according to the missing values or
validation errors
"""

from marshmallow import Schema, fields, validate
import re

"""Nested Schemas"""


class Authors(Schema):
    """Authors Validator."""
    first_name = fields.String(required=True, validate=validate.Length(min=1, max=30))
    last_name = fields.String(required=True, validate=validate.Length(min=1, max=30))
    email = fields.Email(
        required=True,
        # validate=validate.Regexp('(.*)\.(.*)@upr\.edu')
    )
    faculty = fields.String(required=True, validate=validate.Length(min=1, max=30))


class Actors(Schema):
    """Actors Validator."""
    first_name = fields.String(required=True, validate=validate.Length(min=1, max=30))
    last_name = fields.String(required=False, validate=validate.Length(min=1, max=30))
    role = fields.String(required=True, validate=validate.Length(min=1, max=30))


class TimeLineEvent(Schema):
    """Timeline Validator."""
    event = fields.String(required=True, validate=validate.Length(min=10, max=250))
    event_start_date = fields.Date('%Y-%m-%d', required=True)
    event_end_date = fields.Date('%Y-%m-%d', required=True)


"""Request Body Schemas"""


class CreateDocumentValidator(Schema):
    """ Request body schema for the endpoint /api/documents/create"""
    title = fields.String(required=True, validate=validate.Length(min=10, max=250))

    description = fields.String(required=False, validate=validate.Length(min=10, max=500))

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
        fields.String(required=True, validate=validate.Length(min=1)),
        required=True,
        validate=validate.Length(min=1)
    )

    damage_type = fields.List(
        fields.String(required=True, validate=validate.Length(min=1, max=30)),
        required=True,
        validate=validate.Length(min=1)
    )

    incident_date = fields.Date('%Y-%m-%d', required=True)
    language = fields.Str(required=True, validate=validate.Length(min=1))


class RemoveDocumentValidator(Schema):
    doc_id = fields.String(required=True, validate=validate.Length(min=1))


class TitleValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/title"""
    title = fields.String(
        required=True,
        validate=[
            validate.Length(min=10, max=250),
            validate.Regexp(r"^[A-Za-z0-9 :]*[A-Za-z0-9:][A-Za-z0-9 :]*$")
        ]
    )


class DescriptionValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/description"""
    description = fields.String(required=True, validate=validate.Length(min=10, max=500))


class TimelineValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/timeline"""
    timeline = fields.List(fields.Nested(TimeLineEvent), required=True, validate=validate.Length(min=1))


class EditSectionValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/section"""
    section_title = fields.String(required=True, validate=validate.Length(min=1, max=250))
    section_text = fields.String(required=True)


class InfrastructureTypesValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/infrastructure_types"""
    infrastructure_types = fields.List(
        fields.String(required=True, validate=validate.Length(min=1, max=30)),
        required=True,
        validate=validate.Length(min=1)
    )


class DamageTypesValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/damage_types"""
    damage_types = fields.List(
        fields.String(required=True, validate=validate.Length(min=1, max=30)),
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
        fields.String(required=True, validate=validate.Length(min=1)),
        required=True,
        validate=validate.Length(min=1)
    )


class IncidentDateValidator(Schema):
    incident_date = fields.Date('%Y-%m-%d', required=True)


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
        fields.String(
            required=True, validate=validate.Length(min=1, max=20)
        ),
        required=True,
        validate=validate.Length(min=1)
    )
