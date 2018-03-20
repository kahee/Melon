from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView

from artist import serializers
from members.serializers import UserSerializer


class AuthTokenView(APIView):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            Token.objects.get_or_create(user=user)
            print(Token.key)

            serializer = UserSerializer(data=request.user, many=True)

            if serializer.is_valid():
                serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        #
        # return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
