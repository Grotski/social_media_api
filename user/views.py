from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from user.serializers import MyTokenObtainPairSerializer

from user.serializers import UserSerializer
from user.forms import UserRegisterForm, UserLogInForm


User = get_user_model()


class CreateUserView(CreateView):
    form_class = UserRegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("user:login_user")
    serializer_class = UserSerializer

    # def get(self, request):
    #     form = UserRegisterForm()
    #     return render(request, "register.html", {"form": form})

    # def post(self, request):
    #     form = UserRegisterForm(request.POST)
    #     if form.is_valid():
    #         print("✅ Form is valid")
    #         form.save()
    #         return redirect("user:login_user")
    #     else:
    #         print("❌ Form is invalid:", form.errors)
    #     return render(request, "register.html", {"form": form})


class MyLoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    success_url = reverse_lazy("social_media_app:chat")
    # template_name = "login.html"
    # form_class = UserLogInForm

    def get(self, request):
        form = UserLogInForm()
        return render(request, "login.html", {"form": form})


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
