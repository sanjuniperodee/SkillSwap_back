from django.core import serializers

import json

from datetime import datetime, timedelta
from django.utils import timezone
import jwt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer
from .models import *

class GetJobs(APIView):
    # permission_classes = [AllowAny]

    def get(self, request):
        data = serializers.serialize('json', Job.objects.all())
        return Response(json.loads(data), status=200)


class GetJob(APIView):
    # permission_classes = [AllowAny]

    def get(self, request, id):
        data = serializers.serialize('json', Job.objects.filter(pk=id))
        print(json.loads(data)[0])
        return Response(json.loads(data)[0], status=200)




class EnrollView(APIView):
    def post(self, request, userPK, jobPK):
        print(userPK, jobPK)
        enroll = Enrolls(user=User.objects.get(pk=userPK), course=Job.objects.get(pk=jobPK), enrolled_date=datetime.now())
        enroll.save()
        return Response({}, status=200)


class GetCoursesByUserView(APIView):
    def get(self, request, userPK):
        courses = []
        for enroll in Enrolls.objects.filter(user=User.objects.get(pk=userPK)):
            enroll.course.time = enroll.enrolled_date
            courses.append(enroll.course)
        data = serializers.serialize('json', courses)
        return Response(json.loads(data), status=200)

class CheckUserView(APIView):

    def post(self, request):
        phone_number = request.data['phone_number']
        email = request.data['email']

        if len(User.objects.filter(phone_number=phone_number)) + len(User.objects.filter(email=email)) == 0:
            return Response({}, status=200)
        return Response({}, status=400)


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = request.data['email']
            user = User.objects.filter(email=email).first()
            payload = {
                'id': user.id,
                'password': user.password,
                'exp': datetime.utcnow() + timedelta(hours=24),
                'iat': datetime.utcnow()
            }
            token = jwt.encode(payload, 'sercet', algorithm='HS256').encode('utf-8')

            # Set the JWT token in the response
            response = Response()
            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {
                'token': token
            }
            return response
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    def post(self, request):
        user = User.objects.filter(email=request.data['email']).first()
        if user is None:
            raise AuthenticationFailed("user not found")
        if not user.check_password(request.data['password']):
            raise AuthenticationFailed("incorrect password")
        payload = {
            'id': user.id,
            'password': user.password,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, 'sercet', algorithm='HS256').encode('utf-8')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'token': token
        }
        return response


class UserView(APIView):
    def post(self, request):
        token = request.data.get('jwt')
        print(token)
        if not token:
            raise AuthenticationFailed("Failed to authorize")
        try:
            payload = jwt.decode(token, 'sercet', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Authorization is expired")
        user = User.objects.filter(id=payload['id'], password=payload['password']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)