from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *
# Register your models here.

admin.site.unregister(Group)

class InterestAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'status', 'create_date')
    list_filter = ('status', 'create_date')
    search_fields  = ('title',)
    readonly_fields = ('_id_slug',)

admin.site.register(Interest, InterestAdmin)


class IndustryAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'status', 'create_date')
    list_filter = ('status', 'create_date')
    search_fields  = ('title',)
    readonly_fields = ('_id_slug',)

admin.site.register(Industry, IndustryAdmin)


class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'status', 'create_date')
    list_filter = ('status', 'create_date')
    search_fields  = ('title',)
    readonly_fields = ('_id_slug',)

admin.site.register(Goal, GoalAdmin)


class StageAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'status', 'create_date')
    list_filter = ('status', 'create_date')
    search_fields  = ('title',)
    readonly_fields = ('_id_slug',)

admin.site.register(Stage, StageAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'meta_title', 'priority', 'status', 'create_date')
    list_filter = ('status', 'create_date')
    search_fields  = ('title', 'meta_title', 'description')
    readonly_fields = ('_id_slug',)

admin.site.register(Tag, TagAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'meta_title', 'parent_category',
        'priority', 'status', 'create_date'
    )
    list_filter = ('status', 'create_date')
    search_fields  = ('title', 'meta_title', 'description')
    readonly_fields = ('_id_slug',)

admin.site.register(Category, CategoryAdmin)


class PostViewAdmin(admin.ModelAdmin):
    list_display = ('post', 'viewed_by', 'view_count', 'create_date',)
    list_filter = ('create_date',)
    readonly_fields = ('_id_slug', 'post', 'viewed_by', 'view_count')

admin.site.register(PostView, PostViewAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post', 'parent_comment', 'published',
        'create_date', 'publish_date'
    )
    list_filter = ('published', 'create_date', 'publish_date')
    search_fields  = ('post', 'parent_comment', 'comment_by', 'content')
    readonly_fields = ('_id_slug', 'post', 'parent_comment', 'comment_by', 'publish_date')

admin.site.register(Comment, CommentAdmin)


class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'like_by', 'create_date')
    list_filter = ('create_date',)
    readonly_fields = ('_id_slug', 'post', 'like_by')

admin.site.register(Like, LikeAdmin)


class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('post', 'favourite_by', 'create_date')
    list_filter = ('create_date',)
    readonly_fields = ('_id_slug', 'post', 'favourite_by')

admin.site.register(Favourite, FavouriteAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'subject', 'create_date')
    list_filter = ('create_date',)
    search_fields  = ('email', 'subject', 'content',)
    readonly_fields = ('_id_slug', 'email')

admin.site.register(Contact, ContactAdmin)


class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'category', 'status', 'create_date')
    list_filter = ('status', 'create_date')
    search_fields  = ('email',)
    readonly_fields = ('_id_slug', 'email')

admin.site.register(NewsletterSubscriber, NewsletterSubscriberAdmin)


class ContactPageModelAdmin(admin.ModelAdmin):
    list_display = ('page_title',)
    readonly_fields = ('_id_slug',)

admin.site.register(ContactPage, ContactPageModelAdmin)


class AboutPageModelAdmin(admin.ModelAdmin):
    list_display = ('page_title',)
    readonly_fields = ('_id_slug',)

admin.site.register(AboutPage, AboutPageModelAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'author', 'parent_post', 'title', 'meta_title',
        'category', 'published', 'viewed_count',
        'favourite_count', 'like_count', 'comment_count'
    )
    list_filter = (
        'published', 'create_date',
        'update_date', 'publish_date', 'category'
    )
    search_fields  = ('title', 'meta_title', 'summary', 'content')
    readonly_fields = (
        '_id_slug', 'author', 'publish_date', 'viewed_count', 
        'favourite_count', 'like_count', 'comment_count', 'parent_post'
    )

admin.site.register(Post, PostAdmin)


class UserAdmin(BaseUserAdmin):

    list_display = (
        'title', 'site_title', 'email', 'first_name', 'last_name', 'gender',
        'share_profile', 'show_email_address',
        'show_blogs', 'show_followed_sites', 'comment_auto_publish',
    )
    list_filter = (
        'create_date', 'update_date', 'gender', 'status'
    )
    search_fields  = (
        'title', 'site_title', 'email',
        'first_name', 'last_name', 'about'
    )
    readonly_fields = (
        'share_profile', 'show_email_address', 'show_blogs',
        'show_followed_sites', 'comment_auto_publish',
        'blogger', 'staff', 'admin', 'status', 'email'
    )

    fieldsets = (
        (None, {
            'fields': (
                'title', 'site_title', 'email', 'first_name', 'last_name' ,
                'about', 'homepage', 'profile_picture'
            )
        }),
        ('Other info', {
            'fields': (
                'industry', 'occupation', 'interest', 'custom_interest',
                'goals', 'stage', 'custom_stage', 'template_name'
            )
        }),
        ('Options', {
            'fields': (
                'share_profile', 'show_email_address', 'show_blogs',
                'show_followed_sites', 'comment_auto_publish'
            )
        }),
        ('Permissions', {
            'fields': ('blogger', 'staff', 'admin', 'status')
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': (
                'title', 'site_title', 'email',
                'password1', 'password2', 'first_name', 'last_name' ,
                'about', 'homepage', 'profile_picture'
            )
        }),
        ('Other info', {
            'fields': (
                'industry', 'occupation', 'interest', 'custom_interest',
                'goals', 'stage', 'custom_stage', 'template_name'
            )
        }),
        ('Options', {
            'fields': (
                'share_profile', 'show_email_address', 'show_blogs',
                'show_followed_sites', 'comment_auto_publish'
            )
        }),
        ('Permissions', {
            'fields': ('blogger', 'staff', 'admin', 'status')
        }),
    )
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
