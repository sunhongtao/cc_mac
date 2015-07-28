from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^main/$', 'blog.views.frame'),
    url(r'^test/$', 'blog.views.test'),
    url(r'^addmeta.html$', 'blog.views.beginAddmeta'),
    url(r'^addmeta$', 'blog.views.addmeta'),
    url(r'deletemeta/mtid=(\d+)/name=(\w+)/id=(\d+)$', 'blog.views.delmByID'),
    url(r'showmid$', 'blog.views.showMid'),
    url(r'^meta/id=(\d+)/name=(\w+)', 'blog.views.showmeta'),
    url(r'^top/$', 'blog.views.top'),
    url(r'^$', 'blog.views.login'),
    url(r'^metaadd$', 'blog.views.metaadd'),
    url(r'^gettoken', 'blog.views.gettoken'),
    url(r'^admin/', include(admin.site.urls)),
)

# access control
urlpatterns += patterns('blog.Access_control',
    url(r'^user_field', 'views.showsecfield'),
    url(r'^addsefield/$','views.addsefield')
)

#User control
urlpatterns += patterns('blog.user',
    url(r'^user/$', 'views.showuser'),
    url(r'^adduser.html$', 'views.beginAdduser'),
    url(r'^adduser$', 'views.adduser'),
    url(r'deleteuser$', 'views.deluByID'),
    url(r'showuid$', 'views.showUid'),
    url(r'^updateuser$', 'views.updateuser'),
)

#secure_field and secure_class management
urlpatterns += patterns('blog.field_class',
    url(r'^field/', 'views.showfield'),
    url(r'^showfields$', 'views.ss'),
    url(r'^addfield$', 'views.addfield'),
    url(r'^delfield/id=(\d+)$', 'views.delfield'),
    url(r'^showfieldid/id=(\d+)$', 'views.showfid'),
    url(r'^updatefield$', 'views.updatefield'),
)