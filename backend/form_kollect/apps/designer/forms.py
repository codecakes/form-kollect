from designer import constants
from django import forms


class CreateForm(forms.Form):
    choice_field = constants.CHOICE_FIELDS
    field_name = forms.CharField(
        max_length=120,
        min_length=2,
        widget=forms.TextInput,
        required=True,
        label="Field Name",
    )
    field_type = forms.ChoiceField(
        choices=choice_field, widget=forms.Select, required=True, label="Field Type"
    )


class AddMoreFormRequest(forms.Form):
    num_forms = forms.IntegerField(
        min_value=2, widget=forms.widgets.NumberInput, label="Want More Forms?"
    )
