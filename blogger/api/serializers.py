from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.core.validators import EmailValidator
from django_countries.serializers import CountryFieldMixin

from blogger.models import *


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        exclude = ['id']


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        exclude = ['id']


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        exclude = ['id']


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        exclude = ['id']


class UserSerializer(CountryFieldMixin,serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [ 'password']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ['id']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['id']


class PostSerializer(serializers.ModelSerializer):
    author_title = serializers.CharField(source='author.title')
    author_site_title = serializers.CharField(source='author.site_title')
    author_first_name = serializers.CharField(source='author.first_name')
    author_last_name = serializers.CharField(source='author.last_name')
    author_profile_picture = serializers.CharField(source='author.profile_picture_url')

    class Meta:
        model = Post
        # exclude = ['id']
        fields = "__all__"


class PostViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostView
        exclude = ['id']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['id']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        exclude = ['id']


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        exclude = ['id']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        exclude = ['id']


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        exclude = ['id']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters',
        'password': 'Confirm Password not matching.'
    }

    class Meta:
        model = User
        fields = [
            'title', 'site_title', 'email', 'first_name', 'last_name', 'gender',
            'country', 'industry', 'interest', 'custom_interest', 'goals', 'stage', 'password', 'password2'
        ]

    def validate(self, attrs):
        email = attrs.get('email', '')
        # username = attrs.get('username', '')

        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')

        # valid_email = EmailValidator(message="Email format is is not matching.", code=400)
        # valid_email.validate_email(email)

        # if not username.isalnum():
        #     raise serializers.ValidationError(
        #         self.default_error_messages['username'])

        if not password == password2:
            raise serializers.ValidationError(
                self.default_error_messages['password'])

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')

        return User.objects.create_blogger(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    title = serializers.CharField(read_only=True)
    site_title = serializers.CharField(read_only=True)
    gender = serializers.CharField(read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['id', 'last_login', 'is_superuser', '_id_slug', 'title', 'site_title', 'email', 'first_name', 'last_name', 'about', 'profile_picture', 'gender', 'phone', 'city', 'state', 'zip_postal_code', 'country', 'share_profile', 'show_email_address', 'show_blogs', 'show_followed_sites', 'comment_auto_publish', 'industry_id', 'occupation', 'interest_id', 'custom_interest', 'stage_id', 'custom_stage', 'template_name', 'homepage', 'subscribers', 'blogger', 'staff', 'admin', 'status', 'create_date', 'update_date', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)


        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')

        res = user.__dict__
        res.pop('_state')
        res.pop('password')
        res.pop('backend')

        return res

        return super().validate(attrs)


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    password2 = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'password2', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')

            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            _id_slug = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(_id_slug=_id_slug)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return user
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid',)
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')
