# -*- coding: utf-8 -*-
# encoding: utf-8
import hashlib, datetime, random
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, render_to_response
from accounts.models import User, UserProfile
from django.template.context_processors import csrf
from django.core.cache import cache
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from accounts.forms import AdminUserAddForm
from logsys.forms import RegistrationForm
from logsys.models import UserWallet
from django.conf import settings
# Create your views here.
from tovar.models import Product


def findUsers(request, *args):
    if request.method == "POST":
        if request.POST.get('name_parent'):
            try:
                user_parent = User.objects.get(username=request.POST['name_parent'])
                cache.add('id_parent', user_parent.pk)
                return redirect('/auth/register/')
            except ObjectDoesNotExist:
                args = {}
                args['errors'] = "Not foune %s" % (request.POST['name_parent'])
                return render(request, 'register.html', args)
        elif request.POST.get('id_parent'):
            try:
                user_parent = User.objects.get(pk=int(request.POST.get('id_parent')))
                cache.add('parent_isActie', False)
                cache.add('id_parent', user_parent.pk)
                return redirect('/auth/register/')

            except ObjectDoesNotExist:
                args = {}
                args['errors'] = "Not foune %s" %(request.POST['id_parent'])
                return render(request, 'register.html', args)
        else:
            args = {}
            args['errors'] = "There are no values for the search."
            return render(request, 'register.html', args)

    return render(request, 'register.html', args)


# Регистрация аккаунта, в логин записываем емайл
def RegisterView(request, *args):
    #cache.delete('id_parent')
    if not args:
        args = {}

    args.update(csrf(request))
    args['bar'] = "register"

    if request.method == "POST":
        #args['form'] = RegistrationForm(request.POST)
        args['username'] = request.POST['email']
        args['email'] = request.POST['email']
        args['first_name'] = request.POST['first_name']
        args['last_name'] = request.POST['last_name']
        args['password2'] = request.POST['password2']
        args['password1'] = request.POST['password1']
        args['id_parent'] = request.POST['id_parent']

        if not request.POST.get('dogovor'):
            args['errors'] = "Вам следует ознакомится с условиями договора публичной оферты."
            return render(request, 'register.html', args)


        if request.POST.get('id_parent'):
            try:
                user_parent = User.objects.get(pk=int(request.POST.get('id_parent')))
                args['parent'] = user_parent.pk
            except ObjectDoesNotExist:
                args['errors'] = "Ваш рекомендатель не найден."
                return render(request, 'register.html', args)
        try:
            user = User.objects.get(email=request.POST['email'])
            args['errors'] = "Email %s уже существует. Проверьте почту, при регистрации Вам на почту была отправленна ссылка для активациии данного аккаунта." % (user)

            return render(request, 'register.html', args)
        except ObjectDoesNotExist:
            newuser_form = RegistrationForm(args)

        if not newuser_form.errors:
            newuser_form.save()

            email = request.POST['email']
            username = request.POST['email']

            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt + email).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            user = User.objects.get(username=username)

            # Create and save user profile
            new_profile = UserProfile(user=user, activation_key=activation_key,
                                      key_expires=key_expires)
            new_profile.save()

            # Send email with activation key
            email_subject = 'Confirmation of registration'
            email_body = "Hey %s, thanks for signing up. To activate your account, click this link within " \
                         "48 hours http://setbiz.ru/auth/%s/" % (username, activation_key)
            send_mail(email_subject, email_body, settings.EMAIL_HOST_USER,
                      [email], fail_silently=False)

            #Данная форма убирает дополнительную активацию
            #newuser = auth.authenticate(username=newuser_form.cleaned_data['email'], password=newuser_form.cleaned_data['password2'])
            #auth.login(request, newuser)
            args['activeEmail'] = "%s" % (username)

            return render(request, 'register.html', args)
        else:
            args['form'] = newuser_form
            return render(request, 'register.html', args)
    else:
        return render(request, 'register.html', args)


def LoginFormView(request, *args):
    args = {'bar': "register"}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            cache.delete('id_parent')
            cache.add('id_parent', user.pk)
            return redirect('/office/')
        else:
            args['login_error'] = "Пользователь не найден"
            return render(request, 'login.html', args)
    else:
        return render(request, 'login.html', args)


def LogoutView(request):
    auth.logout(request)
    return redirect("/")


def errors404(request):
    args = {}
    args.update(csrf(request))
    args['bar'] = ""
    return render(request, '404-page.html', args)


# @cache_page(60 * 15)
def index(request, id_parent=-1, *args):
    if not args:
        args = {}
    args.update(csrf(request))
    args['bar'] = "register"


    if id_parent != -1:

        cache.delete('id_parent')
        cache.add('id_parent', id_parent)

        id_parent = cache.get('id_parent')

        try:
            user_parent = User.objects.get(pk=id_parent)

            args['parent'] = user_parent.username
            args['id_parent'] = user_parent.pk
            args['lastname_parent'] = user_parent.last_name
            args['firsname_parent'] = user_parent.first_name
            return render(request, 'register.html', args)

        except ObjectDoesNotExist:
            args['errors'] = "Not users number %s" %id_parent
            return render(request, 'register.html', args)

    args['bar'] = "index"
    args['id_parent'] = id_parent
    args['products'] = Product.objects.filter(company_id=4, published_date__lte=timezone.now()).order_by('published_date')[:4]
    args['samsung'] = Product.objects.filter(company_id=25, published_date__lte=timezone.now()).order_by('published_date')[:4]
    args['virt'] = Product.objects.filter(destination_id=33, published_date__lte=timezone.now()).order_by('published_date')[:4]

    return render(request, 'index.html', args)


#########################################################################
# Регистрция нового аккаунта
#########################################################################
@login_required(login_url='/')
# @cache_page(60 * 15)
def new(request, *args):
    args = {'bar': "register"}
    if request.method == 'POST':

        args['username'] = request.POST['email']
        args['email'] = request.POST['email']
        args['first_name'] = request.POST['first_name']
        args['last_name'] = request.POST['last_name']
        args['password2'] = request.POST['password2']
        args['password1'] = request.POST['password1']
        args['parent'] = request.user.pk

        try:
            # Если емайл уже имеется в системе то выдаем сообщение
            user = User.objects.get(email=request.POST['email'])
            args['errors'] = "Email %s уже существует. Проверьте почту, при регистрации на данный электронный адрес " \
                             "была отправленна ссылка для активациии аккаунта." % (user)
            return render(request, 'new.html', args)

        # Еслим емайла нет
        except ObjectDoesNotExist:

            if not request.POST.get('dogovor'):
                args['errors'] = "Вам следует ознакомится с условиями договора публичной оферты."
                return render(request, 'new.html', args)

            # Проверяем имеется ли ид спонсора в кеше
            if not cache.get('id_parent') and request.user.is_active:
                cache.add('id_parent', request.user.pk)
                args['id_parent'] = cache.get('id_parent')

            # Если емайла нет и пришли данные то делаем дела
            if request.method == 'POST':
                email_unique = User.objects.filter(email=request.POST['email'])
                if email_unique:
                    args['errors'] = "Данный емайл уже зарегестрирован."
                else:
                    # Через форму проверяем данные
                    user_form = AdminUserAddForm(args)
                    if user_form.is_valid():
                        if request.POST['password1'] == request.POST['password2']:
                            args.update(csrf(request))
                            # Сохраняем данные профиля
                            user_form.save()
                            ###
                            # При регистрации человека, нужно увеличить структуру на 1 у всех выше пользователя
                            parent = request.user
                            bool = True
                            while bool:
                                structure = User.objects.get(pk=parent.pk)
                                print (structure)
                                User.objects.filter(pk=parent.pk).update(structure=int(structure.structure) + 1)
                                if parent.parent is not None:
                                    parent = parent.parent
                                else:
                                    bool = False
                            ###
                            # Сохраняем данные в переменные
                            email = request.POST['email']
                            username = request.POST['email']
                            #
                            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
                            activation_key = hashlib.sha1(salt + email).hexdigest()
                            key_expires = datetime.datetime.today() + datetime.timedelta(2)

                            user = User.objects.get(username=username)

                            # Create and save user profile
                            new_profile = UserProfile(user=user, activation_key=activation_key,
                                                      key_expires=key_expires)
                            new_profile.save()

                            # Send email with activation key
                            email_subject = 'Confirmation of registration'
                            email_body = "Hey %s, thanks for signing up. To activate your account, click this link within " \
                                         "48 hours http://setbiz.ru/auth/%s/" % (username, activation_key)
                            send_mail(email_subject, email_body, settings.EMAIL_HOST_USER,
                                      [email], fail_silently=False)

                            # Данная форма убирает дополнительную активацию
                            # newuser = auth.authenticate(username=newuser_form.cleaned_data['email'], password=newuser_form.cleaned_data['password2'])
                            # auth.login(request, newuser)
                            args['activeEmail'] = "%s" % (username)

                        else:
                            args['errors'] = "Пароли не совпадают."
                    else:
                        args['errors'] = user_form.errors

    return render(request, 'new.html', args)


######################################################################
# активация аккаунта по ключу высланному на емайл
######################################################################
def register_confirm(request, activation_key, *args):
    #check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        auth.logout(request)

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    ###########################################################################################
    # Проверяем срок действия ключа,
    # нужно добавить ошибку
    ###########################################################################################
    #check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        User.objects.filter(pk=user_profile.user.pk).delete()
        return redirect('/auth/register/')

    #if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()

    ###
    # При регистрации человека, нужно увеличить структуру на 1 у всех выше пользователя
    parent = user.parent
    bool = True
    if parent is not None:
        while bool:
            structure = User.objects.get(pk=parent.pk)
            print (structure)
            User.objects.filter(pk=parent.pk).update(active_is_structure=int(structure.active_is_structure) + 1)
            if parent.parent is not None:
                parent = parent.parent
            else:
                bool = False
    ###
    args={'activeEmail': user.email}
    return render(request, 'login.html', args)


def oferta(request):
    args = {'bar': "marketing"}
    return render(request, 'offerta.html', args)


def contacts(request):
    args = {'bar': "contacts"}
    return render(request, 'contacts.html', args)


def news(request):
    args = {'bar': "company"}
    return render(request, 'info_company.html', args)



########################################################################################################################
# Фукция проверки пин кода в кошельке
########################################################################################################################
@login_required(login_url='/')
def pinWallet(request, args, **kwargs):
    # В данную функцию требуется только передать параметр пин код
    if not args:
        return False

    if args["pin"]:
        try:
            userWallet = UserWallet.objects.get(UserWallet_user=request.user)
            if userWallet.UserWallet_password == args['pin']:
                return True
            else:
                args["errors"] = "Ошибка ввода пин кода для кошелька. "
                # Если пароль введен не верно, то просим пользователя ввести его еще раз
                return render(request, "InWallet.html", args)

        except ObjectDoesNotExist:
            return False

    else:
        return False

