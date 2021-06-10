from django.core.mail import EmailMessage
import threading, random, string, json
from rest_framework.parsers import BaseParser


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()


class RequestAttachMixin(object):
	def get_form_kwargs(self):
		kwargs = super(RequestAttachMixin, self).get_form_kwargs()
		kwargs['request'] = self.request
		return kwargs


class NextUrlMixin(object):
	default_path = '/'

	def get_next_url(self):
		request = self.request
		next_page 		= request.GET.get('next')
		next_post 		= request.POST.get('next')
		redirect_path 	= next_page or next_post or None
		if is_safe_url(redirect_path, request.get_host()):
			return redirect_path
		else:
			return self.default_path


def get_unique_path(how_many=19):
	range_ = how_many
	chars = string.ascii_lowercase + string.digits
	plus = ''.join(random.choice(chars) for _ in range(range_))
	dig = range(0,9)
	plus = plus + str(random.randint(0,9))
	return plus


class FieldMaps:
    def interests(self):
        return {
            '_id_slug': {'field': 'slug', 'type': 'string', 'name': 'ID', 'col': 12, 'show_create': False},
            'title': {'field': 'text', 'type': 'string', 'name': 'Title', 'col': 12, 'required': True},
            'priority': {'field': 'integer', 'type': 'number', 'name': 'Priority', 'col': 12, 'required': False},
            'status': {'field': 'boolean', 'type': 'boolean', 'name': 'Status', 'col': 12, 'required': False},
            'create_date': {'field': 'datetime', 'type': 'date', 'name': 'Create Date', 'show_create': False}
        }
        
    def industries(self):
        return {
            '_id_slug': {'field': 'slug', 'type': 'string', 'name': 'ID', 'col': 12, 'show_create': False},
            'title': {'field': 'text', 'type': 'string', 'name': 'Title', 'col': 12, 'required': True},
            'priority': {'field': 'integer', 'type': 'number', 'name': 'Priority', 'col': 12, 'required': False},
            'status': {'field': 'boolean', 'type': 'boolean', 'name': 'Status', 'col': 12, 'required': False},
            'create_date': {'field': 'datetime', 'type': 'date', 'name': 'Create Date', 'show_create': False}
        }
        
    def goals(self):
        return {
            '_id_slug': {'field': 'slug', 'type': 'string', 'name': 'ID', 'col': 12, 'show_create': False},
            'title': {'field': 'text', 'type': 'string', 'name': 'Title', 'col': 12, 'required': True},
            'priority': {'field': 'integer', 'type': 'number', 'name': 'Priority', 'col': 12, 'required': False},
            'status': {'field': 'boolean', 'type': 'boolean', 'name': 'Status', 'col': 12, 'required': False},
            'create_date': {'field': 'datetime', 'type': 'date', 'name': 'Create Date', 'show_create': False}
        }
        
    def stages(self):
        return {
            '_id_slug': {'field': 'slug', 'type': 'string', 'name': 'ID', 'col': 12, 'show_create': False},
            'title': {'field': 'text', 'type': 'string', 'name': 'Title', 'col': 12, 'required': True},
            'priority': {'field': 'integer', 'type': 'number', 'name': 'Priority', 'col': 12, 'required': False},
            'status': {'field': 'boolean', 'type': 'boolean', 'name': 'Status', 'col': 12, 'required': False},
            'create_date': {'field': 'datetime', 'type': 'date', 'name': 'Create Date', 'show_create': False}
        }
        
    def tags(self):
        return {
            '_id_slug': {'field': 'slug', 'type': 'string', 'name': 'ID', 'col': 12, 'show_create': False},
            'title': {'field': 'text', 'type': 'string', 'name': 'Title', 'col': 12, 'required': True},
            'meta_title': {'field': 'text', 'type': 'string', 'name': 'Meta Title', 'col': 12, 'required': False},
            'description': {'field': 'textarea', 'type': 'string', 'name': 'Description', 'col': 24, 'required': False},
            'priority': {'field': 'integer', 'type': 'number', 'name': 'Priority', 'col': 12, 'required': False},
            'status': {'field': 'boolean', 'type': 'boolean', 'name': 'Status', 'col': 12, 'required': False},
            'create_date': {'field': 'datetime', 'type': 'date', 'name': 'Create Date', 'show_create': False}
        }
        
    def categories(self):
        return {
            '_id_slug': {'field': 'slug', 'type': 'string', 'name': 'ID', 'col': 12, 'show_create': False},
            'parent_category': {'field': 'select', 'model': 'categories', 'to': 'title', 'type': 'object', 'name': 'Parent Category', 'col': 12, 'required': False},
            'title': {'field': 'text', 'type': 'string', 'name': 'Title', 'col': 12, 'required': True},
            'meta_title': {'field': 'text', 'type': 'string', 'name': 'Meta Title', 'col': 12, 'required': False},
            'description': {'field': 'textarea', 'type': 'string', 'name': 'Description', 'col': 24, 'required': False},
            'priority': {'field': 'integer', 'type': 'number', 'name': 'Priority', 'col': 12, 'required': False},
            'status': {'field': 'boolean', 'type': 'boolean', 'name': 'Status', 'col': 12, 'required': False},
            'create_date': {'field': 'datetime', 'type': 'date', 'name': 'Create Date', 'show_create': False}
        }
        
    def users(self):
        return {
            '_id_slug': {'field': 'slug', 'type': 'string', 'name': 'ID', 'col': 12, 'show_create': False}, 
            'title': {'field': 'text', 'type': 'string', 'name': 'Title', 'col': 12, 'required': True}, 
            'site_title': {'field': 'text', 'type': 'string', 'name': 'Site Title', 'col': 12, 'required': False},
            'email': {'field': 'email', 'type': 'email', 'name': 'Email', 'col': 12, 'required': True},
            'first_name': {'field': 'text', 'type': 'string', 'name': 'First Name', 'col': 12, 'required': True}, 
            'last_name': {'field': 'text', 'type': 'string', 'name': 'Last Name', 'col': 12, 'required': True},
            'about': {'field': 'textarea', 'type': 'string', 'name': 'About', 'col': 24, 'required': False},
            'profile_picture': {'field': 'image', 'type': 'string', 'name': 'Image', 'col': 12, 'required': False},
            'gender': {'field': 'text', 'type': 'string', 'name': 'Gender', 'col': 12, 'required': True},
            'phone': {'field': 'text', 'type': 'string', 'name': 'Phone', 'col': 12, 'required': True},
            'city': {'field': 'text', 'type': 'string', 'name': 'City', 'col': 12, 'required': True},
            'state': {'field': 'text', 'type': 'string', 'name': 'State', 'col': 12, 'required': False},
            'zip_postal_code': {'field': 'text', 'type': 'string', 'name': 'Postal Code', 'col': 12, 'required': True},
            'country': {'field': 'select', 'model': 'countries', 'to': 'name', 'type': 'object', 'name': 'Country', 'col': 12, 'required': False},
            'share_profile': {'field': 'boolean', 'type': 'boolean', 'name': 'Show profile', 'col': 12, 'required': False},
            'show_email_address': {'field': 'boolean', 'type': 'boolean', 'name': 'Show email', 'col': 12, 'required': False},
            'show_blogs': {'field': 'boolean', 'type': 'boolean', 'name': 'Show my blogs', 'col': 12, 'required': False},
            'show_followed_sites': {'field': 'boolean', 'type': 'boolean', 'name': 'Show followed sites', 'col': 12, 'required': False},
            'comment_auto_publish': {'field': 'boolean', 'type': 'boolean', 'name': 'Auto publish comment', 'col': 12, 'required': False},
            'industry': {'field': 'select', 'model': 'industries', 'to': 'title', 'type': 'object', 'name': 'Industry', 'col': 12, 'required': False},
            'occupation': {'field': 'text', 'type': 'string', 'name': 'Occupation', 'col': 12, 'required': False},
            'interest': {'field': 'select', 'model': 'interests', 'to': 'title', 'type': 'object', 'name': 'Interest', 'col': 12, 'required': False},
            'custom_interest': {'field': 'text', 'type': 'string', 'name': 'Interest', 'col': 12, 'required': False},
            'goals': {'field': 'multiselect', 'model': 'goals',  'type': 'array', 'name': 'Goals', 'col': 12, 'required': False},
            'stage': {'field': 'select', 'model': 'stages', 'to': 'title', 'type': 'object', 'name': 'Stage', 'col': 12, 'required': False},
            'custom_stage': {'field': 'text', 'type': 'string', 'name': 'Stage', 'col': 12, 'required': False},
            'template_name': {'field': 'text', 'type': 'string', 'name': 'Template', 'col': 12, 'required': False},
            'homepage': {'field': 'text', 'type': 'string', 'name': 'Homepage', 'col': 12, 'required': False},
            'subscribers': {'field': 'integer', 'type': 'number', 'name': 'Total Subscriber', 'show_create': False},
            'blogger': {'field': 'boolean', 'type': 'boolean', 'name': 'Blogger', 'col': 12, 'show_create': False},
            'admin': {'field': 'boolean', 'type': 'boolean', 'name': 'Admin', 'col': 12, 'show_create': False},
            'status': {'field': 'boolean', 'type': 'boolean', 'name': 'Status', 'col': 12, 'required': False},
            'create_date': {'field': 'datetime', 'type': 'date', 'name': 'Create Date', 'show_create': False}, 
            'update_date': {'field': 'datetime', 'type': 'date', 'name': 'Update Date', 'show_create': False},
        }
        
    def posts(self):
        return {
            '_id_slug': {'field': 'slug', 'type': 'string', 'name': 'ID', 'col': 12, 'show_create': False},
            'author': {'field': 'select', 'model': 'users', 'to': 'first_name', 'type': 'number', 'name': 'Author', 'col': 12, 'required': True},
            'parent_post': {'field': 'select', 'model': 'posts', 'to': 'title', 'type': 'string', 'name': 'Parent Post', 'col': 12, 'required': False},
            'title': {'field': 'text', 'type': 'string', 'name': 'Title', 'col': 12, 'required': True},
            'meta_title': {'field': 'text', 'type': 'string', 'name': 'Meta Title', 'col': 12, 'required': True},
            'summary': {'field': 'textarea', 'type': 'string', 'name': 'Summary', 'col': 24, 'required': True},
            'content': {'field': 'texteditor', 'type': 'string', 'name': 'Content', 'col': 24, 'required': True},
            'published': {'field': 'boolean', 'type': 'boolean', 'name': 'Publish', 'col': 12, 'required': False},
            'create_date': {'field': 'datetime', 'type': 'date', 'name': 'Create Date', 'show_create': False},
            'update_date': {'field': 'datetime', 'type': 'date', 'name': 'Update Date', 'show_create': False},
            'publish_date': {'field': 'datetime', 'type': 'date', 'name': 'Publish Date', 'show_create': False},
            'viewed_count': {'field': 'integer', 'type': 'number', 'name': 'Total View', 'show_create': False},
            'favourite_count': {'field': 'integer', 'type': 'number', 'name': 'Total Favourite', 'show_create': False},
            'like_count': {'field': 'integer', 'type': 'number', 'name': 'Total Like', 'show_create': False},
            'comment_count': {'field': 'integer', 'type': 'number', 'name': 'Total Comment', 'show_create': False}
        }
        
    def postviews(self):
        return {
            '_id_slug': {'field': 'slug', 'type': 'string', 'name': 'ID', 'col': 12, 'show_create': False},
            'post': {'field': 'select', 'model': 'posts', 'to': 'title', 'type': 'object', 'name': 'Post', 'col': 12, 'required': True},
            'viewed_by': {'field': 'select', 'model': 'users', 'to': 'first_name', 'type': 'object', 'name': 'Viewed By', 'col': 12, 'show_create': False},
            'view_count': {'field': 'integer', 'type': 'number', 'name': 'Total View', 'show_create': False}
        }
        
    def comments(self):
        return {
            '_id_slug': {'field': 'slug', 'type': 'string', 'name': 'ID', 'col': 12, 'show_create': False},
            'post': {'field': 'select', 'model': 'posts', 'to': 'title', 'type': 'object', 'name': 'Post', 'col': 12, 'required': True},
            'parent_comment': {'field': 'select', 'model': 'comments', 'to': 'title', 'type': 'object', 'name': 'Parent Comment', 'col': 12, 'required': False},
            # 'title': {'field': 'text', 'type': 'string', 'name': 'Title', 'col': 12, 'required': True},
            'content': {'field': 'textarea', 'type': 'string', 'name': 'Content', 'col': 24, 'required': True},
            'priority': {'field': 'integer', 'type': 'number', 'name': 'Priority', 'col': 12, 'required': False},
            'published': {'field': 'boolean', 'type': 'boolean', 'name': 'Publish', 'col': 12, 'required': False},
            'create_date': {'field': 'datetime', 'type': 'date', 'name': 'Create Date', 'show_create': False},
            'publish_date': {'field': 'datetime', 'type': 'date', 'name': 'Publish Date', 'show_create': False}
        }
        
    def likes(self):
        return {
            '_id_slug': {'field': 'slug', 'type': 'string', 'name': 'ID', 'col': 12, 'show_create': False},
            'post': {'field': 'select', 'model': 'posts', 'to': 'post', 'type': 'object', 'name': 'Post', 'col': 12, 'required': True},
        }

    def favourites(self):
        return {
            '_id_slug': {'field': 'slug', 'type': 'string', 'name': 'ID', 'col': 12, 'show_create': False},
            'post': {'field': 'select', 'model': 'posts', 'to': 'post', 'type': 'object', 'name': 'Post', 'col': 12, 'required': True},
        }

    def contacts(self):
        return {
            '_id_slug': {'field': 'slug', 'type': 'string', 'name': 'ID', 'col': 12, 'show_create': False},
            'email': {'field': 'email', 'type': 'email', 'name': 'Email', 'col': 12, 'required': True},
            'subject': {'field': 'text', 'type': 'string', 'name': 'Subject', 'col': 12, 'required': True},
            'content': {'field': 'textarea', 'type': 'string', 'name': 'Content', 'col': 24, 'required': True}
        }

    def newsletters(self):
        return {
            '_id_slug': {'field': 'slug', 'type': 'string', 'name': 'ID', 'col': 12, 'show_create': False},
            'email': {'field': 'email', 'type': 'email', 'name': 'Email', 'col': 12, 'required': True},
            'category': {'field': 'select', 'type': 'object', 'name': 'Category', 'col': 12, 'options': [
                                                                                        {'tag': 'hp', 'text': 'Support'},
                                                                                        {'tag': 'td', 'text': 'Trending'},
                                                                                        {'tag': 'wg', 'text': 'Warning'}
                                                                                    ], 'required': True},
        }


class PlainTextParser(BaseParser):
    """
    Plain text parser.
    """
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        read_stream = stream.read()
        print(read_stream)
        diction = dict(json.loads(read_stream.decode()))
        print(diction)
        return diction
