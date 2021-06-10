from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
# from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect, JsonResponse
import os, json

from blogger.models import *
from .serializers import *
from .renderers import UserRenderer
from blogger.utils import Util, FieldMaps
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist, ValidationError


class ModelViewSetWithIDSlugLookup(ModelViewSet):
    lookup_field = '_id_slug'
    lookup_value_regex = '[-\w]+'


class InterestViewSet(ModelViewSetWithIDSlugLookup):
    serializer_class = InterestSerializer
    queryset = Interest.objects.all()


class IndustryViewSet(ModelViewSetWithIDSlugLookup):
    serializer_class = IndustrySerializer
    queryset = Industry.objects.all()


class GoalViewSet(ModelViewSetWithIDSlugLookup):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()


class StageViewSet(ModelViewSetWithIDSlugLookup):
    serializer_class = StageSerializer
    queryset = Stage.objects.all()


class UserViewSet(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class TagViewSet(ModelViewSetWithIDSlugLookup):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class CategoryViewSet(ModelViewSetWithIDSlugLookup):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class PostViewSet(ModelViewSetWithIDSlugLookup):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostViewViewSet(ModelViewSetWithIDSlugLookup):
    serializer_class = PostViewSerializer
    queryset = PostView.objects.all()


class CommentViewSet(ModelViewSetWithIDSlugLookup):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class LikeViewSet(ModelViewSetWithIDSlugLookup):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()


class FavouriteViewSet(ModelViewSetWithIDSlugLookup):
    serializer_class = FavouriteSerializer
    queryset = Favourite.objects.all()


class ContactViewSet(ModelViewSetWithIDSlugLookup):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()


class NewsletterViewSet(ModelViewSetWithIDSlugLookup):
    serializer_class = NewsletterSerializer
    queryset = NewsletterSubscriber.objects.all()


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data

        if user.get('interest'):
            user['interest'] = Interest.objects.get(_id_slug=user['interest']).id

        if user.get('stage'):
            user['stage'] = Stage.objects.get(_id_slug=user['stage']).id

        user['industry'] = Industry.objects.get(_id_slug=user['industry']).id

        goals = []
        for goal in user['goals']:
            goals.append(Goal.objects.get(_id_slug=goal).id)

        user['goals'] = goals

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        # user = User.objects.get(email=user_data['email'])
        # token = RefreshToken.for_user(user).access_token
        # current_site = get_current_site(request).domain
        # relativeLink = reverse('email-verify')
        # absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
        # email_body = 'Hi ' + user.username + \
        #              ' Use the link below to verify your email \n' + absurl
        # data = {'email_body': email_body, 'to_email': user.email,
        #         'email_subject': 'Verify your email'}
        # Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(_id_slug=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://' + current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                         absurl + "?redirect_url=" + redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            _id_slug = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(_id_slug=_id_slug)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url + '?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(
                    redirect_url + '?token_valid=True&message=Credentials Valid&uidb64=' + uidb64 + '&token=' + token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url + '?token_valid=False')

            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def model_field_map(request):
    try:
        payload = json.loads(request.body)

        mapped_fields = {}

        for model in payload['models']:
            mapped_fields[model] = getattr(FieldMaps(), model)()

        return JsonResponse(
            mapped_fields,
            safe=False,
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return JsonResponse(
            {'error': 'Something terrible went wrong, ' + str(e)},
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def comments_by_post(request, id_):
    try:
        queryset = list(Comment.objects.filter(post__id=id_).all().values())

        return JsonResponse(
            queryset,
            safe=False,
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return JsonResponse(
            {'error': 'Something terrible went wrong, ' + str(e)},
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
def models_statistics(request):
    try:
        payload = json.loads(request.body)

        mapped_stats = {}

        models_map = {
            'interests': Interest,
            'industries': Industry,
            'goals': Goal,
            'stages': Stage,
            'users': User,
            'tags': Tag,
            'categories': Category,
            'posts': Post,
            'postviews': PostView,
            'comments': Comment,
            'likes': Like,
            'favourites': Favourite,
            'newsletters': NewsletterSubscriber,
            'contacts': Contact
        }

        models = payload['models']
        months = payload['months']

        for model in models:
            result = []
            qsets = list(models_map[model].objects.all()
                                    .values_list('create_date__year', 'create_date__month')
                                    .annotate(Count('pk'))
                                    .order_by('create_date__year', 'create_date__month'))

            for q in qsets:
                if [q[0], q[1]-1] in months:
                    result.append(q)

            mapped_stats[model] = result

        return JsonResponse(
            mapped_stats,
            safe=False,
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return JsonResponse(
            {'error': 'Something terrible went wrong, ' + str(e)},
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def get_about_page(request):
    try:
        page = list(AboutPage.objects.all().values())

        return JsonResponse(
            page,
            safe=False,
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return JsonResponse(
            {'error': 'Something terrible went wrong, ' + str(e)},
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
def update_about_page(request):
    try:
        payload = json.loads(request.body)
        page = AboutPage.objects.first()#.update(**payload)
        page.page_title = payload['page_title']
        page.page_head = payload['page_head']
        page.page_main = payload['page_main']
        page.page_footer = payload['page_footer']
        page.save()

        return JsonResponse(
            payload,
            safe=False,
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return JsonResponse(
            {'error': 'Something terrible went wrong, ' + str(e)},
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def get_contact_page(request):
    try:
        page = list(ContactPage.objects.all().values())

        return JsonResponse(
            page,
            safe=False,
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return JsonResponse(
            {'error': 'Something terrible went wrong, ' + str(e)},
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
def update_contact_page(request):
    try:
        payload = json.loads(request.body)
        page = ContactPage.objects.first()#.update(**payload)
        page.page_title = payload['page_title']
        page.page_head = payload['page_head']
        page.page_main = payload['page_main']
        page.page_footer = payload['page_footer']
        page.save()

        return JsonResponse(
            payload,
            safe=False,
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return JsonResponse(
            {'error': 'Something terrible went wrong, ' + str(e)},
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
def post_viewed(request):
    try:
        payload = json.loads(request.body)
        post = Post.objects.get(id=payload['post'])
        viewed_by = User.objects.get(id=payload['viewed_by'])
        try:
            postview = PostView.objects.get(post=post, viewed_by=viewed_by)
            postview.view_count = postview.view_count + 1
            postview.save()

        except ObjectDoesNotExist as e:
            postview = PostView.objects.create(post=post, viewed_by=viewed_by)

        post.viewed_count = post.viewed_count + 1
        post.save()

        return JsonResponse(
            {
                'post': post.id,
                'total_view': post.viewed_count,
                'viewed_by': postview.viewed_by.id,
                'total_viewed_by_user': postview.view_count
            },
            safe=False,
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return JsonResponse(
            {'error': 'Something terrible went wrong, ' + str(e)},
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def new_like_and_list(request):
    try:
        payload = json.loads(request.body)

        post = Post.objects.get(id=payload['post'])

        if payload.get('new', False):
            like_by = User.objects.get(id=payload['like_by'])

            try:
                res = Like.objects.get(post=post, like_by=like_by)
            except ObjectDoesNotExist as e:
                res = Like.objects.create(post=post, like_by=like_by)
                post.like_count = post.like_count + 1
                post.save()

            result = {
                'post': post.id,
                'like_by': like_by.id,
                'like_count': post.like_count
            }

        else:
            result = list(Like.objects.filter(post__id=payload['post']).all().values())
            result['like_count'] = post.like_count

        return JsonResponse(
            result,
            safe=False,
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return JsonResponse(
            {'error': 'Something terrible went wrong, ' + str(e)},
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def new_heart_and_list(request):
    try:
        payload = json.loads(request.body)

        post = Post.objects.get(id=payload['post'])

        if payload.get('new', False):
            heart_by = User.objects.get(id=payload['heart_by'])

            try:
                res = Favourite.objects.get(post=post, favourite_by=heart_by)
            except ObjectDoesNotExist as e:
                res = Favourite.objects.create(post=post, favourite_by=heart_by)
                post.favourite_count = post.favourite_count + 1
                post.save()

            result = {
                'post': post.id,
                'heart_by': heart_by.id,
                'favourite_count': post.favourite_count
            }

        else:
            result = list(Favourite.objects.filter(post=post).all().values())
            result['favourite_count'] = post.favourite_count

        return JsonResponse(
            result,
            safe=False,
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return JsonResponse(
            {'error': 'Something terrible went wrong, ' + str(e)},
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def user_profile_update(request):
    try:
        payload = json.loads(request.body)

        user = User.objects.get(id=payload.pop('id'), _id_slug=payload.pop('_id_slug'))

        for key, value in payload.items():
            setattr(user, key, value)

        user.save()

        result = user.__dict__
        result.pop('_state')
        result.pop('password')
        result['profile_picture'] = result['profile_picture'].url

        return JsonResponse(
            result,
            safe=False,
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return JsonResponse(
            {'error': 'Something terrible went wrong, ' + str(e)},
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def blog_meta_info(request):
    try:

        result = json.loads(open('media/page_data.json', 'r').read())

        return JsonResponse(
            result,
            safe=False,
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return JsonResponse(
            {'error': 'Something terrible went wrong, ' + str(e)},
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def blog_in_industy(request):
    try:

        payload = json.loads(request.body)

        bloggers = User.objects.filter(
                            industry__title=payload['industry_name'].replace('-', ' ')).all()

        all_posts = []

        for blogger in bloggers:
            posts = list(Post.objects.filter(author=blogger).all().values())

            if posts:
                all_posts += posts

        return JsonResponse(
            all_posts,
            safe=False,
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return JsonResponse(
            {'error': 'Something terrible went wrong, ' + str(e)},
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def blog_with_interest(request):
    try:

        payload = json.loads(request.body)

        bloggers = User.objects.filter(
                        interest__title=payload['interest_name'].replace('-', ' ')).all()

        all_posts = []

        for blogger in bloggers:
            posts = list(Post.objects.filter(author=blogger).all().values())

            if posts:
                all_posts += posts

        return JsonResponse(
            all_posts,
            safe=False,
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return JsonResponse(
            {'error': 'Something terrible went wrong, ' + str(e)},
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def popular_blog(request):
    try:
        posts = list(Post.objects.all().order_by(
                                        '-viewed_count', '-comment_count',
                                        '-favourite_count', '-like_count'
                                    ).values(
                                        'id', '_id_slug',
                                        'title', 'meta_title',
                                        'author__first_name',
                                        'author__last_name', 'author__title',
                                        'author__profile_picture',
                                        'summary', 'create_date'
                                    ))

        return JsonResponse(
            posts,
            safe=False,
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return JsonResponse(
            {'error': 'Something terrible went wrong, ' + str(e)},
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
