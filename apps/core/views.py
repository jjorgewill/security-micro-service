from rest_framework.views import APIView
from rest_framework.response import Response
from apps.core.serializers import AuthCustomTokenSerializer, UserSerializer
from rest_framework import parsers
from rest_framework import renderers
from rest_framework.authtoken.models import Token as AuthToken


class UserView(APIView):

    def get(self, request):
        queryset = request.user
        serializer = UserSerializer(queryset)
        return Response(serializer.data)


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )

    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = AuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = AuthToken.objects.get_or_create(user=user)

        content = {
            'token': str(token.key),
        }

        return Response(content)