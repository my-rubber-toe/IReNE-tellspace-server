"""
Validators: validators.py
=========================
Holds the classes that perform the request body validation process. These classes throw message errors according to the
missing values or type errors.
"""

from marshmallow import Schema, fields, validate


class Authors(Schema):
    """Authors Validator."""
    first_name = fields.String(required=True, validate=[
        validate.Length(min=1, max=30),
        validate.Regexp('^[A-ZÁÉÍÓÚÑÜ][a-z A-Z \- À-ÿ]*[a-záéíóúñü]$') ])
    last_name = fields.String(required=True, validate=[
        validate.Length(min=1, max=30),
        validate.Regexp('^[A-ZÁÉÍÓÚÑÜ][a-z A-Z \- À-ÿ]*[a-záéíóúñü]$')])
    email = fields.Email(required=True, validate=[
        validate.Length(min=9, max=70),
        validate.Regexp('^[A-ZÁÉÍÓÚÑÜ][a-z A-Z \- À-ÿ]*[a-záéíóúñü]$')])
    faculty = fields.String(required=True, validate=validate.Length(min=1, max=30))


class Actors(Schema):
    """Actors Validator."""
    first_name = fields.String(required=True, validate=[
        validate.Length(min=1, max=30),
        validate.Regexp('^[A-ZÁÉÍÓÚÑÜ][a-z A-Z \- À-ÿ]*[a-záéíóúñü]$')])
    last_name = fields.String(required=False, validate=[
        validate.Length(min=1, max=30),
        validate.Regexp('^[A-ZÁÉÍÓÚÑÜ][a-z A-Z \- À-ÿ]*[a-záéíóúñü]$')])
    role = fields.String(required=True, validate=validate.Length(min=1, max=30))


class TimeLineEvent(Schema):
    """Timeline Validator."""
    event = fields.String(required=True, validate=validate.Length(min=10, max=100))
    event_start_date = fields.Date('%Y-%m-%d', required=True)
    event_end_date = fields.Date('%Y-%m-%d', required=True)


class CreateDocumentValidator(Schema):
    """ Request body schema for the endpoint /api/documents/create"""
    title = fields.String(required=True, validate=[
            validate.Length(min=10, max=100),
            validate.Regexp("^([A-ZÁÉÓÍÚÑÜ]+)([A-Z a-z 0-9 À-ÿ : \-]*)([A-Za-z0-9À-ÿ]$)")
        ])

    language = fields.String(min_length=1, required=True, validate=[
            validate.Length(min=1, max=20),
            validate.Regexp("^[A-Z][a-z]{1,20}$")
    ])

    authors = fields.List(
        fields.Nested(Authors),
        required=False,
        validate=validate.Length(min=1, max=10)
    )

    actors = fields.List(
        fields.Nested(Actors),
        required=False,
        validate=validate.Length(min=1,max=5)
    )

    infrastructure_type = fields.List(
        fields.String(required=True, validate=[
        validate.Length(min=1, max=50),
        validate.Regexp("^([A-ZÁÉÓÍÚÑÜ]+)([A-Z a-z 0-9 À-ÿ : \-]*)([A-Za-z0-9À-ÿ]$)")]),
        required=True,
        validate=validate.Length(min=1)
    )

    damage_type = fields.List(
        fields.String(required=True, validate=[
        validate.Length(min=1, max=50),
        validate.Regexp("^([A-ZÁÉÓÍÚÑÜ]+)([A-Z a-z 0-9 À-ÿ : \-]*)([A-Za-z0-9À-ÿ]$)")]),
        required=True,
        validate=validate.Length(min=1)
    )

    incident_date = fields.Date('%Y-%m-%d', required=True)


class RemoveDocumentValidator(Schema):
    doc_id = fields.String(required=True, validate=validate.Length(min=1))


class TitleValidator(Schema):
    """ Request body validation class for the endpoint /api/documents/<doc_id>/edit/title"""
    title = fields.String(
        required=True,
        validate=[
            validate.Length(min=10, max=100),
            validate.Regexp("^([A-ZÁÉÓÍÚÑÜ]+)([A-Z a-z 0-9 À-ÿ : \-]*)([A-Za-z0-9À-ÿ]$)")
        ]
    )


class DescriptionValidator(Schema):
    """ Request body validation class for the endpoint /api/documents/<doc_id>/edit/description"""
    description = fields.String(required=True, validate=validate.Length(min=0, max=500))


class TimelineValidator(Schema):
    """ Request body validation class for the endpoint /api/documents/<doc_id>/edit/timeline"""
    timeline = fields.List(fields.Nested(TimeLineEvent), required=True)


class EditSectionValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/section"""
    section_title = fields.String(required=True, validate=[
        validate.Length(min=1, max=100),
        validate.Regexp("^([A-ZÁÉÓÍÚÑÜ]+)([A-Z a-z 0-9 À-ÿ : \-]*)([A-Za-z0-9À-ÿ]$)")])
    section_text = fields.String(required=True)


class InfrastructureTypesValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/infrastructure_types"""
    infrastructure_types = fields.List(
        fields.String(required=True, validate=[
        validate.Length(min=1, max=50),
        validate.Regexp("^[A-ZÁÉÍÓÚÑÜ][a-z A-Z À-ÿ / & , \- ]*$")]),
        required=True, 
        validate=validate.Length(min=1))


class DamageTypesValidator(Schema):
    """ Request body validation class for the endpoint /api/documents/<doc_id>/edit/damage_types"""
    damage_types = fields.List(
        fields.String(required=True, validate=[
            validate.Length(min=1, max=50),
            validate.Regexp("^[A-ZÁÉÍÓÚÑÜ][a-z A-Z À-ÿ / & , \- ]*$")]),
        required=True,
        validate=validate.Length(min=1)
    )


class ActorsValidator(Schema):
    """ Request body validation class for the endpoint /api/documents/<doc_id>/edit/actors"""
    actors = fields.List(
        fields.Nested(Actors),
        required=True,
        validate=validate.Length(min=1,max=5)
    )


class LocationsValidator(Schema):
    """ Request body validation class for the endpoint /api/documents/<doc_id>/edit/locations"""
    locations = fields.List(
        fields.String(required=True, validate=validate.Length(min=1)),
        required=True,
        validate=validate.Length(max=5)
    )


class IncidentDateValidator(Schema):
    """ Request body validation class for the endpoint /api/documents/<doc_id>/edit/incident_date"""
    incident_date = fields.Date('%Y-%m-%d', required=True)


class AuthorsValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/authors"""
    authors = fields.List(
        fields.Nested(Authors),
        required=True,
        validate=validate.Length(min=1,max=10)
    )


class TagsValidator(Schema):
    """ Request body schema for the endpoint /api/documents/<doc_id>/edit/tags"""
    tags = fields.List(fields.String(required=True, validate=[
        validate.Length(min=1, max=50),
        validate.Regexp("^[A-ZÁÉÍÓÚÑÜ][a-z A-Z À-ÿ / & , \- ]*$")]),
        required=True,
        validate=validate.Length(max=10))
