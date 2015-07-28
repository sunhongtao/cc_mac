#coding:utf-8
__author__ = 'sandy'
from django.shortcuts import render_to_response
from blog.models import Tusersecfieldrelation, Tuser, Tsecfield
from django.forms import ModelForm
from django import forms


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


def showsecfield(req):
    sf = Tusersecfieldrelation.objects.all()
    secfieldinfo={}
    for i in range(sf.count()):
        secfield_names = []
        id = sf.values()[i]['idtusersecfieldrelation']
        tuid = sf.values()[i]['tu_id']
        secfid = sf.values()[i]['secfield_id'].split(',')
        name = Tuser.objects.get(tu_id=tuid).username
        for id in secfid:
            secfield_names.append(Tsecfield.objects.get(secfield_id=id).secfield_name.encode('utf-8'))
        info = [id,name,secfield_names]
        secfieldinfo[id]=info
    return render_to_response('show_secfield.html', {'secfieldinfo': secfieldinfo})

def addsefield(req):
    if req.method == 'POST':
        af = SefieldForm(req.POST)
        if af.is_valid():
            print af
    else:
        af = SefieldForm()
    return render_to_response('secfieldadd.html', {'af':af})
    pass