from designer import constants
from django import forms


class CreateForm(forms.Form):
    field_name = forms.CharField(
        max_length=120,
        min_length=2,
        widget=forms.TextInput,
        required=True,
        label="Field Name",
    )
    field_type = forms.ChoiceField(
        choices=constants.CHOICE_FIELDS,
        widget=forms.Select,
        required=True,
        label="Field Type",
    )
    num_values = forms.IntegerField(
        initial=1,
        required=False,
        label="Number of Field Values",
        widget=forms.widgets.HiddenInput,
    )

    def is_selectable(self):
        """Returns True if field_type is a selectable type."""
        return self.cleaned_data["field_type"] in constants.FIELD_OPTS


class AddMoreFormRequest(forms.Form):
    num_forms = forms.IntegerField(
        min_value=2, widget=forms.widgets.NumberInput, label="Want More Forms?"
    )

class CreateFormOpts(forms.Form):
    field_opts_value = forms.CharField(
        max_length=120,
        min_length=2,
        widget=forms.TextInput,
        required=False,
        label="Field Options Value",
    )


class CreateFormOptsBaseSet(forms.BaseFormSet):
    """Custom Formset to pass extra parameters."""

    def __init__(self, *args, **kwargs):
        self.field_name = kwargs['form_kwargs'].pop('field_name')
        self.field_type = kwargs['form_kwargs'].pop('field_type')
        super().__init__(*args, **kwargs)
