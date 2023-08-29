from rest_framework import generics as rest_fw_generics
from rest_framework import mixins as rest_fw_mixins
import django_filters
from . import models, serializers


class CustomRetrieveUpdateDestroyMixin(rest_fw_mixins.RetrieveModelMixin,
                                       rest_fw_mixins.UpdateModelMixin,
                                       rest_fw_mixins.DestroyModelMixin,
                                       rest_fw_generics.GenericAPIView):
    """ Define serializer_class_get and serializer_class_patch in subclass."""
    def get_serializer_class(self):
        if self.request:
            if self.request.method in {"GET", "DELETE"}:
                if hasattr(self.__class__, 'serializer_class_get'):
                    return self.__class__.serializer_class_get
            elif self.request.method == "PATCH":
                if hasattr(self.__class__, 'serializer_class_patch'):
                    return self.__class__.serializer_class_patch
        return self.__class__.serializer_class

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PerformerDetailUpdateDeleteView(CustomRetrieveUpdateDestroyMixin):
    queryset = models.Performer.objects.all()
    serializer_class = serializers.PerformerSerializerListCreateUpdate


class PerformerListCreateView(rest_fw_generics.ListCreateAPIView):
    queryset = models.Performer.objects.all()
    serializer_class = serializers.PerformerSerializerListCreateUpdate


class AlbumDetailUpdateDeleteView(CustomRetrieveUpdateDestroyMixin):
    queryset = models.Album.objects.select_related('performer')
    serializer_class = serializers.AlbumSerializerListCreateUpdate


class AlbumListCreateView(rest_fw_generics.ListCreateAPIView):
    queryset = models.Album.objects.select_related('performer')
    serializer_class = serializers.AlbumSerializerListCreateUpdate


class SongDetailUpdateDeleteView(CustomRetrieveUpdateDestroyMixin):
    queryset = models.Song.objects.prefetch_related('albums')
    serializer_class = serializers.SongSerializerListUpdate


class SongListCreateView(rest_fw_generics.ListCreateAPIView):
    queryset = models.Song.objects.prefetch_related('albums')
    serializer_class = serializers.SongSerializerListCreate


class SongsInAlbumsListCreateView(rest_fw_generics.ListCreateAPIView):
    queryset = models.SongsInAlbums.objects.select_related('album', 'song')
    serializer_class = serializers.SongsInAlbumsSerializerListCreate
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['album', 'songNumber', 'song']


class SongsInAlbumsDetailUpdateDeleteView(CustomRetrieveUpdateDestroyMixin):
    queryset = models.SongsInAlbums.objects.select_related('album', 'song')
    serializer_class_get = serializers.SongsInAlbumsSerializerListCreate
    serializer_class_patch = serializers.SongsInAlbumsSerializerUpdate
