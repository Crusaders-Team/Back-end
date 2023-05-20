from base64 import urlsafe_b64encode
from django.utils.encoding import force_bytes, force_str


from django.shortcuts import render,redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import JsonResponse
from django.urls import reverse_lazy
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SignupSerializer, ForgotPasswordSerializer, ChangePasswordSerializer, EditProfileSerializer
from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView
from users.models import CustomUser
from django.contrib.auth.hashers import make_password



from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .tokens import account_activation_token
# from django.contrib.auth.views import PasswordChangeView
# from .forms import CustomPasswordChangeForm

# class CustomPasswordChangeView(PasswordChangeView):
#     template_name = 'password_change.html'
#     form_class = CustomPasswordChangeForm
#     success_url = reverse_lazy('password_change_done')

#email verfication

# from django.contrib.auth.views import PasswordResetView
# from django.urls import reverse_lazy
# from .forms import CustomPasswordResetForm
# class CustomPasswordResetView(PasswordResetView):
#     # template_name = 'password_reset.html'
#     form_class = CustomPasswordResetForm
#     success_url = reverse_lazy('password_reset_done')


class EditProfileView(UpdateAPIView):
    serializer_class = EditProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.pop('password', None)
        if password:
            hashed_password = make_password(password)
            self.get_object().password = hashed_password
        self.get_object().username = serializer.validated_data.get('username')
        self.get_object().avatar = serializer.validated_data.get('avatar')
        self.get_object().save()
        return Response(serializer.data)


# class UserEdit(RetrieveUpdateAPIView):
#     # permission_classes=[IsAuthenticated]
#     serializer_class=EditProfileSerializer
#     queryset=CustomUser.objects.all()


class SignupAPIView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = (AllowAny, )

class ForgotPasswordAPIView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.filter(email=email).first()
            if user is not None:
                form = PasswordResetForm({'email': email})
                if form.is_valid():
                    subject = 'Password reset'
                    message = 'Please reset your password by clicking on the following link: {0}'.format(
                        request.build_absolute_uri(reverse_lazy('password_reset_confirm', kwargs={
                            'uidb64': urlsafe_b64encode(force_bytes(user.pk)).decode(),
                            'token': default_token_generator.make_token(user),
                        }))
                    )
                    send_mail(subject, message, 'admin@example.com', [email], fail_silently=False)
                return Response({'detail': 'Password reset email has been sent.'})
            else:
                return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.data.get('old_password')
            if not user.check_password(old_password):
                return Response({'old_password': ['Wrong password.']}, status=status.HTTP_400_BAD_REQUEST)
            new_password = serializer.data.get('new_password')
            confirm_new_password = serializer.data.get('confirm_new_password')
            if new_password != confirm_new_password:
                return Response({'confirm_new_password': ['Passwords must match.']}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({'detail': 'Password has been changed.'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'detail': 'Successfully logged out.'})


# Create your views here.


#/----------------------------------------------------------------#\


# from django.shortcuts import render, redirect
# from .models import User

# def signup(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         avatar = request.FILES.get('avatar')
#         if User.objects.filter(username=username).exists():
#             return render(request, 'signup.html', {'error': 'Username already in use.'})
#         if User.objects.filter(email=email).exists():
#             return render(request, 'signup.html', {'error': 'Email already in use.'})
#         user = User()
#         user.create_user(username, email, password)
#         if avatar:
#             user.avatar = avatar
#             user.save()
#         return redirect('login')
#     return render(request, 'signup.html')

# myapp/views.py (continued)

# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = User.objects.filter(username=username, password=hashlib.sha256(password.encode()).hexdigest()).first()
#         if user:
#             request.session['user_id'] = user.id
#             return redirect('protected-page')
#         else:
#             return render(request, 'login.html', {'error': 'Invalid username or password.'})
#     return render(request, 'login.html')

# myapp/views.py (continued)


# from django.contrib.auth.decorators import login_required

# @login_required
# def protected_page(request):
#     user_id = request.session.get('user_id')
#     user = User.objects.get(id=user_id)
#     return render(request, 'protected.html', {'user': user})



#----------------------------------------------edit  profile-----------------------------------

# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .forms import EditProfileForm

# @login_required
# def edit_profile(request):
#     if request.method == 'POST':
#         form = EditProfileForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             # Save the updated user object with the new values
#             user = form.save(commit=False)
#             user.email = request.user.email  # Make sure email doesn't get changed
#             user.save()
#             messages.success(request, 'Your profile has been updated!')
#             return redirect('profile')
#     else:
#         # Display the edit profile form
#         form = EditProfileForm(instance=request.user)
#     return render(request, 'edit_profile.html', {'form': form})