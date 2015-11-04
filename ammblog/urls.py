from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'ammblog_app.views.index'),
    url(r'^login$', 'ammblog_app.views.login_view'),
    url(r'^logout$', 'ammblog_app.views.logout_view'),
    url(r'^signup$', 'ammblog_app.views.signup'),
    url(r'^register$', 'ammblog_app.views.register'),
    url(r'^submit$', 'ammblog_app.views.submit'),
    url(r'^users/(?P<username>\w{0,30})/$', 'ammblog_app.views.users'),
    url(r'^users/$', 'ammblog_app.views.users'),
    url(r'^follow$', 'ammblog_app.views.follow'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
