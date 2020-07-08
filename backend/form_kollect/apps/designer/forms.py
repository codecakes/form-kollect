from typing import Union

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


class CommonOpsBaseSet(forms.BaseFormSet):
    def __init__(self, *args, **kwargs):
        if "form_kwargs" in kwargs:
            for key in kwargs["form_kwargs"]:
                setattr(self, key, kwargs["form_kwargs"][key])
            kwargs["form_kwargs"].clear()
        super().__init__(*args, **kwargs)


class CreateFormBaseSet(CommonOpsBaseSet):
    """Custom Formset to pass extra parameters."""

    def __init__(self, *args, **kwargs):
        print("In CreateFormBaseSet")
        print(args)
        print(kwargs)
        super().__init__(*args, **kwargs)


class AddMoreFormRequest(forms.Form):
    num_forms = forms.IntegerField(
        min_value=2, widget=forms.widgets.NumberInput, label="Want More Forms?"
    )


class CreateFormOpts(forms.Form):
    field_opts_value = forms.CharField(
        max_length=120, min_length=2, widget=forms.TextInput, required=False,
    )


class CreateFormOptsBaseSet(forms.BaseFormSet):
    """Custom Formset to pass extra parameters."""

    # TODO(codecakes): add slots

    def __init__(self, *args, **kwargs):
        if "form_kwargs" in kwargs:
            for key in kwargs["form_kwargs"]:
                setattr(self, key, kwargs["form_kwargs"][key])
            kwargs["form_kwargs"].clear()
        super().__init__(*args, **kwargs)
        self.__set_bulk_field_attrs()

    def __set_bulk_field_attrs(self):
        """Generic html attributes bulk key value update for each form."""
        if not (hasattr(self, "field_name") and hasattr(self, "field_type")):
            return
        for form in self:
            label = f"Options Value for {self.field_name}"
            form.fields["field_opts_value"].widget.attrs.update(
                {"name": label, "placeholder": f"Field type: {self.field_type}",}
            )
            form.fields["field_opts_value"].label = label
