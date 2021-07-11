from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer


class UserLoginSerializer(TokenObtainSerializer):
	@classmethod
	def get_token(cls, user):
		return RefreshToken.for_user(user)

	def validate(self, attrs):
		data = super().validate(attrs)

		refresh = self.get_token(self.user)

		data['tokens'] = {
			'refresh': str(refresh),
			"access": str(refresh.access_token)
		}

		data['user'] = {
			'username': self.user.username,
			'email': self.user.email,
			'first_name': self.user.first_name,
			'last_name': self.user.last_name
		}

		return data
