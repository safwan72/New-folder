from django.db import models
from topperblog.mixins import get_unique_path
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django_countries.fields import CountryField
from .utils import get_unique_path
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


class InterestQuerySet(models.query.QuerySet):
    def count_interest(self):
        return self.aggregate(Count('_id_slug'))


class InterestManager(models.Manager):
    def get_queryset(self):
        return InterestQuerySet(self.model, using=self._db)

    def create(self, **kwargs):
        return super(InterestManager, self).create(_id_slug=kwargs.get('_id_slug', get_unique_path()), **kwargs)


class Interest(models.Model):
    _id_slug = models.SlugField(max_length=20, unique=True, default=get_unique_path)
    title = models.CharField(max_length=24)
    priority = models.IntegerField(default=1)
    status = models.BooleanField(default=1)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority', 'title']
        verbose_name = "Interest"
        verbose_name_plural = "Interests"

    objects = InterestManager()

    def __str__(self):
        return self.title

    @property
    def status_text(self):
        return ['Inactive', 'Active'][self.status]

    @property
    def is_active(self):
        return self.status


class IndustryQuerySet(models.query.QuerySet):
    def count_industry(self):
        return self.aggregate(Count('_id_slug'))


class IndustryManager(models.Manager):
    def get_queryset(self):
        return IndustryQuerySet(self.model, using=self._db)

    def create(self, **kwargs):
        return super(IndustryManager, self).create(_id_slug=kwargs.get('_id_slug', get_unique_path()), **kwargs)


class Industry(models.Model):
    _id_slug = models.SlugField(max_length=20, unique=True, default=get_unique_path)
    title = models.CharField(max_length=32)
    priority = models.IntegerField(default=1)
    status = models.BooleanField(default=1)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority', 'title']
        verbose_name = "Industry"
        verbose_name_plural = "Industries"

    objects = IndustryManager()

    def __str__(self):
        return self.title

    @property
    def status_text(self):
        return ['Inactive', 'Active'][self.status]

    @property
    def is_active(self):
        return self.status


class GoalQuerySet(models.query.QuerySet):
    def count_goal(self):
        return self.aggregate(Count('_id_slug'))


class GoalManager(models.Manager):
    def get_queryset(self):
        return GoalQuerySet(self.model, using=self._db)

    def create(self, **kwargs):
        return super(GoalManager, self).create(_id_slug=kwargs.get('_id_slug', get_unique_path()), **kwargs)


class Goal(models.Model):
    _id_slug = models.SlugField(max_length=20, unique=True, default=get_unique_path)
    title = models.CharField(max_length=48)
    priority = models.IntegerField(default=1)
    status = models.BooleanField(default=1)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority', 'title']
        verbose_name = "Goal"
        verbose_name_plural = "Goals"

    objects = GoalManager()

    def __str__(self):
        return self.title

    @property
    def status_text(self):
        return ['Inactive', 'Active'][self.status]

    @property
    def is_active(self):
        return self.status


class StageQuerySet(models.query.QuerySet):
    def count_stage(self):
        return self.aggregate(Count('_id_slug'))


class StageManager(models.Manager):
    def get_queryset(self):
        return StageQuerySet(self.model, using=self._db)

    def create(self, **kwargs):
        return super(StageManager, self).create(_id_slug=kwargs.get('_id_slug', get_unique_path()), **kwargs)


class Stage(models.Model):
    _id_slug = models.SlugField(max_length=20, unique=True, default=get_unique_path)
    title = models.CharField(max_length=48)
    priority = models.IntegerField(default=1)
    status = models.BooleanField(default=1)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority', 'title']
        verbose_name = "Stage"
        verbose_name_plural = "Stages"

    objects = StageManager()

    def __str__(self):
        return self.title

    @property
    def status_text(self):
        return ['Inactive', 'Active'][self.status]

    @property
    def is_active(self):
        return self.status


class UserManager(BaseUserManager):
    def create_user(self, **kwargs):
        if not kwargs.get('email'):
            raise ValueError('User must be needed a email address.')
        if not kwargs.get('password'):
            raise ValueError('User must be needed a password for security issue.')

        user_obj = self.model(
            email=self.normalize_email(kwargs.pop('email'))
        )

        user_obj.set_password(kwargs.pop('password'))

        goals = kwargs.pop('goals', False)

        for k, v in kwargs.items():
            setattr(user_obj, k, v)

        user_obj.save(using=self._db)

        if goals:
            if kwargs.get('blogger', False):
                user_obj.goals.set(goals)

        return user_obj

    def create_blogger(self, email, password=None, **kwargs):
        user = self.create_user(
            email=email,
            password=password,
            blogger=True,
            **kwargs
        )
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(
            email=email,
            password=password,
            blogger=True,
            staff=True,
            admin=True,
            **kwargs
        )
        return user


class User(AbstractBaseUser, PermissionsMixin):
    _id_slug = models.SlugField(max_length=20, unique=True, default=get_unique_path)

    title = models.CharField(max_length=32, unique=True)
    site_title = models.CharField(max_length=48, unique=True)
    email = models.EmailField(unique=True)  # core for our custom user
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    profile_picture = models.ImageField(default="dummy-profile-pic-male.jpg", upload_to='media', null=True)
    gender = models.CharField(max_length=1, choices=(
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other')
    ))

    phone = models.CharField(max_length=15, null=True)
    city = models.CharField(max_length=30, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)
    zip_postal_code = models.CharField(max_length=30, null=True)
    country = CountryField(null=True, blank=True)

    share_profile = models.BooleanField(default=False)
    show_email_address = models.BooleanField(default=False)
    show_blogs = models.BooleanField(default=False)
    show_followed_sites = models.BooleanField(default=False)
    comment_auto_publish = models.BooleanField(default=True)

    industry = models.ForeignKey('Industry', on_delete=models.CASCADE, null=True)
    occupation = models.CharField(max_length=72, blank=True, null=True)
    interest = models.ForeignKey('Interest', on_delete=models.CASCADE, blank=True, null=True)
    custom_interest = models.CharField(max_length=24, blank=True, null=True)
    goals = models.ManyToManyField('Goal')
    stage = models.ForeignKey('Stage', on_delete=models.CASCADE, blank=True, null=True)
    custom_stage = models.CharField(max_length=48, blank=True, null=True)
    template_name = models.CharField(max_length=2, choices=(
        ('l', 'Light'),
        ('d', 'Dark')
    ), default='l')

    homepage = models.CharField(max_length=30, null=True, blank=True)
    subscribers = models.IntegerField(default=0)

    blogger = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    status = models.BooleanField(default=True)  # can login

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # username

    # USERNAME_FIELD and email are required by default
    REQUIRED_FIELDS = []  # ['full_name', 'email']

    class Meta:
        ordering = ['-update_date', '-create_date']
        verbose_name = "Blogger"
        verbose_name_plural = "Bloggers"

    def __str__(self):
        return self.email

    def get_user(self):
        return self.email

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def short_name(self):
        if self.first_name:
            return self.first_name
        return self.email

    def full_address(self):
        return "%s, %s, %s, %s" % (
            self.zip_postal_code,
            self.city,
            self.country,
            self.state
        )

    def short_address(self):
        return "%s, %s, %s" % (
            self.city,
            self.country,
            self.state
        )

    def join_date(self):
        return self.create_date.date()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    @property
    def profile_picture_url(self):
        return settings.BASE_URL + self.profile_picture.url

    @property
    def status_text(self):
        return ['Inactive', 'Active'][self.status]

    @property
    def is_active(self):
        return self.status

    @property
    def is_blogger(self):
        return self.blogger

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin


class TagQuerySet(models.query.QuerySet):
    def count_tag(self):
        return self.aggregate(Count('_id_slug'))


class TagManager(models.Manager):
    def get_queryset(self):
        return TagQuerySet(self.model, using=self._db)

    def create(self, **kwargs):
        return super(TagManager, self).create(_id_slug=kwargs.get('_id_slug', get_unique_path()), **kwargs)


class Tag(models.Model):
    _id_slug = models.SlugField(max_length=20, unique=True, default=get_unique_path)
    title = models.CharField(max_length=75)
    meta_title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.IntegerField(default=1)
    status = models.BooleanField(default=1)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority', 'title']
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    objects = TagManager()

    def __str__(self):
        return self.title

    @property
    def status_text(self):
        return ['Inactive', 'Active'][self.status]

    @property
    def is_active(self):
        return self.status


class CategoryQuerySet(models.query.QuerySet):
    def count_category(self):
        return self.aggregate(Count('_id_slug'))


class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def create(self, **kwargs):
        return super(CategoryManager, self).create(_id_slug=kwargs.get('_id_slug', get_unique_path()), **kwargs)


class Category(models.Model):
    _id_slug = models.SlugField(max_length=20, unique=True, default=get_unique_path)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=75)
    meta_title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.IntegerField(default=1)
    status = models.BooleanField(default=1)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority', 'title']
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    objects = CategoryManager()

    def __str__(self):
        return self.title

    @property
    def status_text(self):
        return ['Inactive', 'Active'][self.status]

    @property
    def is_active(self):
        return self.status


class PostQuerySet(models.query.QuerySet):
    def count_post(self):
        return self.aggregate(Count('_id_slug'))


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def create(self, **kwargs):
        return super(PostManager, self).create(_id_slug=kwargs.get('_id_slug', get_unique_path()), **kwargs)


class Post(models.Model):
    _id_slug = models.SlugField(max_length=20, unique=True, default=get_unique_path)
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    parent_post = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    title = models.CharField(max_length=75)
    meta_title = models.CharField(max_length=100)
    summary = models.TextField()
    content = models.TextField()

    thumbnail = models.ImageField(null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)

    published = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(blank=True, null=True)

    viewed_count = models.IntegerField(default=0)
    favourite_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-published', 'title']
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    objects = PostManager()

    def __str__(self):
        return self.title

    @property
    def publish_text(self):
        return ['Drafted', 'Published'][self.published]

    @property
    def thumbnail_url(self):
        return settings.BASE_URL + '/media/' + self.thumbnail

    @property
    def is_publish(self):
        return self.published

    @property
    def is_draft(self):
        return not self.published


class PostViewQuerySet(models.query.QuerySet):
    def count_post_view(self):
        return self.aggregate(Count('_id_slug'))


class PostViewManager(models.Manager):
    def get_queryset(self):
        return PostViewQuerySet(self.model, using=self._db)

    def create(self, **kwargs):
        return super(PostViewManager, self).create(_id_slug=kwargs.get('_id_slug', get_unique_path()), **kwargs)


class PostView(models.Model):
    _id_slug = models.SlugField(max_length=20, unique=True, default=get_unique_path)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    viewed_by = models.ForeignKey('User', on_delete=models.CASCADE)
    view_count = models.IntegerField(default=1)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-view_count']
        verbose_name = "Blog Viewed"
        verbose_name_plural = "Blogs Viewed"

    objects = PostViewManager()

    def __str__(self):
        return "%s views by %s on %s" %(self.view_count, self.viewed_by, self.post)


class CommentQuerySet(models.query.QuerySet):
    def count_comment(self):
        return self.aggregate(Count('_id_slug'))


class CommentManager(models.Manager):
    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db)

    def create(self, **kwargs):
        return super(CommentManager, self).create(_id_slug=kwargs.get('_id_slug', get_unique_path()), **kwargs)


class Comment(models.Model):
    _id_slug = models.SlugField(max_length=20, unique=True, default=get_unique_path)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    comment_by = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.TextField()
    priority = models.IntegerField(default=1)

    published = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-published']
        verbose_name = "Blog Comment"
        verbose_name_plural = "Blogs Comments"

    objects = CommentManager()

    def __str__(self):
        return "{} on {}".format(self.comment_by, self.post)

    @property
    def publish_text(self):
        return ['Drafted', 'Published'][self.published]

    @property
    def is_publish(self):
        return self.published

    @property
    def is_draft(self):
        return not self.published


class LikeQuerySet(models.query.QuerySet):
    def count_like(self):
        return self.aggregate(Count('_id_slug'))


class LikeManager(models.Manager):
    def get_queryset(self):
        return LikeQuerySet(self.model, using=self._db)

    def create(self, **kwargs):
        return super(LikeManager, self).create(_id_slug=kwargs.get('_id_slug', get_unique_path()), **kwargs)


class Like(models.Model):
    _id_slug = models.SlugField(max_length=20, unique=True, default=get_unique_path)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    like_by = models.ForeignKey('User', on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)

    objects = LikeManager()

    class Meta:
        ordering = ['-create_date']
        verbose_name = "Blog Like"
        verbose_name_plural = "Blogs Likes"

    def __str__(self):
        return "Like on %s" %self.post


class FavouriteQuerySet(models.query.QuerySet):
    def count_like(self):
        return self.aggregate(Count('_id_slug'))


class FavouriteManager(models.Manager):
    def get_queryset(self):
        return FavouriteQuerySet(self.model, using=self._db)

    def create(self, **kwargs):
        return super(FavouriteManager, self).create(_id_slug=kwargs.get('_id_slug', get_unique_path()), **kwargs)


class Favourite(models.Model):
    _id_slug = models.SlugField(max_length=20, unique=True, default=get_unique_path)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    favourite_by = models.ForeignKey('User', on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)

    objects = FavouriteManager()

    class Meta:
        ordering = ['-create_date']
        verbose_name = "Blog Favourite"
        verbose_name_plural = "Blogs Favourites"

    def __str__(self):
        return "Heart on %s" %self.post


class ContactManager(models.Manager):
    def get_queryset(self):
        return LikeQuerySet(self.model, using=self._db)

    def create(self, **kwargs):
        return super(ContactManager, self).create(_id_slug=kwargs.get('_id_slug', get_unique_path()), **kwargs)


class Contact(models.Model):
    _id_slug = models.SlugField(max_length=20, unique=True, default=get_unique_path)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

    objects = ContactManager()

    class Meta:
        ordering = ['-create_date']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return self.email


class NewsletterSubscriberManager(models.Manager):
    def get_queryset(self):
        return LikeQuerySet(self.model, using=self._db)

    def create(self, **kwargs):
        return super(NewsletterSubscriberManager, self).create(_id_slug=kwargs.get('_id_slug', get_unique_path()), **kwargs)


class NewsletterSubscriber(models.Model):
    newsletter_cat_choices = (
        ('hp', 'Support'),
        ('td', 'Trending'),
        ('wg', 'Warning')
    )

    _id_slug = models.SlugField(max_length=20, unique=True, default=get_unique_path)
    email = models.EmailField()
    category = models.CharField(max_length=2, choices=newsletter_cat_choices, default='hp')
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)

    objects = NewsletterSubscriberManager()

    class Meta:
        ordering = ['-create_date']
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"

    def __str__(self):
        return self.email


class ContactPageManager(models.Manager):
    def get_queryset(self):
        return LikeQuerySet(self.model, using=self._db)

    def create(self, **kwargs):
        return super(ContactPageManager, self).create(_id_slug=kwargs.get('_id_slug', get_unique_path()), **kwargs)


class ContactPage(models.Model):
    _id_slug = models.SlugField(max_length=20, unique=True, default=get_unique_path)
    page_title = models.CharField(max_length=255, default='Contact')
    page_head = models.TextField()
    page_main = models.TextField()
    page_footer = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    objects = ContactPageManager()

    class Meta:
        ordering = ['-create_date']
        verbose_name = "Pages - Contact"
        verbose_name_plural = "Pages - Contact"

    def __str__(self):
        return self.page_title


class AboutPageManager(models.Manager):
    def get_queryset(self):
        return LikeQuerySet(self.model, using=self._db)

    def create(self, **kwargs):
        return super(AboutPageManager, self).create(_id_slug=kwargs.get('_id_slug', get_unique_path()), **kwargs)


class AboutPage(models.Model):
    _id_slug = models.SlugField(max_length=20, unique=True, default=get_unique_path)
    page_title = models.CharField(max_length=255, default='About')
    page_head = models.TextField()
    page_main = models.TextField()
    page_footer = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    objects = AboutPageManager()

    class Meta:
        ordering = ['-create_date']
        verbose_name = "Pages - About"
        verbose_name_plural = "Pages - About"

    def __str__(self):
        return self.page_title
