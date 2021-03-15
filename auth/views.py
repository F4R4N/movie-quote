from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .serializers import UserLoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase
from rest_framework_simplejwt.tokens import RefreshToken

class UserLoginView(TokenViewBase):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT, data={'detail': "logged out"})
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "refresh_token is not valid"})
