from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from allauth.socialaccount.providers.linkedin.views import LinkedInOAuthAdapter
from django.views.decorators.csrf import csrf_exempt
from rest_auth.registration.views import SocialLoginView
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import parsers
from rest_framework import renderers
from rest_framework.authtoken.models import Token as AuthToken
from rest_framework.response import Response
from apps.core.serializers import AuthCustomTokenSerializer, UserSerializer, UserDetailSerializer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import facebook


User = get_user_model()


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class TwitterLogin(SocialLoginView):
    adapter_class = TwitterOAuthAdapter


class LinkedinLogin(SocialLoginView):
    adapter_class = LinkedInOAuthAdapter


class SignUpAPIView(APIView):
    """
        Creates the user.
        """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )

    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                #json = serializer.data
                json = dict()
                json['access'] = True
                json['id']= user.id
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainAuthToken(APIView):
    """
    Example post
    data: {email_or_username, password }
    const result = await fetch(CONSTANTS.API_URL, {
				method: 'POST', // or 'PUT'
				headers: {
					 'Accept': 'application/json',
					 'Content-Type': 'application/json'
				 },
				body: JSON.stringify(data), // data can be `string` or {object}!
			})
			.then((response)=>response.json())
			return result
	}
	:return "token"
    """
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
            'id': user.id
        }

        return Response(content)


class UserDetailView(RetrieveAPIView):
    """
    Use this endpoint to retrieve user.
    """
    # Set the AUTH_USER_MODEL in settings.py file to make it work with custom user models as well.
    model = User
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, *args, **kwargs):
        return self.request.user