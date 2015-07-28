# -*- coding:utf-8 -*-
__author__ = 'sandy'
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.forms import ModelForm
from django import forms
from blog.models import Tsecfield
import datetime

class FieldForm(ModelForm):
    fieldsname=[]
    sefieldid = []
    sefieldid.append(0)
    fieldsname.append('主范畴')
    fields = Tsecfield.objects.filter(parent_secfd_id=0)#the names of null
    for field in fields:#[音乐 相声]
        secfid = Tsecfield.objects.get(secfield_name=field).secfield_id#[1,7]
        sefieldid.append(secfid) #the secfield_ids which the parent_secfd_id is null
        fieldsname.append(field)#the secfield_names which the parent_secf_id is null
        secondname = Tsecfield.objects.filter(parent_secfd_id=secfid) #[1:2 5]
        for second in secondname:
            secfidid = Tsecfield.objects.get(secfield_name=second).secfield_id
            sefieldid.append(secfidid)
            fieldsname.append(second)
    fieldinfo = zip(sefieldid,fieldsname)
    choise = tuple(fieldinfo)
    #idsecfield = forms.IntegerField(label='范畴ID', required=True)
    idparent = forms.ChoiceField(label='所属范畴', required=True, choices=choise)
    secfieldname = forms.CharField(label='范畴名字', max_length=30, required=True)
    class Meta:
        model = Tsecfield
        fields = ('idparent', 'secfieldname')


def ss(req):
    return HttpResponseRedirect('/field')

def showfield(req):
    a=Tsecfield.objects.all()
    fieldinfo={}
    for i in range(a.count()):
        fieldid = a.values()[i]['secfield_id']
        parentid = a.values()[i]['parent_secfd_id']
        if parentid == 0:
            parentname='主范畴'
        else:
            parentname = Tsecfield.objects.get(secfield_id=parentid)
        fieldname = a.values()[i]['secfield_name']
        name=[fieldid, fieldname, parentname]
        fieldinfo[fieldid]=name
    return render_to_response('show_fields.html',{'fieldinfo':fieldinfo})

def addfield(req):
    fieldinfo = Tsecfield()
    if req.method == 'POST':
        af = FieldForm(req.POST)
        if af.is_valid():
            parentname = req.POST['idparent'].encode('utf-8')
            fieldname = req.POST['secfieldname'].encode('utf-8')
            fieldinfo.parent_secfd_id = int(parentname)
            fieldinfo.secfield_name = fieldname
            fieldinfo.gen_time = datetime.datetime.now()
            try:
                fieldinfo.save()
            except Exception as e:
                return HttpResponse(e)
            return HttpResponseRedirect('/field')
    else:
        af = FieldForm()
    return render_to_response('secfieldadd.html', {'af':af})

def delfield(req, id):
    print id
    field_info = Tsecfield.objects.get(secfield_id=id)
    #field_info.delete()
    return HttpResponseRedirect('/field')

def showfid(req, id):
    uf = FieldForm().fieldinfo
    field_info = Tsecfield.objects.get(secfield_id=id)
    fieldname = field_info.secfield_name
    field_id = field_info.secfield_id
    parent_name = field_info.parent_secfd_id
    field = [fieldname, field_id, parent_name]
    for k,v in uf:
        if k == field[2]:
            print k
    return render_to_response('updatefield.html', {'field':field,'uu':uf})

def updatefield(req):
    print req.POST
    fieid = req.POST['field_id']
    fiename = req.POST['field_name']
    parentname = req.POST['parent_name']
    print parentname
    print parentname != u'主范畴'
    print Tsecfield.objects.get(secfield_name=parentname)
    gentime = datetime.datetime.now()
    if parentname != u'主范畴':
        parid = Tsecfield.objects.get(secfield_name=parentname).secfield_id
        print '###',parid
        Tsecfield.objects.filter(secfield_id=fieid).update(secfield_id=fieid,secfield_name=fiename,parent_secfd_id=parid)
    return HttpResponseRedirect('/field')