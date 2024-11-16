from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class RegisterView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Correo electrónico y contraseña son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        if get_user_model().objects.filter(email=email).exists():
            return Response({"error": "El correo electrónico ya está en uso."}, status=status.HTTP_400_BAD_REQUEST)

        # Crear el usuario manualmente sin pasar username
        user = get_user_model()(email=email)
        user.set_password(password)
        user.save()

        return Response({"message": "Usuario creado con éxito."}, status=status.HTTP_201_CREATED)


class CustomAuthToken(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"detail": "Correo electrónico y contraseña son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return Response({"detail": "Usuario no encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return Response({"detail": "Contraseña incorrecta."}, status=status.HTTP_400_BAD_REQUEST)

        # Generar el token
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
