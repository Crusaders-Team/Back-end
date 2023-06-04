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

class SignupSerializerTestCase(TestCase):
    # with open(img_path,"rb") as img_file:
    #     image=base64.b64encode(img_file.read())
           
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

    def test_valid_data(self):
        self.invalid_password_data
        response = self.client.post(reverse('signup'), self.valid_data, format='json')
        print(response.content, "****")
        self.assertEqual(response.status_code, 201)
        print(response.content,'#$%1\n')
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpassword'))

#         payload = jwt_payload_handler(user)
#         token = jwt_encode_handler(payload)
#         auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

#         response = self.client.get(reverse('user'), **auth_header)
#         print(response.content,'#$%2\n')
#         self.assertEqual(response.status_code, 200)
# # #Continuation of the previous test code for `SignupSerializer`:

#         self.assertEqual(response.data['username'], 'testuser')
#         self.assertEqual(response.data['email'], 'test@example.com')
#         self.assertEqual(response.data['avatar'], '/avatars/avatars/default.png')

    def test_invalid_password(self):
        response = self.client.post(reverse('signup'), self.invalid_password_data, format='json')
        print(response.content,'#$%3\n')
        
        # print(json.loads(response.content)['password'], "###########")
        
        self.assertEqual(response.status_code, 400)
        self.assertEquals(json.loads(response.content)['password'], ["['This password is too common.']"])

#     def test_missing_required_fields(self):
#         response = self.client.post(reverse('signup'), {'username': 'testuser'}, format='json')
#         print(response.content,'#$%4\n')
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.data['email'], 'This field is required.')
#         self.assertEqual(response.data['password'], 'This field is required.')

#     def test_login_with_valid_credentials(self):
#         # Create a user with valid credentials
#         response = self.client.post(reverse('signup'), self.valid_data, format='json')
#         print(response.content,'#$%5\n')
#         self.assertEqual(response.status_code, 201)

#         # Try to login with the valid credentials
#         login_data = {
#             'username': 'testuser',
#             'password': 'testpassword'
#         }
#         response = self.client.post(reverse('login'), login_data, format='json')
#         self.assertEqual(response.status_code, 200)

#         # Check if the response contains a JWT token
#         self.assertIn('token', response.data)

#         #Continuation of the test code for `SignupSerializer`:

#         # Use the JWT token to make a request to the protected endpoint
#         auth_header = {'HTTP_AUTHORIZATION': f'Bearer {response.data["token"]}'}
#         response = self.client.get('/api/user/', **auth_header)
#         print(response.content,'#$%6\n')
#         self.assertEqual(response.status_code, 200)

#         # Check if the response data is correct
#         self.assertEqual(response.data['username'], 'testuser')
#         self.assertEqual(response.data['email'], 'test@example.com')
#         self.assertEqual(response.data['avatar'], '/avatars/avatars/default.png')

#     def test_login_with_invalid_credentials(self):
#         # Create a user with valid credentials
#         response = self.client.post(reverse('signup'), self.valid_data, format='json')
#         self.assertEqual(response.status_code, 201)
#         print(response.content)
#         # Try to login with invalid password
#         login_data = {
#             'username': 'testuser',
#             'password': 'wrongpassword'
#         }
#         response = self.client.post(reverse('login'), login_data, format='json')
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.data['non_field_errors'], 'Unable to log in with provided credentials.')

#         # Try to login with invalid username
#         login_data = {
#             'username': 'wrongusername',
#             'password': 'testpassword'
#         }
#         response = self.client.post(reverse('login'), login_data, format='json')
#         print(response.content,'#$%7\n')
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.data['non_field_errors'], 'Unable to log in with provided credentials.')
        
        
# # test_valid_data - This test case checks if the serializer can create a user with valid data, and if the JWT authentication works properly. It is the same as the test_valid_data test case from the previous test code.

# # test_invalid_password - This test case checks if the serializer raises an error when the password is too weak. It is the same as the test_invalid_password test case from the previous test code.

# # test_missing_required_fields - This test case checks if the serializer raises an error when required fields are missing. It is the same as the test_missing_required_fields test case from the previous test code.

# # test_login_with_valid_credentials - This test case checks if the login endpoint works properly with valid credentials. It first creates a user with valid credentials using the valid_data, then it tries to log in with the same credentials using the /api/login/ endpoint. It checks if the response contains a JWT token, and uses the token to make a GET request to the protected /api/user/ endpoint. It checks if the response status is 200 and the data is correct.

# # test_login_with_invalid_credentials - This test case checks if the login endpoint returns the correct error message when provided with invalid credentials. It creates a user with valid credentials using the valid_data, then it tries to log in with invalid credentials (wrong password and wrong username) using the /api/login/ endpoint. It checks if the response status is 400 and the response data contains the correct error message







class LoginTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            #avatar='avatars/default.jpg',
            is_active=True
        )

    def test_login(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_invalid_login(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)    



# class loginSerializerTestCase(TestCase):
#     def setup(self):
#         self.client = APIClient()
#         self.valid_data = {
#             'username': 'testuser',
#             'password': 'testpassword',

#         }
#         self.invalid_password_data_1 = {
#             'username': 'testuser',
#             'password': 'password',
#         }
        
#     def test_valid_data_1(self):
#         self.invalid_password_data_1
#         response = self.client.post(reverse('login'), self.valid_data, format='json')
#         print(response.content, "****")
#         self.assertEqual(response.status_code, 201)
#         print(response.content,'****login2\n')
#         user = User.objects.get(username='testuser')
#         self.assertTrue(user.check_password('testpassword'))
    
    # def test_invalid_password_1(self):
    #     response = self.client.post(reverse('login'), self.invalid_password_data, format='json')
    #     print(response.content,'#$inval\n')        
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEquals(json.loads(response.content)['password'], ["['This password is not correct.']"])



from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import CustomUser






class EditProfileTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            #avatar='avatars/default.jpg',
            is_active=True
        )
        self.client = APIClient()

    def test_valid_editprofile(self):
        url = reverse('editprofile')
        self.client.force_authenticate(user=self.user)
        new_username = 'newusername'
        new_password = 'newpassword'
        #new_avatar = '../avatars/avatars/new_avatar.jpg'
        data = {
            'username': new_username,
            'password': new_password,
            #'avatar': new_avatar
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, new_username)
        self.assertTrue(self.user.check_password(new_password))
        #self.assertEqual(self.user.avatar.path, new_avatar)

    def test_invalid_edit_profile(self):
        url = reverse('editprofile')
        self.client.force_authenticate(user=self.user)
        new_username = 'newusername'
        # Password is too short (less than 8 characters)
        new_password = 'short'
        # Invalid avatar path
        #new_avatar = '/invalid/path/to/avatar.jpg'
        data = {
            'username': new_username,
            'password': new_password,
        #    'avatar': new_avatar
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that the user's fields haven't been updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('testpassword'))
        #self.assertEqual(self.user.avatar.path, 'avatars/default.jpg')


# class editprofiletestcase(TestCase):
#     def setup(self):
#         self.client = APIClient()
#         self.valid_data = {
#             'username': 'testuser',
#             'password': 'testpassword',

#         }
#         self.invalid_password_data = {
#             'username': 'testuser',
#             'password': 'password',
#         }