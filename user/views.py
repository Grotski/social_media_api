from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.serializers import UserSerializer
from user.forms import UserRegisterForm, UserLogInForm


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

    @action(detail=False, methods=["get"])
    def get(self, request):
        form = UserRegisterForm()
        return render(request, "register.html", {"form": form})


class LoginView(generics.CreateAPIView):
    serializer_class = UserSerializer
    
    @action(detail=False, methods=["get"])
    def get(self, request):
        form = UserLogInForm()
        return render(request, "login.html", {"form": form})


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
