from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_jwt.settings import api_settings
from django.urls import reverse
from django.db import models
import base64
from django.conf import settings
import os
import random
import io
from PIL import Image
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser
import json


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()

def random_base64():
    file=io.BytesIO()
    image=Image.new("RGBA",size=(100,100),color=(155,0,0))
    image.save(file,'png')
    file.name='test.png'
    file.seek(0)
    return file

img_path = random_base64()



    # with open(img_path,"rb") as img_file:
    #     image=base64.b64encode(img_file.read()) 
class SignupSerializerTestCase(TestCase):
      
    def setUp(self):
        self.client = APIClient()
        self.valid_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            # 'avatar': img_path
        }
        self.invalid_password_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password',
            # 'avatar': img_path
        }
        self.invalid_password_data_email= {
            'username': 'testuser',
            'email': 'testexample.com',
            'password': 'passwordasas',
            # 'avatar': img_path
        }
        self.invalid_data_username_exist = {
            'username': 'testuser',
            'email': 'test123@example.com',
            'password': 'testpassword',
            # 'avatar': img_path
        }

    def test_valid_data(self):
        self.invalid_password_data
        response = self.client.post(reverse('signup'), self.valid_data, format='json')
        print(response.content, "****")
        self.assertEqual(response.status_code, 201)
        print(response.content,'#$%1\n')
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpassword'))

    def test_invalid_password(self):
        response = self.client.post(reverse('signup'), self.invalid_password_data, format='json')
        print(response.content,'#$%3\n')        
        self.assertEqual(response.status_code, 400)
        self.assertEquals(json.loads(response.content)['password'], ["['This password is too common.']"])
    
    def test_invalid_email_fromat(self):
        response = self.client.post(reverse('signup'),self.invalid_password_data_email, format='json')
        self.assertEqual(response.status_code, 400)
        print("didipaeizo?",response.content) 
        self.assertEquals(json.loads(response.content),{'email': ['Enter a valid email address.']})
# .......................................................................................................................................................................
    # def test_invalid_username_exist(self):
    #     response = self.client.post(reverse('signup'),self.invalid_data_username_exist , format='json')
    #     self.assertEqual(response.status_code, 400)
    #     print("wenevervewalk?",response.content) 
    #     self.assertEquals(json.loads(response.content),{'email': ['user with this username already exists.']})




    # def test_invalid_username_exist(self):
    #     response = self.client.post(reverse('signup'), self.invalid_data_username_exist, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertDictEqual(
    #         response.json(),
    #         {'username': ['user with this username already exists.']}
    #     )
# .......................................................................................................................................................................


class LoginTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            #avatar='avatars/default.jpg',
            is_active=True
        )

    def test_login_valid(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_invalid_login_wrongpass(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)    
    
    def test_invalid_login_username(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'userhi',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)   
        response_data = json.loads(response.content.decode('utf-8'))
        print("chetoricriss",response_data)
        self.assertEqual(response_data, {'detail': 'No active account found with the given credentials'})







from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import CustomUser

# class EditProfileTest(TestCase):
#     def setUp(self):
#         self.user = CustomUser.objects.create_user(
#             username='testuser',
#             email='testuser@example.com',
#             password='testpassword',
#             #avatar='avatars/default.jpg',
#             is_active=True
#         )
#         self.client = APIClient()

#     def test_valid_editprofile(self):
#         url = reverse('editprofile')
#         self.client.force_authenticate(user=self.user)
#         new_username = 'newusername'
#         new_password = 'newpassword'
#         #new_avatar = '../avatars/avatars/new_avatar.jpg'
#         data = {
#             'username': new_username,
#             'password': new_password,
#             #'avatar': new_avatar
#         }
#         response = self.client.put(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.username, new_username)
#         self.assertTrue(self.user.check_password(new_password))
#         #self.assertEqual(self.user.avatar.path, new_avatar)

#     def test_invalid_edit_profile(self):
#         url = reverse('editprofile')
#         self.client.force_authenticate(user=self.user)
#         new_username = 'newusername'
#         # Password is too short (less than 8 characters)
#         new_password = 'short'
#         # Invalid avatar path
#         #new_avatar = '/invalid/path/to/avatar.jpg'
#         data = {
#             'username': new_username,
#             'password': new_password,
#         #    'avatar': new_avatar
#         }
#         response = self.client.put(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         # Check that the user's fields haven't been updated
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.username, 'testuser')
#         self.assertTrue(self.user.check_password('testpassword'))
#         #self.assertEqual(self.user.avatar.path, 'avatars/default.jpg')






#........................................................................................................................
# class EditProfileTest(TestCase):
#     def setUp(self):
#         self.user = CustomUser.objects.create_user(
#             username='testuser',
#             email='testuser@example.com',
#             password='testpassword',
#             #avatar='avatars/default.jpg',
#             is_active=True
#         )
#         # self.client.force_authenticate(user=self.user)
#         self.client = APIClient()
#     def test_edit_profile(self):
#         url = reverse('editprofile', args=[self.user.id])
#         new_username = 'newusername'
#         new_password = 'newpassword123'
#         data = {
#             'username': new_username,
#             'password': new_password,
#         }
#         response = self.client.put(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.username, new_username)
#         self.assertTrue(self.user.check_password(new_password))
    
    
    
    # def test_invalid_edit_profile(self):
    #     url = reverse('editprofile', args=[self.user.id])
    #     self.client.force_authenticate(user=self.user)
    #     new_username = 'newusername'
    #     # Password is too short (less than 8 characters)
    #     new_password = 'short'
    #     # Invalid avatar path
    #     #new_avatar = '/invalid/path/to/avatar.jpg'
    #     data = {
    #         'username': new_username,
    #         'password': new_password,
    #     #    'avatar': new_avatar
    #     }
    #     response = self.client.put(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     print("statuscode",response.status_code)
    #     print("responses",response.content)
    #     # Check that the user's fields haven't been updated
    #     self.user.refresh_from_db()
    #     self.assertEqual(self.user.username, 'testuser')
    #     self.assertTrue(self.user.check_password('testpassword'))
    #     #self.assertEqual(self.user.avatar.path, 'avatars/default.jpg')
    #...................................................................................................................................






class ResetPasswordViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url ="/auth/users/reset_password/"

    def test_reset_password_valid_email(self):
        user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='testpassword',is_active=1)
        data = {'email': 'test@example.com'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data,None )
        print(response.content,"email_evalid")

    def test_reset_password_dosnt_exist_email(self):
        data = {'email': 'invalid@example.com'}
        response = self.client.post(self.url, data, format='json')
        #self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        #self.assertEqual(response.content.bytes,'User with given email does not exist.')
        #print("hello guys",response.data)
        #print(response.content,"email_not_invalid")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content.decode('utf-8'))
        print("helloworld",response_data)
        self.assertEqual(response_data[0], 'User with given email does not exist.')
    
    def test_reset_password_invalid_email(self):
        data = {'email': 'invalidexample.com'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content.decode('utf-8'))
        print("higuys",response_data)
        self.assertEqual(response_data, {'email': ['Enter a valid email address.']})



        


    # def test_forgot_password_serializer_invalid(self):
    #     data = {'email': 'invalid'}
    #     serializer = ForgotPasswordSerializer(data=data)
    #     self.assertFalse(serializer.is_valid())
