from .views import *
from rest_framework import routers
from django.urls import re_path

router = routers.SimpleRouter()
router.register(r'interests', InterestViewSet)
router.register(r'industries', IndustryViewSet)
router.register(r'goals', GoalViewSet)
router.register(r'stages', StageViewSet)
router.register(r'tags', TagViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'posts', PostViewSet)
router.register(r'postviews', PostViewViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'favourites', FavouriteViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'newsletters', NewsletterViewSet)

urlpatterns = [
    re_path(r'^meta-info/$', blog_meta_info, name='meta_info'),

    re_path(r'^users/', UserViewSet.as_view(), name='user_list'),

    re_path(r'^model/field-map', model_field_map, name='model_field_map'),
    re_path(r'^model/statistics', models_statistics, name='models_statistics'),

    re_path(r'^signup', RegisterView.as_view(), name='api_signup'),
    re_path(r'^login', LoginAPIView.as_view(), name='api_login'),
    re_path(r'^update-my-profile/', user_profile_update, name='user_profile_update'),
    re_path(r'^logout', LogoutAPIView.as_view(), name='api_logout'),

    re_path(r'^email-verify', VerifyEmail.as_view(), name='email-verify'),

    re_path(r'^request-password-reset', RequestPasswordResetEmail.as_view(), name='request-password-reset'),
    re_path(r'^password-token-check', PasswordTokenCheckAPI.as_view(), name='password-token-check'),
    re_path(r'^set-new-password', SetNewPasswordAPIView.as_view(), name='set-new-password'),

    re_path(r'^comments/post/(?P<id_>\d+)/$', comments_by_post, name='comments_by_post'),

    re_path(r'^industry/posts/$', blog_in_industy, name="blog_in_industry"),
    re_path(r'^interest/posts/$', blog_with_interest, name="blog_with_interest"),
    re_path(r'^posts/popular/', popular_blog, name='popular_blog'),

    re_path(r'^post/view/$', post_viewed, name='post_viewed'),
    re_path(r'^post/like/$', new_like_and_list, name='new_like_and_list'),
    re_path(r'^post/heart/$', new_heart_and_list, name='new_heart_and_list'),

    re_path(r'^pages/about/$', get_about_page, name='get_about_page'),
    re_path(r'^pages/about/update/$', update_about_page, name='update_about_page'),
    re_path(r'^pages/contact/$', get_contact_page, name='get_contact_page'),
    re_path(r'^pages/contact/update/$', update_contact_page, name='update_contact_page'),
]

urlpatterns += router.urls
