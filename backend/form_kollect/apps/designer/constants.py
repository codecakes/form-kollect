from collections import namedtuple

from django import forms
from phonenumber_field.modelfields import PhoneNumberField


FIELD_TUPLE = namedtuple("field_name", ["input_field", "field_callable", "widget"])

# HTML Form Input Types
FIELD_TYPE = dict(
    # Defines a one-line text input field
    TXT=FIELD_TUPLE("text", forms.CharField, forms.TextInput),
    # Defines a one-line password input field
    PWD=FIELD_TUPLE("password", forms.CharField, forms.PasswordInput),
    # Defines a radio button which allows select one option.
    RADIO=FIELD_TUPLE("radio", forms.ChoiceField, forms.widgets.RadioSelect),
    # Defines checkboxes which allow select multiple options form.
    CHECKBOX=FIELD_TUPLE("checkbox", forms.ChoiceField, forms.CheckboxSelectMultiple),
    # Defines to select the file from device storage.
    FILE=FIELD_TUPLE("file", forms.FileField, None),
    IMG=FIELD_TUPLE("image", forms.ImageField, None),
    # Defines an input field for selection of date.
    DATE=FIELD_TUPLE("date", forms.DateField, None),
    # Defines an input field for entering an email address.
    EMAIL=FIELD_TUPLE("email", forms.EmailField, None),
    # Defines an input field to enter a number.
    NUMBER=FIELD_TUPLE("number", forms.IntegerField, forms.NumberInput),
    # Defines a field for entering URL
    URL=FIELD_TUPLE("url", forms.URLField, None),
    TEL=FIELD_TUPLE("tel", PhoneNumberField, None),
)

CHOICE_FIELDS = [
    (field_key, val_tuple.input_field) for field_key, val_tuple in FIELD_TYPE.items()
]

FIELD_OPTS = dict(
    filter(
        lambda field_kv: field_kv[1].field_callable == forms.ChoiceField,
        FIELD_TYPE.items(),
    )
)
