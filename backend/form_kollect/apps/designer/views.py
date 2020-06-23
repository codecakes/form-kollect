from django.shortcuts import render
from django.http import HttpResponse
from . import forms as designer_forms
from django.views.generic import ListView
from django import forms

FORM_LIST_TEMPLATE = "designer/index.html"
FORM_CREATE_TEMPLATE = "designer/create.html"
FORM_BULK_TEMPLATE = "designer/bulk.html"
FORM_SHOW_BULK_TEMPLATE = "designer/show-bulk.html"


class FormList(ListView):
    template_name = FORM_LIST_TEMPLATE


def create(request):
    context: dict = {}
    msg: str = ''
    error: str = ''
    more_forms = designer_forms.AddMoreFormRequest()
    if request.method == 'POST':
        form = designer_forms.CreateForm(request.POST)
        if form.is_valid():
            msg = 'thanks'
        else:
            error = 'Form is invalid'
        context.update(
            dict(
                msg=msg,
                error=error,
                form=form,
                more_forms=more_forms)
        )
    else:
        context.update(dict(form=designer_forms.CreateForm(), more_forms=more_forms))
    return render(request, FORM_CREATE_TEMPLATE, context=context)


def create_bulk_forms(request):
    error: str = ''
    num_forms: int = 2
    context: dict = {}
    more_forms = designer_forms.AddMoreFormRequest(request.GET)
    if more_forms.is_valid():
        num_forms = more_forms.cleaned_data['num_forms']
    else:
        error = "Invalid Incoming Form."
    FormSet = forms.formset_factory(designer_forms.CreateForm, extra=num_forms)
    formset = FormSet()
    if not formset.is_valid():
        error = f"{error} Formset not valid. num_forms is {num_forms} type: {type(num_forms)}"
        print('formset')
        print(formset)
    context.update(dict(formset=formset, error=error))
    return render(request, FORM_BULK_TEMPLATE, context=context)

def show_bulk_forms(request):
    FormSet = forms.formset_factory(designer_forms.CreateForm)
    formset = FormSet(request.POST)
    context = dict(formset=formset)
    return render(request, FORM_SHOW_BULK_TEMPLATE, context=context)

