__author__ = 'sandy'
# -*- coding:utf-8 -*-
#coding=utf-8
from django.forms import ModelForm
from blog.models import Tsecfield
from django import forms

class SefieldForm(ModelForm):
    idsecfield = forms.IntegerField(label='范畴ID', required=True)
    idparent = forms.MultipleChoiceField(label='父类范畴', required=True)
    secfieldname = forms.CharField(max_length=30)
    class Meta:
        model = Tsecfield