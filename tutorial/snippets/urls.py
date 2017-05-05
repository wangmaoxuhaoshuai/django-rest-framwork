from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url,include
from snippets import views
from snippets.views import SnippetViewSet, UserViewSet, api_root
from rest_framework import renderers
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

#urlpatterns = [
#    url(r'^$',views.api_root),
#    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$',views.SnippetHighlight.as_view())
#    url(r'^snippets/$', views.SnippetList.as_view()),
#    url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
#    url(r'^authors/$',views.author_list),
#    url(r'^authors/(?P<pk>[0-9]+)/$',views.author_detail),
#	]

router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

schema_view = get_schema_view(title='Pastebin API')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('^schema/$',schema_view),
]

snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
snippet_highlight = SnippetViewSet.as_view({
    'get': 'highlight'
    }, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = format_suffix_patterns([
#    url(r'^$', views.api_root),
#    url(r'^snippets/$',
#        views.SnippetList.as_view(),
#        name='snippet-list'),
#    url(r'^snippets/(?P<pk>[0-9]+)/$',
#        views.SnippetDetail.as_view(),
#	name='snippet-detail'),
#    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$',
#        views.SnippetHighlight.as_view(),
#	name='snippet-highlight'),
#    url(r'^users/$',
#        views.UserList.as_view(),
#	name='user-list'),
#    url(r'^users/(?P<pk>[0-9]+)/$',
#        views.UserDetail.as_view(),
#	name='user-detail'),
    url(r'^$', api_root),
    url(r'^snippets/$', snippet_list, name='snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$', snippet_detail, name='snippet-detail'),
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', snippet_highlight, name='snippet-highlight'),
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail')
])

# Login and logout views for the browsable API
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
       namespace='rest_framework')),
       ]
