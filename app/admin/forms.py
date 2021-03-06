from flask_wtf import Form
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import PasswordField, StringField, SubmitField, TextAreaField, FormField, SelectField, IntegerField, BooleanField, SelectMultipleField, HiddenField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import Email, EqualTo, InputRequired, Length

from .. import db
from ..models import Role, User, Candidate, Race, Class, Gender, SexualOrientation, Term, Status


class ChangeUserEmailForm(Form):
    email = EmailField(
        'New email', validators=[InputRequired(), Length(1, 64), Email()])
    submit = SubmitField('Update email')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class ChangeAccountTypeForm(Form):
    role = QuerySelectField(
        'New account type',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Role).order_by('permissions'))
    submit = SubmitField('Update role')


class InviteUserForm(Form):
    role = QuerySelectField(
        'Account type',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Role).order_by('permissions'))
    first_name = StringField(
        'First name', validators=[InputRequired(), Length(1, 64)])
    last_name = StringField(
        'Last name', validators=[InputRequired(), Length(1, 64)])
    email = EmailField(
        'Email', validators=[InputRequired(), Length(1, 64), Email()])
    submit = SubmitField('Invite')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

class InviteAcceptedCandidatesForm(Form):
    selected_candidates = HiddenField()
    submit = SubmitField('Invite Selected')


class NewUserForm(InviteUserForm):
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(), EqualTo('password2', 'Passwords must match.')
        ])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])

    submit = SubmitField('Create')


class NewTermForm(Form):
    name = StringField(
        'Name', validators=[InputRequired()])
    start_date = DateField(
        'Start Date', validators=[InputRequired()])
    end_date = DateField(
        'End Date', validators=[InputRequired()])
    submit = SubmitField('Create')
# TODO check if end date is larger than start date

class EditTermForm(Form):
    name = StringField(
        'Name', validators=[InputRequired()])
    start_date = DateField(
        'Start Date', validators=[InputRequired()])
    end_date = DateField(
        'End Date', validators=[InputRequired()])
    submit = SubmitField('Update')

class DemographicForm(Form):
    race = SelectField(
        'Race',
        choices=[(choice.name, choice.name.replace('_', ' ').title()) for choice in Race]
    )

    soc_class = SelectField(
        'Class',
        choices=[(choice.name, choice.name.replace('_', ' ').title()) for choice in Class]
    )
    gender = SelectField(
        'Gender',
        choices=[(choice.name, choice.name.replace('_', ' ').title()) for choice in Gender]
    )
    sexual_orientation = SelectField(
        'Sexual Orientation',
        choices=[(choice.name, choice.name.replace('_', ' ').title()
                  if choice.name != 'LGBTQ' else 'LGBTQ') for choice in SexualOrientation]
    )
    age = IntegerField('Age', default=0)


class EditStatusForm(Form):
    participant = HiddenField(label='')
    status = SelectField(
        label='',
        choices=[(choice.name, choice.name.replace('_', ' ').title()) for choice in Status]
    )
    term = QuerySelectField(
        label='',
        get_label='name',
        allow_blank=True,
        query_factory=lambda: db.session.query(Term).order_by('start_date'))
    submit_status = SubmitField('Update Status')

class StatsSelectTermForm(Form):
    term = QuerySelectField(
        label='',
        get_label='name',
        query_factory=lambda:  db.session.query(Term).order_by(Term.start_date.desc()))
    submit_term = SubmitField('Update')

class NewCandidateForm(Form):
    first_name = StringField(
        'First name', validators=[InputRequired(), Length(1, 64)])
    last_name = StringField(
        'Last name', validators=[InputRequired(), Length(1, 64)])
    email = EmailField(
        'Email', validators=[InputRequired(), Length(1, 64), Email()])
    phone_number = StringField(
        'Phone Number')
    term = QuerySelectField(
        'Term',
        get_label='name',
        allow_blank=True,
        query_factory=lambda: db.session.query(Term).order_by('start_date'))
    source = StringField(
        'Source')
    staff_contact = StringField(
        'Staff Contact')
    notes = TextAreaField(
        'Notes')
    demographic = FormField(DemographicForm)
    submit = SubmitField('Create')


class EditParticipantForm(Form):
    first_name = StringField(
        'First name', validators=[InputRequired(), Length(1, 64)])
    last_name = StringField(
        'Last name', validators=[InputRequired(), Length(1, 64)])
    email = EmailField(
        'Email', validators=[InputRequired(), Length(1, 64), Email()])
    phone_number = StringField(
        'Phone Number', default="")
    source = StringField(
        'Source', validators=[Length(1, 256)])
    staff_contact = StringField(
        'Staff Contact', validators=[Length(1, 64)])
    notes = TextAreaField(
        'Notes', validators=[Length(0, 1024)])
    status = IntegerField(
        'Status', validators=[InputRequired()])
    assigned_term = QuerySelectField(
        'Assigned Term',
        get_label='name',
        query_factory=lambda: db.session.query(Term).order_by('start_date'))
    amount_donated = IntegerField(
        'Amount Donated', validators=[])
    applied = BooleanField(
        'Applied', default=False)
    demographic = FormField(DemographicForm)
    submit = SubmitField('Save')
