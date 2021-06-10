from django.shortcuts import render, redirect
from django.db.models import Sum
from django.core.management import ManagementUtility

from .models import *
from cdi.models import ActiveCompany

import requests, json


def confirm_setup_account(request):

    data = request.POST
    data = {k: v for k, v in data.items()}

    if data.pop('csrfmiddlewaretoken', False):

        payload = {
            'blogdi': {
                'client': {
                    'entry_name': data['entry_name'],
                    'email': data['email'],
                    'phone': data['phone'],
                    'address': data['address'],
                    'zip_postal_code': data['zip_postal_code'],
                    'is_active': True
                },
                'license': {
                    'license_key': data['license_key'],
                    'active_period': 'nan',
                    'domain': request.META['HTTP_HOST']
                },
                'domain': request.META['HTTP_HOST'],
                'frontend_domain': data['frontend_domain'],
                'ip_address': request.META['REMOTE_ADDR'],
                'mac_address': None,
                'browser': request.META['HTTP_USER_AGENT'],
                'is_active': True
            }
        }

        result = requests.post(
                    "https://circledi.herokuapp.com/register/setup-blogdi/",
                    data=json.dumps(payload),
                    headers={
                        'ContentType': 'application/json'
                    }
                )

        # print(result.content.decode())

        json_result = result.json()

        if json_result['statusCode'] == 200 and json_result.get('setup', False):
            active_company = ActiveCompany.objects.create(
                    entry_name = data['entry_name'],
                    email = data['email'],
                    phone = data['phone'],
                    address = data['address'],
                    zip_postal_code = data['zip_postal_code'],
                    license_key = data['license_key'],
                    active_period = 'nan',
                    domain = request.META['wsgi.url_scheme'] + '://' + request.META['HTTP_HOST']
                )

            user = User.objects.filter(email=data['email']).first()

            if user:
                if not user.status:
                    user.status = True
                    user.save()
            else:
                user = User.objects.create_superuser(
                    title = 'suser',
                    site_title = 'suser',
                    email = data['email'],
                    password = '@123456@',
                    first_name = 'Sandbox',
                    last_name = 'Admin',
                    about = 'Demo user to access panel',
                    gender = 'm',
                    phone = data['phone']
                )

            cdi_fixtures = ManagementUtility(
                                        [
                                            'manage.py',
                                            'loaddata',
                                            'topperblog/fixtures/cdi.json'
                                        ]
                                    )
            blogger_fixtures = ManagementUtility(
                                        [
                                            'manage.py',
                                            'loaddata',
                                            'topperblog/fixtures/blogger.json'
                                        ]
                                    )

            cdi_fixtures.execute()
            blogger_fixtures.execute()

            return redirect('blogdi_dashboard')

    else:
        print('Blocked by server')

    return render(request, 'login.html', {})


def dashboard(request):
    client = ActiveCompany.objects.first()

    authentic = False
    print(client)
    if client:
        if client.domain == request.META['HTTP_HOST']:
            authentic = True

    if not authentic:
        return render(request, 'login.html', {})

    if not request.user.is_authenticated:
        return redirect('/admin/login/?next=/')

    bloggers = User.objects.filter(blogger=True, status=True).order_by('-subscribers')
    posts = Post.objects.filter(published=True).all()
    comments = Comment.objects.filter(published=True).all()
    likes = Like.objects.all()
    favourites = Favourite.objects.all()
    total_view = PostView.objects.aggregate(total=Sum('view_count'))

    context = {
        'bloggers': bloggers,
        'posts': posts,
        'comments': comments,
        'likes': likes,
        'favourites': favourites,
        'total_view': total_view
    }

    return render(request, 'index.html', context)

