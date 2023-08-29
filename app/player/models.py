import datetime
from django.db import models
import django.core.validators as dj_validators


class Performer(models.Model):
    NAME_LEN = 80
    name = models.CharField(max_length=NAME_LEN, blank=False)


def maxValueCurrentYear(value):
    currentYear = datetime.date.today().year
    return dj_validators.MaxValueValidator(currentYear)(value)


class Album(models.Model):
    TITLE_LEN = 80
    performer = models.ForeignKey(Performer, on_delete=models.CASCADE, blank=False)
    title = models.CharField(max_length=TITLE_LEN, blank=False)
    year = models.PositiveSmallIntegerField(
        validators=[dj_validators.MinValueValidator(0), maxValueCurrentYear])


class Song(models.Model):
    TITLE_LEN = 80
    title = models.CharField(max_length=TITLE_LEN, blank=False)
    albums = models.ManyToManyField(Album, through='SongsInAlbums', blank=False)


class SongsInAlbums(models.Model):
    MIN_SONG_NUM = 1
    MAX_SONG_NUM = 32767

    album = models.ForeignKey(Album, on_delete=models.CASCADE, blank=False)
    songNumber = models.PositiveSmallIntegerField(
        null=False, blank=False, validators=[
            dj_validators.MinValueValidator(MIN_SONG_NUM),
            dj_validators.MaxValueValidator(MAX_SONG_NUM)])
    song = models.ForeignKey(Song, on_delete=models.CASCADE, blank=False)

    class Meta:
        constraints = [
            models.constraints.UniqueConstraint('song_id', 'songNumber',
                                                name='unique_songId_songNumber'),
            models.constraints.UniqueConstraint('song_id', 'album_id',
                                                name='unique_songId_albumId'),
            models.constraints.UniqueConstraint('album_id', 'songNumber',
                                                name='unique_albumId_songNumber'),
        ]
