import json

from django.http import HttpResponse
from django.shortcuts import render
from django.template.defaulttags import csrf_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.decorators import protected_resource
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from CustomUser.Service import sign_up_service, login_service
from CustomUser.TokenSerializer import CustomTokenSerializer


# Create your views here.



@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = sign_up_service(data)
            if user is None:
                return HttpResponse(
                    json.dumps({'error': 'User already exists'}),
                    content_type='application/json',
                    status=400
                )
            return HttpResponse(
                json.dumps({'message': 'User created successfully'}),
                content_type='application/json',
                status=201
            )
        except Exception as e:
            return HttpResponse(
                json.dumps({'error': str(e)}),
                content_type='application/json',
                status=500
            )


@method_decorator(csrf_exempt, name='dispatch')
class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        token = login_service(data['email'], data['password'])
        if token is None:
            return HttpResponse(
                json.dumps({'error': 'Invalid credentials'}),
                content_type='application/json',
                status=401
            )
        return HttpResponse(
            json.dumps({'token': token}),
            content_type='application/json',
            status=200
        )
    else:
        return HttpResponse(
            json.dumps({'error': 'Method not allowed'}),
            content_type='application/json',
            status=405
        )


@protected_resource()
def hello_world(request):
    return HttpResponse(
        json.dumps({'message': 'Hello World'}),
        content_type='application/json',
        status=200
    )