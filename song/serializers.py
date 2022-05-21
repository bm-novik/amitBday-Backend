from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer

from song.models import Song, Rating


class SongSerializer(ModelSerializer):
    was_rated = SerializerMethodField()

    class Meta:
        model = Song
        fields = ['id', 'singer', 'song', 'was_rated']
        read_only_fields = ["id"]

    def get_was_rated(self, obj):
        request = self.context.get('request')
        user_rating = Rating.objects.filter(song=obj, user=request.user)
        if user_rating.exists():
            return user_rating.first().rating
        return None


class RatingSerializer(ModelSerializer):

    class Meta:
        model = Rating
        fields = ['id', 'user', 'song', 'rating']
        read_only_fields = ["id"]



class RatingCalc(Serializer):
    pass