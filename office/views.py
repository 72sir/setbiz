# -*- coding: utf8 -*-
import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.core.cache import cache
from django.template.context_processors import csrf
from accounts.models import User
from accounts.forms import AdminUserChangeForm, UserChangeForm
from django.utils import timezone
from logsys.models import UserWallet
from newMatrix.models import newMatrix_UserLargeDesk, newMatrix_smallDesk, newMatrix_UserDesk, \
    newMatrix_LargeDeskSmallDesk, newMatix_largeDesk
from office.models import Office_HistoryTransfer
from message.models import massege_user

# Главная странца кабинета
# /office/
from tovar.models import OrderProduct, OrderPaymentProduct, MatrixProduct


@login_required(login_url='/auth/login/')
def office(request, *args):
    if args is None or args == ():
        args = {}
    # Параметр меню
    args['bar'] = "office"
    # Проверим имеется ли у пользователя баланс
    try:
        ewallet = UserWallet.objects.get(UserWallet_user=request.user)
        args['balance'] = ewallet.UserWallet_walletPrice
    except ObjectDoesNotExist:
        args['balance'] = 0

    # Проверим новые сообщения для пользователя
    message = massege_user.objects.filter(Q(user_one=request.user) | Q(user_two=request.user))
    args['message'] = message.count

    # проверим структуру
    # проверим стол пользователя

    cache.delete('id_parent')
    cache.add('id_parent', request.user.pk)

    args['all_users'] = User.objects.all()

    #########################################################################
    # Проверка кошелька
    try:
        userWallet = UserWallet.objects.get(UserWallet_user=request.user)
        args['balance'] = userWallet.UserWallet_walletPrice
        args['iduserwallet'] = userWallet.pk

    except ObjectDoesNotExist:
        # Проверяем одинаковые ли пароли ввел пользователь.
        #############################################################################################
        # Пока что пароль не проверяется на макс и мин значений и вообще не проверяется и хранятся в открытом виде
        #############################################################################################
        args['errors_wallet'] = "Внутренний кошелек не активен. Бонусы и выплаты не начисляются. Активируйте кошелек."

    # Конец проверки кошелька
    #########################################################################

    #########################################################################
    # Выводим заказаный товар пользователя

    args['orderProducts'] = OrderProduct.objects.filter(user=request.user)

    args['orderProductsMatrix'] = MatrixProduct.objects.filter(user=request.user)

    # Конец вывода заказаного товара пользователя
    #########################################################################

    #########################################################################
    # Шаг ищем прикреплен ли пользователь к ГЛАВНОМУ столу заказов
    try:
        Desk = newMatrix_UserLargeDesk.objects.get(UserLargeDesk_User=request.user)
        args["desk"] = Desk.UserLargeDesk_Desk
        # Если да, то в шаблоне выделяем его красным
        args['parent'] = Desk.UserLargeDesk_User
        # Переносим в переменные все малые столы из главного стола

        if Desk.UserLargeDesk_Desk.largeDesk_RightDesk is not None:
            args["largeDeskRight"] = newMatrix_smallDesk.objects.get(
                pk=Desk.UserLargeDesk_Desk.largeDesk_RightDesk.pk)
        if Desk.UserLargeDesk_Desk.largeDesk_LeftDesk is not None:
            args["largeDeskLeft"] = newMatrix_smallDesk.objects.get(
                pk=Desk.UserLargeDesk_Desk.largeDesk_LeftDesk.pk)

    except ObjectDoesNotExist:
        try:
            # Смотрим зарегестрирован ли за пользователем МАЛЫЙ стол заказов
            Desk = newMatrix_UserDesk.objects.get(UserDesk_User=request.user)
            # Если да, то ищем большой стол заказов и передаем уже его
            Desk = newMatrix_LargeDeskSmallDesk.objects.get(LargeDeskSmallDesk_SmallDesk=Desk.UserDesk_Desk)
            Desk = Desk.LargeDeskSmallDesk_LargeDesk

            args["desk"] = Desk
            # Если да, то в шаблоне выделяем его красным
            args['parent'] = request.user
            # Переносим в переменные все малые столы из главного стола

            args["largeDeskRight"] = Desk.largeDesk_RightDesk
            args["largeDeskLeft"] = Desk.largeDesk_LeftDesk

        except ObjectDoesNotExist:
            # Тртьим шагом ищем стол родителя
            parent = request.user.parent
            bool = True

            while bool:
                # Ищем родителя в главном столе заказов
                try:
                    Desk = newMatrix_UserLargeDesk.objects.get(UserLargeDesk_User=parent)
                    args["desk"] = Desk.UserLargeDesk_Desk
                    # Если да, то в шаблоне выделяем его красным
                    args['parent'] = Desk.UserLargeDesk_User
                    # Переносим в переменные все малые столы из главного стола

                    if Desk.UserLargeDesk_Desk.largeDesk_RightDesk is not None:
                        args["largeDeskRight"] = newMatrix_smallDesk.objects.get(
                            pk=Desk.UserLargeDesk_Desk.largeDesk_RightDesk.pk)
                    if Desk.UserLargeDesk_Desk.largeDesk_LeftDesk is not None:
                        args["largeDeskLeft"] = newMatrix_smallDesk.objects.get(
                            pk=Desk.UserLargeDesk_Desk.largeDesk_LeftDesk.pk)
                    return render(request, 'office.html', args)

                except ObjectDoesNotExist:
                    # Ищем родителя в малом столе заказов
                    try:
                        # Смотрим зарегестрирован ли за пользователем МАЛЫЙ стол заказов
                        Desk = newMatrix_UserDesk.objects.get(UserDesk_User=parent)
                        # Если да, то ищем большой стол заказов и передаем уже его
                        Desk = newMatrix_LargeDeskSmallDesk.objects.get(
                            LargeDeskSmallDesk_SmallDesk=Desk.UserDesk_Desk)
                        Desk = Desk.LargeDeskSmallDesk_LargeDesk

                        args["desk"] = Desk
                        # Если да, то в шаблоне выделяем его красным
                        args['parent'] = parent
                        # Переносим в переменные все малые столы из главного стола

                        args["largeDeskRight"] = Desk.largeDesk_RightDesk
                        args["largeDeskLeft"] = Desk.largeDesk_LeftDesk
                        return render(request, 'office.html', args)

                    except ObjectDoesNotExist:
                        # Если родитель не найден не в малом не в главном то смотрим имеется ли у него родитель
                        # Если да, то ищем стол родителя 2
                        print("vvv --- ", parent)
                        if parent.parent is not None:
                            parent = parent.parent
                        else:
                            bool = False

            # раз в столе не зареган значить выводим случайный стол
            # Из таблицы СТОЛ - ПОЛЬЗОВАТЕЛЬ берем первую запись и выводим стол
            Desk = newMatrix_UserDesk.objects.all()
            Desk = Desk[0]
            args['parent'] = Desk.UserDesk_User
            # Ищем главный стол
            Desk = newMatrix_LargeDeskSmallDesk.objects.get(LargeDeskSmallDesk_SmallDesk=Desk.UserDesk_Desk)
            largeDesk = newMatix_largeDesk.objects.get(pk=Desk.LargeDeskSmallDesk_LargeDesk.pk)
            args["desk"] = largeDesk
            # Подтягиваем малые столы
            args["largeDeskLeft"] = largeDesk.largeDesk_LeftDesk
            args["largeDeskRight"] = largeDesk.largeDesk_RightDesk

    return render(request, 'office.html', args)


#############################################################################################
# url браузера - /office/wallet/
# Шаблон finance.html
# url(r'^wallet/$', views.wallet, name="wallet"),
# Проверяет пин и выводит всю нужную инфу в кошельке.
# Баланс. Пакеты на оплату.
#############################################################################################
@login_required(login_url='/auth/login/')
def wallet(request, *args):
    if not args:
        args = {}
    args['bar'] = "office"
    args.update(csrf(request))

    if request.user.is_active:
        # Данный try_get нужен для проверки существования у пользователя кошелька, если есть то делаем дела в нем
        # если нет, то первым делом нужно его создать.
        try:
            userWallet = UserWallet.objects.get(UserWallet_user=request.user)
            #############################################################################################
            # Плохо с защитой, так как в кеше можно просто проставить Труе и левый человек зайдет в кабинет
            # Пароль не шифрован, может предеаваться в массиве данных
            #############################################################################################

            if cache.get('wallet_user_commit') and cache.get('wallet_user_commit') == "True":
                args['balance'] = userWallet.UserWallet_walletPrice
                args['bonuce'] = userWallet.UserWallet_walletBonuce
                args['iduserwallet'] = userWallet.pk
                cache.add('wallet_user_commit', "True")

                return render(request, 'finance.html', args)

            if request.method == 'POST' and request.POST['pin']:
                if userWallet.UserWallet_password == request.POST['pin']:
                    args['balance'] = userWallet.UserWallet_walletPrice
                    args['bonuce'] = userWallet.UserWallet_walletBonuce
                    args['iduserwallet'] = userWallet.pk
                    cache.add('wallet_user_commit', "True")

                    return render(request, 'office.html', args)
            return render(request, 'InWallet.html', args)

        except ObjectDoesNotExist:
            # Проверяем одинаковые ли пароли ввел пользователь.
            #############################################################################################
            # Пока что пароль не проверяется на макс и мин значений и вообще не проверяется и хранятся в открытом виде
            #############################################################################################
            if request.method == 'POST' and request.POST['password1'] != request.POST['password2']:
                args['errors'] = "Ошибка. Пароли не совпадают."
                return render(request, 'createWallet.html', args)

            # Пользователя нет, значить пришли данные формы для создания нового пароля
            if request.method == 'POST':
                UserWallet.objects.create(
                    UserWallet_user=request.user,
                    UserWallet_password=request.POST['password1']
                )
                return redirect('/office/', args)

            else:
                return render(request, 'createWallet.html', args)

    return redirect('/auth/register/', args)


@login_required(login_url='/')
def changeInfo(request):
    args = {}
    args.update(csrf(request))
    user = User.objects.get(pk=request.user.id)

    args['bar'] = "office"
    args['username'] = user.username
    args['last_name'] = user.last_name
    args['first_name'] = user.first_name
    args['adress'] = user.adress
    args['city'] = user.city
    if user.birthday:
        args['birthday'] = user.birthday.strftime("%Y-%m-%d")
    args['avatar'] = user.avatar
    if user.phone_number:
        args['phone_number'] = int(user.phone_number)
    args['email'] = user.email

    if request.method == 'POST':
        form = UserChangeForm(request.POST)
        if form.is_valid():
            user.last_name = request.POST['last_name']
            user.first_name = request.POST['first_name']
            user.phone_number = request.POST['phone_number']
            user.city = request.POST['city']
            user.adress = request.POST['adress']
            user.save()
            return redirect('/office/changeInfo/')
        else:
            args['errors'] = form.errors
            return render(request, 'changeInfo.html', args)

    return render(request, 'changeInfo.html', args)


@login_required(login_url='/')
def sendmail(request):
    send_mail('Subject', 'Body', '72sir@mail.ru', ['72gsir@gmail.com'], fail_silently=False)
    return redirect('/office/')


######################################################################################
# Переводим валюту другому польователю
# /office/wallet/transfer/  - Перевести валюту
######################################################################################
def transferMoney(request, id_payKey='&&&&***9911', *args):
    if not args:
        args = {}
    args.update(csrf(request))
    args['bar'] = "office"

    # Проверяем все ли данные были высланы
    if request.method == "POST":
        # Первым делом ищем кошелек пользователя что бы сравнить пин
        userWallet = UserWallet.objects.get(UserWallet_user=request.user)
        # Проверяем больше ли нуля сумма
        if int(request.POST['usernameTransferWallet']) <= 0:
            args['errors'] = "Сумма перевода не корректна."
            return render(request, 'Transfer.html', args)

        else:
            # Проверяем пин
            if userWallet.UserWallet_password == request.POST.get('pin'):
                # Проверяем есть ли столько денежек на счету для перевода
                if userWallet.UserWallet_walletPrice < int(request.POST.get('usernameTransferWallet')):
                    args['errors'] = "На счету не достаточно средств. Пополните счет."
                    return render(request, 'Transfer.html', args)
                else:
                    # Если все хорошо, пин нужный на счету денежки есть, кошелек у пользователя создан
                    # переводим средства
                    try:
                        # Ищем кому переводить
                        userTransfer = User.objects.get(pk=int(id_payKey))
                        # Проверяем разные ли аккаунты то кто переводит и куда переводит
                        if request.user == userTransfer:
                            args['errors'] = "Не корректный ввод пользователя для перевода."
                            return render(request, 'Transfer.html', args)

                        # Ищем куда переводить
                        userWalletTransfers = UserWallet.objects.get(UserWallet_user=userTransfer)
                        # Вычитаем у пользователя средства
                        # i содержит количество денег пользователя
                        i = userWallet.UserWallet_walletPrice
                        UserWallet.objects.filter(UserWallet_user=request.user).update(
                            UserWallet_walletPrice=i - int(request.POST.get('usernameTransferWallet'))
                        )
                        # iTransfers содержит сумму денежек у пользователя которому переводим
                        iTransfers = userWalletTransfers.UserWallet_walletPrice
                        # Переводим денежки пользователю
                        UserWallet.objects.filter(UserWallet_user=userTransfer).update(
                            UserWallet_walletPrice=iTransfers + int(request.POST.get('usernameTransferWallet'))
                        )
                        # Создаем в истории переводов запись о диянии
                        Office_HistoryTransfer.objects.create(
                            # Кто перевел
                            HistoryTransfer_userTransfer=request.user,
                            # Кому перевел (сохраняю как интежер так как не 2 ключа выдают ошибку)
                            HistoryTransfer_userGets=userTransfer.pk,
                            # Сумма перевода
                            HistoryTransfer_TransferAmount=int(request.POST.get('usernameTransferWallet'))
                        )
                        return redirect('/office/wallet/')

                    except ObjectDoesNotExist:
                        args['id_payKey'] = "False"
                        args['id_payment'] = "transfer"
                        args['errors'] = "Пользователь не найден или у пользователя отсутствует электронный кошелек."
                        return render(request, 'Transfer.html', args)
            else:
                args['errors'] = "Ошибка PIN кода."
                return render(request, 'Transfer.html', args)

    else:
        # Данные не передаются выводим ошибку
        args['errors'] = "Данные не корректны."
        return render(request, 'Transfer.html', args)


######################################################################################
# Ищем и проверяем данные для перевода валюты
# /office/wallet/transfer/  - Перевести валюту
######################################################################################
def transfer(request, id_payKey='&&&&***9911', *args):
    if not args:
        args = {}
    args.update(csrf(request))
    args['bar'] = "office"
    # Первым делом ищем кошелек пользователя
    try:
        userWallet = UserWallet.objects.get(UserWallet_user=request.user)

        if id_payKey == '&&&&***9911' and not request.method == "POST":
            if request.POST.get('search_user_id'):
                # 1. Рассказать форме, что нас интересует перевод валюты другому пользователю
                args['id_payKey'] = "False"
                args['id_payment'] = "transfer"
                return render(request, 'Transfer.html', args)

            else:
                print ("1")
                # 1. Рассказать форме, что нас интересует перевод валюты другому пользователю
                args['id_payKey'] = "False"
                args['id_payment'] = "transfer"
                return render(request, 'Transfer.html', args)

        # Смотрим отсылались ли с формы какие нибудь данные
        elif id_payKey == '&&&&***9911' and request.method == "POST":
            if request.POST.get('search_user_id'):
                urls = "/office/wallet/transfer/" + request.POST.get('search_user_id') + "/"
                return redirect(urls)

            else:
                print ("2")
                # 1. Рассказать форме, что нас интересует перевод валюты другому пользователю
                args['id_payKey'] = "False"
                args['id_payment'] = "transfer"
                return render(request, 'Transfer.html', args)

        # Если ключ нам передавался значить ищем кошелек
        elif id_payKey != '&&&&***9911':
            try:
                # Выполняем поиск пользователя по ид которое пришло с формы
                userSearch = User.objects.get(pk=int(id_payKey))
                # Ищем кошелек пользователя которому нужные денежки
                userWalletSearch = UserWallet.objects.get(UserWallet_user=userSearch)
                # Передаем в форму баланс пользователя
                userWallet = UserWallet.objects.get(UserWallet_user=request.user)
                args['balance'] = userWallet.UserWallet_walletPrice

                # Если пользователя нашли и кошелек его нашли
                # То перезагружаем уже по ссылке со значением id_payKey
                # и передаем новую ссылку для формы

                args['userWalletSearch'] = userWalletSearch
                args['id_payKey'] = "True"
                args['id_payment'] = "transfer"
                args['urls'] = "/office/wallet/transfer/" + id_payKey + "/money/"

                return render(request, 'Transfer.html', args)

            except ObjectDoesNotExist:
                args['id_payKey'] = "False"
                args['id_payment'] = "transfer"
                args['errors'] = "Пользователь не найден или у пользователя отсутствует электронный кошелек."
                return render(request, 'Transfer.html', args)

    except ObjectDoesNotExist:
        print ("3 --  ")
        args['errors'] = "Ошибка профиля кошелька. Вам стоит обратиться к администратору."
        return render(request, 'office.html', args)


######################################################################################
# Функция для работы со средствами с баланса
# /office/wallet/payment/  - Оплатить валютой
######################################################################################
@login_required(login_url='/')
def payment(request, *args):
    if not args:
        args = {}

    args.update(csrf(request))
    args['bar'] = "office"

    if request.method == "POST":
        if request.POST['paymentKey']:
            url = request.POST['paymentKey']
            return redirect("/office/wallet/payment/" + url + "/", args)

    return render(request, 'TransferPaymentCurrency.html', args)


######################################################################################
# Оплата товара по ключу
# если пакет найден вводим пин код и оплачиваем пакет
######################################################################################
@login_required(login_url='/')
def payment_key(request, id_payKey=1, *args, **kwargs):
    if not args:
        args = {}
    args.update(csrf(request))
    args['bar'] = "office"

    # Проверяем на наличие в базе
    orderProduct = get_object_or_404(OrderProduct, activation_key=id_payKey)
    # Если товар активирован то выдаем ошибку что товар уже проплачен
    if orderProduct.payment:
        args['errors_payment'] = "Продукт уже проплачен. Введите для поиска не оплаченный продукт."
        return render(request, 'TransferPaymentCurrency.html', args)

    wallet = get_object_or_404(UserWallet, UserWallet_user=request.user)

    args['orderProduct'] = orderProduct
    args['wallet'] = wallet

    if request.method == "POST":
        if request.POST['key_product'] and request.POST['pin']:
            ### Находим кошелек
            userWallet = UserWallet.objects.get(UserWallet_user=request.user)
            # Проверяем пин код
            if str(userWallet.UserWallet_password) == request.POST['pin']:
                ### Проводим оплату пакета если хватает средств
                if wallet.UserWallet_walletPrice >= orderProduct.product.price:
                    money = wallet.UserWallet_walletPrice
                    UserWallet.objects.filter(UserWallet_user=request.user).update(UserWallet_walletPrice=money-orderProduct.product.price)
                    OrderProduct.objects.filter(activation_key=id_payKey).update(
                        status="Оплачен. Ожидаем отклик партнера по отправке товара",
                        payment=True
                    )
                    ########### добавляем товар в таблицу по реализации товара
                    OrderPaymentProduct.objects.create(
                        userPayment=request.user,
                        product=orderProduct
                    )
                    ########### закончили добавление товара на реализацию

                else:
                    args['no_money'] = "На вашем счету не хватает денежных средств для оплаты заказа."
                    return render(request, 'searchOrderKey.html', args)

                # и ставим что пакет активен ожидает
                orderProduct = get_object_or_404(OrderProduct, activation_key=request.POST['key_product'])
                return redirect("/office/")
            else:
                args['error_pin'] = "Не верный пин код."
                return render(request, 'searchOrderKey.html', args)

    return render(request, 'searchOrderKey.html', args)


######################################################################################
# Функция оплаты пакета по ключу оплаты
# /office/wallet/pay/
######################################################################################
@login_required(login_url='/')
def payKey(request, *args):
    if not args:
        args = {}
    args.update(csrf(request))

    if request.method == "POST":
        if request.POST['key_product'] and request.POST['pin']:
            ### Находим кошелек
            userWallet = UserWallet.objects.get(UserWallet_user=request.user)
            # Проверяем пин код
            if str(userWallet.UserWallet_password) == request.POST['pin']:
                orderProduct = get_object_or_404(OrderProduct, activation_key=request.POST['key_product'])
                return redirect("/office/", args)
            else:
                args['error_pin'] = "Не верный пин код."
                return redirect("/office/wallet/payment/" + request.POST['key_product'] + "/", args, {'error_pin': "Не верный пин код."})

    return redirect('/office/')


@login_required(login_url='/')
def deleteKey(request, id_deleteKey=0, *args):
    ##########################################################################################################
    # Ограничить удаление пакетов, иначе можно удалять и тут же регистрировать новый.
    # Перегружая серевер.
    ##########################################################################################################
    if not args:
        args = {}

    return redirect('/office/')


#################################################################
# поиск анкеты другого пользователя
@login_required(login_url='/')
def anketa(request, id_user=0, *args):
    args = {}
    args['bar'] = "office"

    try:
        user_search = User.objects.get(pk=id_user)
        args['user_search'] = user_search

        # Шаг ищем прикреплен ли пользователь к ГЛАВНОМУ столу заказов
        try:
            Desk = newMatrix_UserLargeDesk.objects.get(UserLargeDesk_User=user_search)
            args["desk"] = Desk.UserLargeDesk_Desk
            # Если да, то в шаблоне выделяем его красным
            args['parent'] = Desk.UserLargeDesk_User
            # Переносим в переменные все малые столы из главного стола
            # 1 малый стол
            if Desk.UserLargeDesk_Desk.largeDesk_RightDesk is not None:
                args["largeDeskRight"] = newMatrix_smallDesk.objects.get(
                    pk=Desk.UserLargeDesk_Desk.largeDesk_RightDesk.pk)
            # 2 малый стол
            if Desk.UserLargeDesk_Desk.largeDesk_LeftDesk is not None:
                args["largeDeskLeft"] = newMatrix_smallDesk.objects.get(
                    pk=Desk.UserLargeDesk_Desk.largeDesk_LeftDesk.pk)

        except ObjectDoesNotExist:
            try:
                # Смотрим зарегестрирован ли за пользователем МАЛЫЙ стол заказов
                Desk = newMatrix_UserDesk.objects.get(UserDesk_User=user_search)
                # Если да, то ищем большой стол заказов и передаем уже его
                Desk = newMatrix_LargeDeskSmallDesk.objects.get(LargeDeskSmallDesk_SmallDesk=Desk.UserDesk_Desk)
                Desk = Desk.LargeDeskSmallDesk_LargeDesk

                args["desk"] = Desk
                # Если да, то в шаблоне выделяем его красным
                args['parent'] = user_search
                # Переносим в переменные все малые столы из главного стола

                args["largeDeskRight"] = Desk.largeDesk_RightDesk
                args["largeDeskLeft"] = Desk.largeDesk_LeftDesk

            except ObjectDoesNotExist:
                # Тртьим шагом ищем стол родителя
                parent = user_search.parent
                bool = True

                while bool:
                    # Ищем родителя в главном столе заказов
                    try:
                        Desk = newMatrix_UserLargeDesk.objects.get(UserLargeDesk_User=parent)
                        args["desk"] = Desk.UserLargeDesk_Desk
                        # Если да, то в шаблоне выделяем его красным
                        args['parent'] = Desk.UserLargeDesk_User
                        # Переносим в переменные все малые столы из главного стола

                        if Desk.UserLargeDesk_Desk.largeDesk_RightDesk is not None:
                            args["largeDeskRight"] = newMatrix_smallDesk.objects.get(
                                pk=Desk.UserLargeDesk_Desk.largeDesk_RightDesk.pk)
                        if Desk.UserLargeDesk_Desk.largeDesk_LeftDesk is not None:
                            args["largeDeskLeft"] = newMatrix_smallDesk.objects.get(
                                pk=Desk.UserLargeDesk_Desk.largeDesk_LeftDesk.pk)
                        return render(request, 'anketa_search.html', args)

                    except ObjectDoesNotExist:
                        # Ищем родителя в малом столе заказов
                        try:
                            # Смотрим зарегестрирован ли за пользователем МАЛЫЙ стол заказов
                            Desk = newMatrix_UserDesk.objects.get(UserDesk_User=parent)
                            # Если да, то ищем большой стол заказов и передаем уже его
                            Desk = newMatrix_LargeDeskSmallDesk.objects.get(
                                LargeDeskSmallDesk_SmallDesk=Desk.UserDesk_Desk)
                            Desk = Desk.LargeDeskSmallDesk_LargeDesk

                            args["desk"] = Desk
                            # Если да, то в шаблоне выделяем его красным
                            args['parent'] = parent
                            # Переносим в переменные все малые столы из главного стола

                            args["largeDeskRight"] = Desk.largeDesk_RightDesk
                            args["largeDeskLeft"] = Desk.largeDesk_LeftDesk
                            return render(request, 'anketa_search.html', args)

                        except ObjectDoesNotExist:
                            # Если родитель не найден не в малом не в главном то смотрим имеется ли у него родитель
                            # Если да, то ищем стол родителя
                            print("1 --- ", parent)
                            if parent is not None:
                                if parent.parent is not None:
                                    parent = parent.parent
                                else:
                                    bool = False
                            else:
                                bool = False

                # раз в столе не зареган значить выводим случайный стол
                # Из таблицы СТОЛ - ПОЛЬЗОВАТЕЛЬ берем первую запись и выводим стол
                Desk = newMatrix_UserDesk.objects.all()
                Desk = Desk[0]
                args['parent'] = Desk.UserDesk_User
                # Ищем главный стол
                Desk = newMatrix_LargeDeskSmallDesk.objects.get(LargeDeskSmallDesk_SmallDesk=Desk.UserDesk_Desk)
                largeDesk = newMatix_largeDesk.objects.get(pk=Desk.LargeDeskSmallDesk_LargeDesk.pk)
                args["desk"] = largeDesk
                # Подтягиваем малые столы
                args["largeDeskLeft"] = largeDesk.largeDesk_LeftDesk
                args["largeDeskRight"] = largeDesk.largeDesk_RightDesk

        return render(request, 'anketa_search.html', args)

    except ObjectDoesNotExist:
        args['errors'] = "Такого пользователя не найдено."

    return render(request, 'anketa_search.html', args)
