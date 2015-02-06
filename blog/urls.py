from django.conf.urls import patterns, url
from . import views, feed

urlpatterns = patterns(
    '',
    url(r'^feed/$', feed.LatestPosts(), name="feed"),
    url(r'^$', views.BlogIndex.as_view(), name="home"),
    url(r'^contact/$', views.ContactFormView, name="contact"),
    url(r'^cv/$', views.cv, name="cv"),
    url(r'^blog/$', views.blog, name="blog"),

    url(r'^entry/(?P<slug>\S+)$', views.BlogDetail.as_view(), name="entry_detail"),
    # url(r'^$', views., name='index'),
)