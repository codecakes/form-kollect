from django import forms
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView

from . import forms as designer_forms

FORM_LIST_TEMPLATE = "designer/index.html"
FORM_CREATE_TEMPLATE = "designer/create.html"
FORM_BULK_TEMPLATE = "designer/bulk.html"
FORM_SHOW_BULK_TEMPLATE = "designer/show-bulk.html"
FORM_CREATE_FORM_OPTS_TEMPLATE = "designer/create-form-options.html"


class FormList(ListView):
    template_name = FORM_LIST_TEMPLATE


def create(request):
    """Creates (Bulk)Form Request."""
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
    """Design bulk forms."""
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


def show_bulk_forms(request):
    FormSet = forms.formset_factory(designer_forms.CreateForm)
    formset = FormSet(request.POST)
    context = dict(formset=formset)
    return render(request, FORM_SHOW_BULK_TEMPLATE, context=context)

def create_form_options(request):
    return render(request, FORM_CREATE_FORM_OPTS_TEMPLATE)

# def redirect_bulk_forms(request):
#     kwargs: dict = {}
#     if request.method == "POST" and request.POST.get("edit"):
#         return redirect(
#             "designer-bulk-forms",
#             **dict(submit_name=request.POST.get("edit")),
#         )

