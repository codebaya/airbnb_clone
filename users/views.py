from django.conf import settings
from django.contrib.auth import authenticate, login, logout
import jwt
import requests
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users import serializers
from users.models import User


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user, data=request.data, partial=True, )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Users(APIView):
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError

        serializer = serializers.PrivateUserSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PublicUser(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not old_password or not new_password:
            return ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogIn(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            raise ParseError

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"ok": "Welcome"})
        else:
            return Response(
                {"error": "wrong password"},
                status=status.HTTP_400_BAD_REQUEST
            )


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "Bye"})


class JWTLogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})
        else:
            return Response({"error": "wrong password"})


class GitHubLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                f"https://github.com/login/oauth/access_token?"
                f"code={code}&client_id={settings.GH_CLIENT_ID}&"
                f"client_secret={settings.GH_SECRET_KEY}",
                headers={"Accept": "application/json"},
            )
            access_token = access_token.json().get('access_token')
            user_data = requests.get(
                "https://api.github.com/user",
                headers={"Authorization": f"Bearer {access_token}",
                         "Accept": "application/json",
                         },
            )
            user_data = user_data.json()
            user_emails = requests.get(
                "https://api.github.com/user/emails",
                headers={"Authorization": f"Bearer {access_token}",
                         "Accept": "application/json",
                         },
            )
            user_emails = user_emails.json()
            # print("user_emails1 : ", user_emails)
            # testemail = user_emails[1]['email'] + "1""1"
            # print("user_data", user_data)
            # return Response()
            # username = user_data.get('login') + "1",
            # email = user_emails[1]['email'],
            # name = user_data.get('name') + "1",
            # avatar = user_data.get('avatar_url'),
            # print(username, email, name, avatar)
            # return Response()

            try:
                user = User.objects.get(email=user_emails[1]['email'])
                print("user_emails2", user)
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                # pass
                user = User.objects.create(
                    username=user_data.get('login'),
                    email=user_emails[1]['email'],
                    name=user_data.get('login'),
                    avatar=user_data.get('avatar_url'),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class KakaoLogin(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            print("kacod", code)
            access_token = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data={
                    "grant_type": "authorization_code",
                    "client_id": "c2d2fc16a7e706d9736a0f3a418c4513",
                    "redirect_uri": "https://airbnb-frontend-yzk4.onrender.com/social/kakao",

                    "code": code,
                }
            )
            access_token = access_token.json().get("access_token")
            admin_key = "1b58d63ea91d42e8626fbe5de23984f8"
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer ${access_token}",
                    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                }

            )
            user_data = user_data.json()
            kakao_account = user_data.get('kakao_account')
            profile = kakao_account.get('profile')

            try:
                user = User.objects.get(email=kakao_account.get('email'))
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    email=kakao_account.get('email'),
                    username=profile.get('nickname'),
                    name=profile.get('nickname'),
                    avatar=profile.get('profile_image_url'),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SignUp(APIView):
    def post(self, request):
        print("signup page test")
        try:
            name = request.data.get('name')
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password1')
            print("Collect Data ", name, username, email, password)
            try:
                user = User.objects.get(email=email)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    email=email,
                    username=username,
                    password=password,
                    name=name,
                    avatar="/",
                )
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
