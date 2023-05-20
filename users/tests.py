from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()

class SignupSerializerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'avatar': None
        }
        self.invalid_password_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password',
            'avatar': None
        }

    def test_valid_data(self):
        response = self.client.post('/api/signup/', self.valid_data, format='json')
        self.assertEqual(response.status_code, 201)

        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpassword'))

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

        response = self.client.get('/api/user/', **auth_header)
        self.assertEqual(response.status_code, 200)
#Continuation of the previous test code for `SignupSerializer`:

        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['avatar'], None)

    def test_invalid_password(self):
        response = self.client.post('/api/signup/', self.invalid_password_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['password'][0], 'This password is too common.')

    def test_missing_required_fields(self):
        response = self.client.post('/api/signup/', {'username': 'testuser'}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['email'][0], 'This field is required.')
        self.assertEqual(response.data['password'][0], 'This field is required.')

    def test_login_with_valid_credentials(self):
        # Create a user with valid credentials
        response = self.client.post('/api/signup/', self.valid_data, format='json')
        self.assertEqual(response.status_code, 201)

        # Try to login with the valid credentials
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post('/api/login/', login_data, format='json')
        self.assertEqual(response.status_code, 200)

        # Check if the response contains a JWT token
        self.assertIn('token', response.data)

        #Continuation of the test code for `SignupSerializer`:

        # Use the JWT token to make a request to the protected endpoint
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {response.data["token"]}'}
        response = self.client.get('/api/user/', **auth_header)
        self.assertEqual(response.status_code, 200)

        # Check if the response data is correct
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['avatar'], None)

    def test_login_with_invalid_credentials(self):
        # Create a user with valid credentials
        response = self.client.post('/api/signup/', self.valid_data, format='json')
        self.assertEqual(response.status_code, 201)

        # Try to login with invalid password
        login_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post('/api/login/', login_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'][0], 'Unable to log in with provided credentials.')

        # Try to login with invalid username
        login_data = {
            'username': 'wrongusername',
            'password': 'testpassword'
        }
        response = self.client.post('/api/login/', login_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'][0], 'Unable to log in with provided credentials.')