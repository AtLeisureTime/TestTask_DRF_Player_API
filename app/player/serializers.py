from rest_framework import serializers as rest_fw_serializers
from . import models, exceptions


class PerformerSerializerListCreateUpdate(rest_fw_serializers.ModelSerializer):
    class Meta:
        model = models.Performer
        fields = '__all__'


class AlbumSerializerListCreateUpdate(rest_fw_serializers.ModelSerializer):
    class Meta:
        model = models.Album
        fields = '__all__'


class SongSerializerListUpdate(rest_fw_serializers.ModelSerializer):
    albums = rest_fw_serializers.PrimaryKeyRelatedField(
        many=True, allow_null=True, queryset=models.Album.objects.all())

    class Meta:
        model = models.Song
        fields = '__all__'

    def validate(self, attrs):
        qs = self.fields['albums'].get_attribute(self.instance)
        dbAlbums = set(qs.values_list('pk', flat=True))
        requestAlbums = {album.pk for album in attrs['albums']}
        albumsNotFromDb = requestAlbums - dbAlbums
        if albumsNotFromDb:
            raise exceptions.AppLogicError(
                f"This song isn't in albums {albumsNotFromDb}. "
                "Use POST 'songs_in_albums/' requests to add the song to new albums.")
        return super().validate(attrs)


def validateUniqueConstraints(qs, attrs, onlySongNumInAlbum=False):
    """ Validate unique constraints of SongsInAlbums model.
        Workaround of https://github.com/encode/django-rest-framework/issues/7173 """
    if qs.filter(album=attrs['album'], songNumber=attrs['songNumber']).exists():
        albumId = attrs['album'].pk if isinstance(attrs['album'], models.Album) else attrs['album']
        raise exceptions.AppLogicError(
            f"'songNumber' {attrs['songNumber']} is already used in 'album' {albumId}.")
    if onlySongNumInAlbum:
        return

    if qs.filter(song=attrs['song'], songNumber=attrs['songNumber']).exists():
        raise exceptions.AppLogicError(
            f"'songNumber' {attrs['songNumber']} is already used for 'song' {attrs['song'].pk}.")

    if qs.filter(song=attrs['song'], album=attrs['album']).exists():
        raise exceptions.AppLogicError(
            f"'song' {attrs['song'].pk} has been already added to 'album' {attrs['album'].pk}.")


class SongNumInAlbumsSerializerCreate(rest_fw_serializers.Serializer):
    albumId = rest_fw_serializers.IntegerField()
    songNumber = rest_fw_serializers.IntegerField()


class SongSerializerListCreate(rest_fw_serializers.ModelSerializer):
    albums = rest_fw_serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    songNumInAlbums = SongNumInAlbumsSerializerCreate(many=True, write_only=True)

    class Meta:
        model = models.Song
        fields = '__all__'

    def validate(self, attrs):
        songNumInAlbums = attrs.get('songNumInAlbums', [])
        albumIds = [songNumInAlbum.get('albumId')
                    for songNumInAlbum in songNumInAlbums if songNumInAlbum]
        songNumbers = [songNumInAlbum.get('songNumber')
                       for songNumInAlbum in songNumInAlbums if songNumInAlbum]

        if len(albumIds) != len(set(albumIds)):
            raise exceptions.AppLogicError("The song can't be added to the same album 2 times.")
        if len(songNumbers) != len(set(songNumbers)):
            raise exceptions.AppLogicError("Song numbers should be unique.")

        for albumId, songNumber in zip(albumIds, songNumbers):
            qs = models.SongsInAlbums.objects
            _attrs = {'album': albumId, 'songNumber': songNumber}
            validateUniqueConstraints(qs, _attrs, onlySongNumInAlbum=True)

        return super().validate(attrs)

    def create(self, validated_data):
        songNumInAlbums = validated_data.pop('songNumInAlbums', [])
        newSong = super().create(validated_data)

        albumIds = [songNumInAlbum.get('albumId')
                    for songNumInAlbum in songNumInAlbums if songNumInAlbum]
        if albumIds:
            albumId_songNum = {songNumInAlbum.get('albumId'): songNumInAlbum.get('songNumber')
                               for songNumInAlbum in songNumInAlbums if songNumInAlbum}
            albums = models.Album.objects.filter(pk__in=albumIds)
            albumIds = albums.values_list('pk', flat=True)
            songNums = [albumId_songNum.get(albumId) for albumId in albumIds]
            for album, songNum in zip(albums, songNums):
                newSong.albums.add(album, through_defaults={'songNumber': songNum})
        return newSong


class SongsInAlbumsSerializerListCreate(rest_fw_serializers.ModelSerializer):
    class Meta:
        model = models.SongsInAlbums
        fields = '__all__'

    def validate(self, attrs):
        qs = models.SongsInAlbums.objects
        validateUniqueConstraints(qs, attrs)
        return super().validate(attrs)


class SongsInAlbumsSerializerUpdate(rest_fw_serializers.ModelSerializer):
    class Meta:
        model = models.SongsInAlbums
        fields = '__all__'

    def validate(self, attrs):
        if self.instance:
            attrs = {attr: attrs[attr] if attr in attrs else getattr(self.instance, attr)
                     for attr in ['album', 'song', 'songNumber']}
            qs = models.SongsInAlbums.objects.exclude(pk=self.instance.id)
            validateUniqueConstraints(qs, attrs)
        return super().validate(attrs)
