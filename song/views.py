# From rest_framework
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# From Django
from django.contrib.auth.models import User

# From Project
from amituladet.utils import calc_and_stringify
from song.models import Rating, Song
from song.pagination import SongPagination
from song.serializers import RatingSerializer, SongSerializer


class SongViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options']
    serializer_class = SongSerializer
    pagination_class = SongPagination

    def get_queryset(self):
        return Song.objects.all()


class RatingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RatingSerializer
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def get_queryset(self):
        return Rating.objects.all()

    def create(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)
        did_rated = self.get_queryset().filter(user=user,
                                               song=request.data.get('song'))
        if did_rated.exists():
            content = {'error_massage': 'The song was already rated!'}
            return Response(content, status=status.HTTP_409_CONFLICT)

        serializer = self.get_serializer(data={'user': user.id,
                                               'song': request.data.get('song'),
                                               'rating': request.data.get('rating'),
                                               }, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def partial_update(self, request, *args, **kwargs):
        if request.data.get('authorized_change'):
            user = get_object_or_404(User, pk=request.user.id)
            instance = self.get_queryset().filter(user=user,
                                                  song=request.data.get('song'))
            if instance.exists():
                serializer = self.get_serializer(instance=instance.first(),
                                                 data={"rating": request.data.get('rating')},
                                                 context={'request': request}, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

            return Response(status=status.HTTP_404_NOT_FOUND)

        content = {'error_massage': 'The rating can no longer be changed!'}
        return Response(content, status=status.HTTP_409_CONFLICT)

    @action(detail=False)
    def rating_calc(self, request, *args, **kwargs):
        raring_list = Rating.objects.calc_list()
        return Response(calc_and_stringify(raring_list),
                        status=status.HTTP_200_OK)

