# coding: utf-8
# encoding=utf8
import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.template.context_processors import csrf

from message.models import massege_user, message_message
from accounts.models import User
from django.shortcuts import get_object_or_404


# Create your views here.


##########################################################################
# Главная страница сообщений
##########################################################################
@login_required(login_url='/')
def index(request, *args):
    if not args:
        args = {}
    args['bar'] = "office"

    var1 = None
    message = None

    args['massege_user'] = massege_user.objects.filter(user_one=request.user)
    args['massege_user2'] = massege_user.objects.filter(user_two=request.user)
    print (args)

    return render(request, 'message.html', args)


@login_required(login_url='/')
def send_message(request, id_user=None, *args):
    if not args:
        args = {}
    args['bar'] = "office"

    sendUser = get_object_or_404(User, pk=id_user)
    args['sendUser'] = sendUser
    var1 = None
    message = None

    try:
        var1 = massege_user.objects.get(user_one=request.user, user_two=sendUser)
        message = message_message.objects.filter(correspondents=var1.pk)

    except ObjectDoesNotExist:
        try:
            var1 = massege_user.objects.get(user_one=sendUser, user_two=request.user)
            message = message_message.objects.filter(correspondents=var1.pk)
        except ObjectDoesNotExist:
            print ("None")

    args['massege'] = message
    args['massege_user'] = var1

    # Проверяем отсыл данных
    if request.method == 'POST':
        args.update(csrf(request))
        # Имеются ли данные в строке
        ##############################################Плохо что данные не экранируются№№№№№№№№№№№№№№№№
        if request.POST['comments'] != '':

            messagePost = request.POST['comments']

            if int(id_user) == request.user.pk:
                args['errors'] = "Нельзя отсылать сообщение самому себе."
                return render(request, 'errors.html', args)

            # Создаем сообщение
            # Ищем пользователя в таблице пользователь переписка
            if var1 is not None:
                print ("search", var1)

                message_message.objects.create(
                    correspondents=var1,
                    massage=messagePost.encode('utf-8'),
                    user_send=request.user
                )
            else:

                if request.POST['team'] != '':
                    teamPost = request.POST['team']
                else:
                    teamPost = "Дружеское общение по интересам."

                save_massege_user = massege_user.objects.create(
                    user_one=request.user,
                    user_two=sendUser,
                    team=teamPost.encode('utf-8')
                )
                save_massege_user.save()

                message_message.objects.create(
                    correspondents=save_massege_user,
                    massage=messagePost.encode('utf-8'),
                    user_send=request.user
                )

            url = "/message/send/" + str(sendUser.pk) + "/"
            return redirect(url)

    return render(request, 'correspondents.html', args)
