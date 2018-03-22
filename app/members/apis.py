from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.compat import authenticate
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


class AuthTokenView(APIView):

    def post(self, request):
        serializers = AuthTokenSerializer(data=request.data)
        # 오류가 발생하면 exception 발생
        serializers.is_valid(raise_exception=True)
        user = serializers.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        data = {
            'token': token.key,
            'user': UserSerializer(user).data,
        }

        return Response(data)

        # raise APIException('authenticate failure')
        # raise AuthenticationFailed()


class MyUserDetail(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
