import json
from django import forms
from django.core.validators import validate_email, URLValidator

class MultiEmailField(forms.Field):
    def to_python(self, value):
        if not value:
            return []
        return json.loads(value)

    def validate(self, value):
        super().validate(value)
        for email in value:
            validate_email(email)

class MultiPkField(forms.Field):
    def to_python(self, value):
        if not value:
            return []
        return json.loads(value)

    def validate(self, value):
        super().validate(value)



class NewProjectForm(forms.Form):
    title  = forms.CharField(max_length=255)
    pad    = MultiPkField(required=False)
    people = MultiEmailField(required=False)

    def cleaned_pad(self):
        return json.loads(self.cleaned_data['pad'])

    def cleaned_people(self):
        return json.loads(self.cleaned_data['people'])
