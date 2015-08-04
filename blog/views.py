# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from blog.models import Tseclass,Tuser,Tmeta,Tusersecfieldrelation,Tsecfield
from django.http import HttpResponseRedirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from os import popen
from blog.forms import MetaForm
from django.core.cache import cache
import re

def main(req):
    a = Tseclass.objects.filter(parent_secl_id=None)
    det={}
    for i in range(a.count()):
        seclassid = a.values()[i]['seclass_id']
        name = a.values()[i]['seclass_name']
        aa = Tseclass.objects.filter(parent_secl_id=seclassid)
        detdet={}
        for ii in range(aa.count()):
            seclassidid = aa.values()[ii]['seclass_id']
            name1 = aa.values()[ii]['seclass_name']
            d = Tseclass.objects.filter(parent_secl_id=seclassidid)
            detdet[name1]=d
        det[name]=detdet
    return render_to_response('main.html',{'det':det})

def test(req):
    uname = req.GET['id'].encode('utf-8')
    a = Tseclass.objects.filter(parent_secl_id=0)
    det={}
    for i in range(a.count()):
        seclassid = a.values()[i]['seclass_id']
        name = a.values()[i]['seclass_name'] #yinyue xiangsheng
        aa = Tseclass.objects.filter(parent_secl_id=seclassid)
        detdet={}
        for ii in range(aa.count()):
            seclassidid = aa.values()[ii]['seclass_id']
            name1 = aa.values()[ii]['seclass_name']
            d = Tseclass.objects.filter(parent_secl_id=seclassidid)
            detdetdet={}
            for iii in range(d.count()):
                seclassididid = d.values()[iii]['seclass_id']
                name11 = d.values()[iii]['seclass_name']
                detdetdet[name11]=seclassididid
            detdet[name1]=detdetdet
        det[name]=detdet
    return render_to_response('test.html',{'det':det, 'uname':str(uname)})

def beginAddmeta(req):
    return render_to_response('addmeta.html')

@csrf_exempt
def addmeta(req):
   # c={}
    obj_id =req.POST['obj_id']
    obj_name=req.POST['obj_name']
    obj_secl_id = req.POST['obj_secl_id']
    obj_level = req.POST['obj_level']
    st=Tmeta()

    st.object_id=obj_id
    st.object_name=obj_name
    st.parent_secl_id=obj_secl_id
    st.obj_seclevel = obj_level
    st.save()
    return HttpResponseRedirect("/meta?id=%s"%obj_id)

def delmByID(request, me_id, name, id):
    '''
    :param request:
    :param me_id: the parent_secl_id of Tmeta database,we can return the page after we delete the id of meta.
    :param name: the meta name
    :param id: the meta object_id
    :return: return to the page of before we execute delete.
    '''

    bb=Tmeta.objects.get(object_id=id)

    bb.delete()
    return HttpResponseRedirect("/meta/id=%s/name=%s" % (me_id, name))

def showMid(req):
    obj_id = req.GET['id']
    bb = Tmeta.objects.get(object_id=obj_id)
    return render_to_response('updatemeta.html',{'data': bb})

def showmeta(req, meid, uname):
    #meid = req.GET['id']
    print meid
    #uname = req.GET['name'].encode('utf-8')
    print uname
    mt = Tmeta.objects.filter(parent_secl_id=meid)
    metainfo = {}
    for i in range(mt.count()):
        objectid = mt.values()[i]['object_id']
        name = mt.values()[i]['object_name']
        paseclid = mt.values()[i]['parent_secl_id']
        paseclname = Tseclass.objects.get(seclass_id=paseclid).seclass_name
        objseclevel = mt.values()[i]['obj_seclevel']
        author = mt.values()[i]['author']
        objpath = mt.values()[i]['path']
        #name=[objectid,name,paseclid,objseclevel,objpath]
        name=[objectid, name, paseclname, objseclevel, author, objpath]
        metainfo[objectid]=name
    return render_to_response('show_meta.html',{'metainfo':metainfo, 'uname':uname, 'mt_id':meid})

def frame(req):
    return render_to_response('MyFrame.html')

def showsecfield(req):
    sf = Tusersecfieldrelation.objects.all()
    secfieldinfo={}
    for i in range(sf.count()):
        secfield_names = []
        id = sf.values()[i]['idtusersecfieldrelation']
        tuid = sf.values()[i]['tu_id']
        secfid = sf.values()[i]['secfield_id'].split(',')
        print type(secfid)
        name = Tuser.objects.get(tu_id=tuid).username
        for id in secfid:
            print Tsecfield.objects.get(secfield_id =id).secfield_name
            secfield_names.append(Tsecfield.objects.get(secfield_id=id).secfield_name.encode('utf-8'))
        info = [id,name,secfield_names]
        secfieldinfo[id]=info
    return render_to_response('showuserfield.html',{'secfieldinfo':secfieldinfo})

def top(req):
    name = req.GET['id']
    if not name:
        name = cache.get(name)
    cache.set(name, name)
    return render_to_response('top.html',{'name':name})

def login(req):
    if req.method == 'POST':
        name = req.POST.get('uname','')
        passwd = req.POST.get('upasswd','')
        nm = Tuser.objects.filter(login_name__exact='%s' % name, password__exact='%s' % passwd)
        if nm:
            print name,passwd
            return render_to_response('MyFrame.html', {'name':name})
    return render_to_response('login.html', {'document_root':'~/sun/django/mac/blog/templates/images'})

def metaadd(req):
    '''
    :param req:
    :return:
    '''
    uname = req.GET['id'].encode('utf-8')
    name_token = '_'.join([uname, 'token'])
    name_url = '_'.join([uname,'url'])
    token = cache.get(name_token)
    url = cache.get(name_url)
    pattern = re.compile('\(.+\)')
    if req.method == 'POST':
        mf = MetaForm(req.POST,req.FILES)
        if mf.is_valid():
            name = req.POST.get('object_name').encode('utf-8')
            secfiled = req.POST.get('parent_secl_id').encode('utf-8')
            seclevel = req.POST.get('obj_seclevel').encode('utf-8')
            meta_info = dict(req.FILES).values()[0]
            stype = pattern.findall(str(meta_info))[0].strip('()')
            path = str(meta_info).split(' ')[1]
            print stype,path,name,secfiled,seclevel,meta_info,stype
            values=(path, name, secfiled, seclevel, stype, token, str(url)+'/sun/%s'% path)
            print values
            print url
            content = popen("curl -X PUT -T ~/%s -D- -H 'object_name:%s' -H 'parent_secl_id:%s' -H \
            'obj_seclevel:%s' -H 'Content-Type:%s' -H '%s' %s" % values).readlines()
            print content
            return HttpResponse(content[-1])
    else:
        mf = MetaForm()
    return render_to_response('addmetadb.html', {'mf':mf})

def gettoken(req):
    '''
    :param the attribute: we should know the user name .and then use the api to get the token with
     popen function.
    :return:still in the page.but we have stored the token and url in the cache.
    '''
    name = req.GET['id'].encode('utf-8')
    content = popen("curl -D- -H 'X-Storage-User:%s' http://192.168.119.89:8080/auth/v1.0" % name).readlines()
    name_info = '_'.join([name,'info'])
    token = content[2].strip()
    url = content[1].split(':', 1)[-1].strip()
    print url
    name_token = '_'.join([name, 'token'])
    name_url = '_'.join([name, 'url'])
    cache.set(name_token, token, 12700)
    cache.set(name_url, url, 12700)
    return HttpResponseRedirect("/top?id=%s"%name)

