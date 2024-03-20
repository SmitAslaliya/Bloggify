from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from post import postpermission
from post.models import Post,PostPermission
from django.core.mail import EmailMessage, get_connection
from django.conf import settings


class UserCreateView(APIView):
    def post(self,request):
        data = request.data
        try:
            username = data['username']
            email = data['email']
            password = data['password']
            
        except Exception as key:
            return Response({str(key):['field is required']})
        
        if User.objects.filter(username=username).exists():
            return Response({'username':['user already exists']})
        
        user = User.objects.create(email=email,username=username)
        user.set_password(password)
        user.save()
        PostPermission.objects.create(user=user)
        
        with get_connection(host=settings.EMAIL_HOST, 
                            port=settings.EMAIL_PORT,  
                            username=settings.EMAIL_HOST_USER,  
                            password=settings.EMAIL_HOST_PASSWORD,  
                            use_tls=settings.EMAIL_USE_TLS) as connection:  
            recipient_list = ['smitaslaliya@gmail.com']  
            subject = 'Test Email' 
            email_from = settings.EMAIL_HOST_USER  
            message = "Hello How are? Khana kha ke jana ha!" 
            EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()
        
        res = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            }
        return Response ({'msg':'user created','user':res})
    
class UserLoginView(APIView):
    def post(self,request):
        data = request.data
        user_name = request.data['username']
        password = data['password']
        
        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            return Response('user already exist!')
        
        if authenticate(username=user_name,password=password):
            token , created = Token.objects.update_or_create(user=user)
            if not created:
                token.delete()
                token = Token.objects.create(user=user)
                
            rsp = {
                "username" : user.username,
                "email" : user.email,
                "usertype" : 'admin',
                'token' : str(token), 
                }
            return Response(rsp, status=200)
        return Response({"message": "Invalid Credientials"}, status=status.HTTP_401_UNAUTHORIZED)
    
class UserLogoutView(APIView):
    authentication_classes = (TokenAuthentication, )
    def delete(self, request):
        try:
            Token.objects.get(user=request.user).delete()
            return Response({"message":"user logout"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"message": "user already logout"}, status=status.HTTP_404_NOT_FOUND)
    
class UserChangePassword(APIView):
    authentication_classes = (TokenAuthentication, )
    def post(self,request):
        
        data = request.data
        breakpoint()
        current_password = request.data['current_password']
        password1 = data['password1']
        password2 = data['passwprd2']
        
        if authenticate(request.user.username,password=current_password):
            if password1 == password2:
                request.user.set_password(password1)
                request.user.save()
                
                return Response({"message":'user password changed succesful'},status=status.HTTP_200_OK)
            else:
                return Response({'message':"new password are not same"},status=status)
        else:
            return Response({"message":"invalid password"},status=status.HTTP_400_BAD_REQUEST)
        