#coding:utf-8
__author__ = 'sandy'
from django.shortcuts import render_to_response
from blog.models import Tusersecfieldrelation, Tuser, Tsecfield, Tpolicy, Tseclass
from django.forms import ModelForm
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
import sys
sys.path.append('..')
from blog.field_class import views

class SefieldForm(ModelForm):
    '''
    :param req: First we get the secfield_id and secfield_name of the parent_secfd_id
     which is Null and the parent_secfd_id is Null.like we chose Null and 1.
     This way is to give us choices to chose when we add secfield.
     Main idea:
     1.we get the first secfield_ids which parent_secfd_id is null.
     2.we continue get the second secfield_ids which parent_secfd_id is in the first secfield_ids.
    :return:to the show secure field html
    '''
    fieldsname=[]
    sefieldid = []
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
    idsecfield = forms.IntegerField(label='范畴ID', required=True)
    idparent = forms.ChoiceField(label='所属范畴', required=True, choices=choise)
    secfieldname = forms.CharField(label='范畴名字', max_length=30, required=True)
    class Meta:
        model = Tsecfield
        fields = ('idsecfield', 'secfieldname', 'idparent')

class Sefield_Form(ModelForm):
    a = Tuser.objects.all()
    uid=[]
    uname=[]
    for i in a:
        uid.append(i.tu_id)
        uname.append(i.login_name)
    userinfo = tuple(zip(uid, uname))
    fields_info = views.FieldForm().allfieldsinfo
    nameofusers = forms.ChoiceField(label='用户名', required=True, choices=userinfo)
    nameoffields = forms.MultipleChoiceField(label='范畴名', required=True, choices=fields_info, \
                                             widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Tuser
        fields = ('nameofusers','nameoffields',)

class PolicyForm(ModelForm):
    fields_info = views.FieldForm().allfieldsinfo
    classes_info = views.ClassForm().allclassinfo
    field = forms.ChoiceField(label=u'范畴名', choices=fields_info,required=True)
    classes = forms.MultipleChoiceField(label=u'分类名称', choices=classes_info, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Tpolicy
        fields = ('field', 'classes')


def showuserfield(req):
    sf = Tusersecfieldrelation.objects.all()
    secfieldinfo={}
    for i in range(sf.count()):
        secfield_names = []
        id = sf.values()[i]['idtusersecfieldrelation']
        tuid = sf.values()[i]['tu_id']
        secfid = sf.values()[i]['secfield_id'].split(',')
        name = Tuser.objects.get(tu_id=tuid).login_name
        for sid in secfid:
            secfield_names.append(Tsecfield.objects.get(secfield_id=sid).secfield_name.encode('utf-8'))
        info = [id,name,secfield_names]
        secfieldinfo[id]=info
    return render_to_response('showuserfield.html', {'secfieldinfo': secfieldinfo})

def adduserfield(req):
    head = u'范畴用户关系'
    if req.method == 'POST':
        af = Sefield_Form(req.POST)
        if af.is_valid():
            print req.POST
            uid = req.POST.get('nameofusers')
            cc =  req.POST.getlist('nameoffields')
            secfieldid = ','.join(cc)
            print secfieldid
            try:
                Tusersecfieldrelation.objects.create(tu_id=int(uid), secfield_id=secfieldid)
            except Exception as e:
                return HttpResponse(e)
            #return HttpResponse('Okkkkk!!!')
            return HttpResponseRedirect('/user_field')
    else:
        af = Sefield_Form()
    return render_to_response('field_classadd.html', {'af':af, 'head':head})

def delufrelation(req, id):
    user_field = Tusersecfieldrelation.objects.get(idtusersecfieldrelation=id)
    user_field.delete()
    return HttpResponseRedirect('/user_field')

def showrelation(req, id):
    '''
    :param req: we send the id and uname to the html.and the checkbox of Secfield_form.
    :param id:kk includes all the secfield_name from the file of field_class.views.py
    :return:
    '''
    kk = views.FieldForm().allfieldsinfo
    # ufrealtion={}
    relationinfo = Tusersecfieldrelation.objects.get(idtusersecfieldrelation=id)
    tu_name = Tuser.objects.get(tu_id=relationinfo.tu_id).login_name
    secfield_ids = relationinfo.secfield_id.split(',')
    secfield_names = []
    for sid in secfield_ids:
        secfield_names.append(Tsecfield.objects.get(secfield_id=sid).secfield_name)
    ufrealtion=[id,tu_name,secfield_names]
    return render_to_response('updateufrelation.html',{'ufrealtion':ufrealtion,'uu':kk})

def updateufrelation(req):
    usfid = req.POST['field_id']
    uname=req.POST.get('user_name')
    tu_id = Tuser.objects.get(login_name=uname).tu_id
    secfieldnames = ','.join(req.POST.getlist('field_names'))
    Tusersecfieldrelation.objects.filter(idtusersecfieldrelation=usfid).update(idtusersecfieldrelation=usfid, \
                                                                               tu_id=tu_id, secfield_id=secfieldnames)
    return HttpResponseRedirect('/user_field')

def showpolicy(req):
    sp = Tpolicy.objects.all()
    policyinfo = {}
    for tp in sp:
        policyid = tp.idtusersecfieldrelation
        secname = Tsecfield.objects.get(secfield_id = tp.secfield_id).secfield_name
        classname=[]
        classids = tp.seclass_id.split(',')
        for classid in classids:
            if int(classid) == 0:
                classname.append('主分类')
            classname.append(Tseclass.objects.get(seclass_id=classid).seclass_name)
        policyinfo[policyid]=[policyid, secname, classname]
    return render_to_response('show_policy.html',{'policyinfo':policyinfo})

def addpolicy(req):
    head = u'添加决策'
    if req.method=='POST':
        poli = PolicyForm(req.POST)
        if poli.is_valid():
            print req.POST
            secfield = req.POST.get('field')
            seclass = ','.join(req.POST.getlist('classes'))
            try:
                Tpolicy.objects.create(secfield_id=int(secfield),seclass_id=seclass)
            except Exception as e:
                return HttpResponse(e)
            return HttpResponseRedirect('/policy')
    else:
        poli = PolicyForm()
    return render_to_response('field_classadd.html',{'af':poli, 'head':head})

def delpolicy(req,id):
    tpolicy = Tpolicy.objects.get(idtusersecfieldrelation=id)
    tpolicy.delete()
    return HttpResponseRedirect('/policy')

