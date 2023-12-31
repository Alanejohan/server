# for django-rest framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

# for simple jwt
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

# for register views
from django.contrib.auth.hashers import make_password
from rest_framework import status

from .serializers import UserSerializerWithToken
from .models import User
from category.models import Category


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # customizing view
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    # serializing
    serializer_class = MyTokenObtainPairSerializer


@api_view(["POST"])
def registerUser(request):
    """Gets User data and Create New User"""
    data = request.data
    print("Data:", data)
    try:
        user = User.objects.create(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=make_password(data["password"]),
        )

         # Add preferences to the user
        preferences = data.get("preferences", [])  # Get the preferences from the request data
        for preference_id in preferences:
            preference = Category.objects.get(id=preference_id)
            user.preferences.add(preference)

        serializer = UserSerializerWithToken(user, many=False, context={"request": request})
        return Response(serializer.data)
    except Exception as e:
        message = {"detail": str(e)}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """Blacklist the refresh token for effective logout
    The token should also be discarded from the frontend
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            message = {"detail": "Logout Successful"}
            return Response(message, status=status.HTTP_200_OK)
        except Exception as e:
            message = {"detail": str(e)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
