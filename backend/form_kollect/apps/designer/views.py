from typing import List

from django import forms
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import reverse
from django.views.generic import ListView

from . import forms as designer_forms

FORM_LIST_TEMPLATE = "designer/index.html"
FORM_CREATE_TEMPLATE = "designer/create.html"
FORM_BULK_TEMPLATE = "designer/bulk.html"
FORM_SHOW_BULK_TEMPLATE = "designer/show-bulk.html"
FORM_ADD_OPTS_TEMPLATE = "designer/add-form-options.html"
FORM_VIEW_TEMPLATE = "designer/view-form.html"


class FormList(ListView):
    template_name = FORM_LIST_TEMPLATE


def create(request):
    """Creates (Bulk)Form Request. Start Page"""
    context: dict = {}
    msg: str = ""
    error: str = ""
    more_forms = designer_forms.AddMoreFormRequest()
    if request.method == "POST":
        form = designer_forms.CreateForm(request.POST)
        if form.is_valid():
            msg = "thanks"
        else:
            error = "Form is invalid"
        context.update(dict(msg=msg, error=error, form=form, more_forms=more_forms))
    else:
        context.update(dict(form=designer_forms.CreateForm(), more_forms=more_forms))
    return render(request, FORM_CREATE_TEMPLATE, context=context)


def create_bulk_forms(request):
    """Create bulk forms based on Number of Fields in previous Input."""
    error: str = ""
    num_forms: int = 2
    context: dict = {}
    more_forms = designer_forms.AddMoreFormRequest(request.GET)
    # Check for num_forms in request param
    if more_forms.is_valid():
        # Create form set from request parameter if provided
        num_forms = more_forms.cleaned_data.get("num_forms", num_forms)
        FormSet = forms.formset_factory(designer_forms.CreateForm, extra=num_forms)
        formset = FormSet()
    else:
        error = "Invalid Incoming Form."
        print(error)
        FormSet = forms.formset_factory(designer_forms.CreateForm)
        formset = FormSet(request.POST)
    if not formset.is_valid():
        error = f"{error} Formset not valid. num_forms is {num_forms} type: {type(num_forms)}"
        print("error in formset")
        print(f"formset error: {formset.errors}")
    context.update(dict(formset=formset, error=error))
    return render(request, FORM_BULK_TEMPLATE, context=context)


def edit_bulk_forms(request):
    """Review Forms Added. Continue or Re edit from here."""
    FormSet = forms.formset_factory(designer_forms.CreateForm)
    formset = FormSet(request.POST)
    return render(request, FORM_SHOW_BULK_TEMPLATE, context=dict(formset=formset))


def add_form_options(request):
    """Add values to options of selectable field types."""
    context: dict = {}
    formset_opts_list: List = []
    # Get received formset data
    FormSet = forms.formset_factory(designer_forms.CreateForm)
    formset: FormSet = FormSet(request.POST)
    # Get list of form data dictionary
    cleaned_forms_data = formset.cleaned_data
    # Filter out only selectable fields dictionary
    selectable_fields = filter(
        lambda clean_dict: clean_dict["field_type"]
        in designer_forms.constants.FIELD_OPTS,
        cleaned_forms_data,
    )
    # Create multiple formssets for selectable fields values.
    for idx, each_selectable_field in enumerate(selectable_fields):
        # Create Formset for Values in Selectable Options
        FormOptsSet = forms.formset_factory(
            designer_forms.CreateFormOpts,
            extra=each_selectable_field["num_values"],
            formset=designer_forms.CreateFormOptsBaseSet,
        )
        formset_opts_list += [
            FormOptsSet(
                prefix=f"formset-{idx}",
                form_kwargs=dict(
                    field_name=each_selectable_field["field_name"],
                    field_type=each_selectable_field["field_type"],
                ),
            )
        ]
    context.update(dict(formset=formset, formset_opts_list=formset_opts_list))
    return render(request, FORM_ADD_OPTS_TEMPLATE, context=context)


def view_bulk_form(request):
    "View the newly created form."
    return render(request, FORM_VIEW_TEMPLATE)


# def redirect_bulk_forms(request):
#     kwargs: dict = {}
#     if request.method == "POST" and request.POST.get("edit"):
#         return redirect(
#             "designer-bulk-forms",
#             **dict(submit_name=request.POST.get("edit")),
#         )
