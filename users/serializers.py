from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import CustomUser

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        #fields = ('username','email', 'password', )
        fields = ('username','email', 'password','avatar')
        
    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value
    def create(self, validated_data):
        print(validated_data.get('avatar'))
        if validated_data.get('avatar')==None:
            validated_data['avatar'] = '/avatars/avatars/default.png'
        else:
            user.avatar=validated_data.get('avatar')
        user = User.objects.create(username=validated_data.get('username'), email=validated_data.get('email'))
        user.set_password(validated_data.get('password'))
        user.save()
        return user
    
class EditProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(max_length=30, required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'avatar', 'password')

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.username = validated_data.get('username', instance.username)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.save()
        return instance  

        
# class EditProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         #fields = ('username','email', 'password', )
#         fields = ('username','avatar','password')
# #    User.password.has_default=True
#     def validate_password(self, value):
#         try:
#             validate_password(value)
#         except ValidationError as e:
#             raise serializers.ValidationError(str(e))
#         return value
    

#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value

    def validate(self, data):
        if data.get('new_password') != data.get('confirm_new_password'):
            raise serializers.ValidationError({'confirm_new_password': ['Passwords must match.']})
        return data
