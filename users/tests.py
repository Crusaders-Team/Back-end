from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_jwt.settings import api_settings
from django.urls import reverse
from django.db import models

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()

class SignupSerializerTestCase(TestCase):
    image=models.ImageField('/avatars/avatars/default.png')
    def setUp(self):
        self.client = APIClient()
        self.valid_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'avatar': '/avatars/avatars/default.png'
        }
        self.invalid_password_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password',
            'avatar': '/avatars/avatars/default.png'
        }

    def test_valid_data(self):
        self.invalid_password_data
        response = self.client.post(reverse('signup'), self.valid_data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, 201)
        print(response.content,'#$%1\n')
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@example.com')
        # self.assertTrue(user.check_password('testpassword'))

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

        response = self.client.get(reverse('user'), **auth_header)
        print(response.content,'#$%2\n')
        self.assertEqual(response.status_code, 200)
# #Continuation of the previous test code for `SignupSerializer`:

        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['avatar'], '/avatars/avatars/default.png')

    def test_invalid_password(self):
        response = self.client.post(reverse('signup'), self.invalid_password_data, format='json')
        print(response.content,'#$%3\n')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['password'], 'This password is too common.')

    def test_missing_required_fields(self):
        response = self.client.post(reverse('signup'), {'username': 'testuser'}, format='json')
        print(response.content,'#$%4\n')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['email'], 'This field is required.')
        self.assertEqual(response.data['password'], 'This field is required.')

    def test_login_with_valid_credentials(self):
        # Create a user with valid credentials
        response = self.client.post(reverse('signup'), self.valid_data, format='json')
        print(response.content,'#$%5\n')
        self.assertEqual(response.status_code, 201)

        # Try to login with the valid credentials
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(reverse('login'), login_data, format='json')
        self.assertEqual(response.status_code, 200)

        # Check if the response contains a JWT token
        self.assertIn('token', response.data)

        #Continuation of the test code for `SignupSerializer`:

        # Use the JWT token to make a request to the protected endpoint
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {response.data["token"]}'}
        response = self.client.get('/api/user/', **auth_header)
        print(response.content,'#$%6\n')
        self.assertEqual(response.status_code, 200)

        # Check if the response data is correct
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['avatar'], '/avatars/avatars/default.png')

    def test_login_with_invalid_credentials(self):
        # Create a user with valid credentials
        response = self.client.post(reverse('signup'), self.valid_data, format='json')
        self.assertEqual(response.status_code, 201)
        print(response.content)
        # Try to login with invalid password
        login_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('login'), login_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'], 'Unable to log in with provided credentials.')

        # Try to login with invalid username
        login_data = {
            'username': 'wrongusername',
            'password': 'testpassword'
        }
        response = self.client.post(reverse('login'), login_data, format='json')
        print(response.content,'#$%7\n')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'], 'Unable to log in with provided credentials.')
        
        
# test_valid_data - This test case checks if the serializer can create a user with valid data, and if the JWT authentication works properly. It is the same as the test_valid_data test case from the previous test code.

# test_invalid_password - This test case checks if the serializer raises an error when the password is too weak. It is the same as the test_invalid_password test case from the previous test code.

# test_missing_required_fields - This test case checks if the serializer raises an error when required fields are missing. It is the same as the test_missing_required_fields test case from the previous test code.

# test_login_with_valid_credentials - This test case checks if the login endpoint works properly with valid credentials. It first creates a user with valid credentials using the valid_data, then it tries to log in with the same credentials using the /api/login/ endpoint. It checks if the response contains a JWT token, and uses the token to make a GET request to the protected /api/user/ endpoint. It checks if the response status is 200 and the data is correct.

# test_login_with_invalid_credentials - This test case checks if the login endpoint returns the correct error message when provided with invalid credentials. It creates a user with valid credentials using the valid_data, then it tries to log in with invalid credentials (wrong password and wrong username) using the /api/login/ endpoint. It checks if the response status is 400 and the response data contains the correct error message