from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from ...models import Artist
from ...pagination import StandardResultsSetPagination
from ...serializers import ArtistSerializer


class ArtistListView(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def get(self, request, *args, **kwargs):
        print('request.user:', request.user)
        return super().get(request, *args, **kwargs)


class ArtistDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    pagination_class = StandardResultsSetPagination
