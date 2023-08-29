from django.urls import path, re_path, include
from django.views.generic import TemplateView
from rest_framework import renderers as rest_fw_renderers, routers as rest_fw_routers
from rest_framework.schemas import get_schema_view
from . import views

app_name = "player"

router = rest_fw_routers.DefaultRouter()

urlpatterns = [
    re_path('^performer/?$', views.PerformerListCreateView.as_view(),
            name="performer-list"),
    re_path('^performer/(?P<pk>[0-9]+)/?$', views.PerformerDetailUpdateDeleteView.as_view(),
            name="performer-detail"),
    re_path('^album/?$', views.AlbumListCreateView.as_view(),
            name="album-list"),
    re_path('^album/(?P<pk>[0-9]+)/?$', views.AlbumDetailUpdateDeleteView.as_view(),
            name="album-detail"),
    re_path('^song/?$', views.SongListCreateView.as_view(),
            name="song-list"),
    re_path('^song/(?P<pk>[0-9]+)/?$', views.SongDetailUpdateDeleteView.as_view(),
            name="song-detail"),
    re_path('^songs_in_albums/?$', views.SongsInAlbumsListCreateView.as_view(),
            name="songsInAlbums-list"),
    re_path('^songs_in_albums/(?P<pk>[0-9]+)/?$',
            views.SongsInAlbumsDetailUpdateDeleteView.as_view(),
            name="songsInAlbums-detail"),

    path('openapi/', get_schema_view(
        title="App API", description="API", version="1.0.0",), name='openapi-schema'),
    path('openapi-schema.json/', get_schema_view(
        title="App API", description="API",  version="1.0.0",
        renderer_classes=[rest_fw_renderers.JSONOpenAPIRenderer],
    ), name='openapi-schema-json'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html', extra_context={'schema_url': 'player:openapi-schema'}
    ), name='swagger-ui'),
    path('', include(router.urls)),
]
