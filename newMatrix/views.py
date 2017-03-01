# coding: utf-8
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from logsys.models import UserWallet
from newMatrix.models import newMatrix_UserDesk, newMatix_largeDesk, newMatrix_smallDesk, newMatrix_UserLargeDesk, \
    newMatrix_LargeDeskSmallDesk, newMatrix_freePlaceSmallDesk
from django.core.urlresolvers import reverse, resolve


# Create your views here.


######################################################################
# Главная страница нового матричного маркетинга
######################################################################
from tovar.models import MatrixProduct


@login_required(login_url='/auth/login/')
def newMatrix_index(request, *args, **kwargs):
    if not args:
        args = {}
    args['bar'] = "marketing"

    # Шаг ищем прикреплен ли пользователь к ГЛАВНОМУ столу заказов
    try:
        Desk = newMatrix_UserLargeDesk.objects.get(UserLargeDesk_User=request.user)
        args["desk"] = Desk.UserLargeDesk_Desk
        # Если да, то в шаблоне выделяем его красным
        args['parent'] = Desk.UserLargeDesk_User
        # Переносим в переменные все малые столы из главного стола

        if Desk.UserLargeDesk_Desk.largeDesk_RightDesk is not None:
            args["largeDeskRight"] = newMatrix_smallDesk.objects.get(pk=Desk.UserLargeDesk_Desk.largeDesk_RightDesk.pk)
        if Desk.UserLargeDesk_Desk.largeDesk_LeftDesk is not None:
            args["largeDeskLeft"] = newMatrix_smallDesk.objects.get(pk=Desk.UserLargeDesk_Desk.largeDesk_LeftDesk.pk)

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
                    return render(request, 'newMatrix_index.html', args)

                except ObjectDoesNotExist:
                    # Ищем родителя в малом столе заказов
                    try:
                        # Смотрим зарегестрирован ли за пользователем МАЛЫЙ стол заказов
                        Desk = newMatrix_UserDesk.objects.get(UserDesk_User=parent)
                        # Если да, то ищем большой стол заказов и передаем уже его
                        Desk = newMatrix_LargeDeskSmallDesk.objects.get(LargeDeskSmallDesk_SmallDesk=Desk.UserDesk_Desk)
                        Desk = Desk.LargeDeskSmallDesk_LargeDesk

                        args["desk"] = Desk
                        # Если да, то в шаблоне выделяем его красным
                        args['parent'] = parent
                        # Переносим в переменные все малые столы из главного стола

                        args["largeDeskRight"] = Desk.largeDesk_RightDesk
                        args["largeDeskLeft"] = Desk.largeDesk_LeftDesk
                        return render(request, 'newMatrix_index.html', args)

                    except ObjectDoesNotExist:
                        # Если родитель не найден не в малом не в главном то смотрим имеется ли у него родитель
                        # Если да, то ищем стол родителя
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

    return render(request, 'newMatrix_index.html', args)


######################################################################
# Передаем параметр малого стола и текущего пользователя для регистрации
# 4 шаг Закрываем малый стол и открываем новый большой стол
######################################################################
def newMatrix_closeSmallDesk(request, small_desk, *args):
    if not args:
        args = {}

    # Здесь проверяем пришли ли данные по столу
    if not small_desk:
        args['errors'] = "#55445. Кретическая ситуация - для регистрации не был передан малый стол заказов."
        args['url_'] = "/office/"
        return render(request, 'errors.html', args)

    else:
        # Находим большой стол
        largeDesk = newMatrix_LargeDeskSmallDesk.objects.get(pk=small_desk.pk)
        largeDesk = largeDesk.LargeDeskSmallDesk_LargeDesk

        print ("Wallet4 ok")

        ########################################################################################################
        # Начисляем пользователю в голове денежек за закрытый малый стол
        # пока сумму возьмем в 1500 тысячи рублей

        # Нашли пользователя в голове
        moneyUser = largeDesk.largeDesk_User
        # Находим сумму для начисления
        if largeDesk.largeDesk_RightDesk is not None:
            print ("largeDesk.largeDesk_RightDesk ok", largeDesk.largeDesk_RightDesk)
            moneySum = int(largeDesk.largeDesk_RightDesk.smallDesk_matrixMoneyPay.outMatrix)
        else:
            print ("largeDesk.largeDesk_LeftDesk ok", largeDesk.largeDesk_LeftDesk)
            moneySum = int(largeDesk.largeDesk_LeftDesk.smallDesk_matrixMoneyPay.outMatrix)
        # Ищем кошелек пользователя в голове
        moneyUserWallet = UserWallet.objects.get(UserWallet_user=moneyUser)
        # Запоминаем его денежки и прибовляем 1500 рублей
        money = int(moneyUserWallet.UserWallet_walletPrice)

        UserWallet.objects.filter(UserWallet_user=moneyUser).update(UserWallet_walletPrice=money + moneySum)

        # Начисляем денежки родителям вверх на 5 уровней по 100 валюты
        ########################################################################################################

        # Ищем место нахождение малого стола в большом
        if largeDesk.largeDesk_RightDesk is not None:
            print ("largeDesk ok")
            if largeDesk.largeDesk_RightDesk == small_desk:
                placeSmallDeskInLargeDesk = "RightDesk"
                largeDesk.largeDesk_RightDesk = None
        else:
            print ("largeDesk2 ok")
            placeSmallDeskInLargeDesk = "LeftDesk"
            largeDesk.largeDesk_LeftDesk = None
            print ("largeDesk3 ok")

        print ("largeDesk4 ok")

        # Проверяем малый стол, действительно ли пришло время его удалить
        small_desk = newMatrix_smallDesk.objects.get(pk=small_desk.pk)

        print ("Wallet5 ok")

        print ("Wallet6 ok")
        parent = moneyUser
        i = 5


        while i > 0:
            # Если родителя закончились то обрываем цикл
            if parent.parent is None:
                i = 0
            else:
                # Если родитель есть то вычитваем единицу
                i -= 1
                # Находим родителя
                parent = parent.parent
                # Находим его кошелек и начисляем денег UserWallet_walletPrice
                parentWallet = UserWallet.objects.filter(UserWallet_user=parent)
                if parentWallet.count() > 0:
                    parentWallet = int(parentWallet[0].UserWallet_walletPrice)
                    UserWallet.objects.filter(UserWallet_user=parent).update(UserWallet_walletPrice=parentWallet+100)

        # Закончили начисление в голову денежек
        ########################################################################################################

        if small_desk.smallDesk_RightPlace is not None and small_desk.smallDesk_LeftPlace is not None:
            # Удаляем малый стол из плеча большого стола
            if placeSmallDeskInLargeDesk == "LeftDesk":
                newMatix_largeDesk.objects.filter(pk=largeDesk.pk).update(largeDesk_LeftDesk=None)
            elif placeSmallDeskInLargeDesk == "RightDesk":
                newMatix_largeDesk.objects.filter(pk=largeDesk.pk).update(largeDesk_RightDesk=None)

            # удаляем связь ПОЛЬЗОВАТЕЛЬ - Маленький СТОЛ
            newMatrix_UserDesk.objects.filter(UserDesk_User=small_desk.smallDesk_UserInHead).delete()
            newMatrix_UserDesk.objects.filter(UserDesk_User=small_desk.smallDesk_RightPlace).delete()
            newMatrix_UserDesk.objects.filter(UserDesk_User=small_desk.smallDesk_LeftPlace).delete()

            # Малый стол убрали из большого нужно убрать свзяь большой = малый стол
            newMatrix_LargeDeskSmallDesk.objects.filter(LargeDeskSmallDesk_SmallDesk=small_desk).delete()
            # Удаляем связь малый стол = места
            newMatrix_freePlaceSmallDesk.objects.filter(freeSpaceSmallDesk_smallDesk=small_desk).delete()

            ######################## Создаем малые столы ##############################################
            # Создаем новый малые столы с пользователями из плеч в головах
            newsmallDesk_LeftPlace = newMatrix_smallDesk.objects.create(
                smallDesk_UserInHead=small_desk.smallDesk_LeftPlace
            )
            newsmallDesk_LeftPlace.save()
            newsmallDesk_RightPlace = newMatrix_smallDesk.objects.create(
                smallDesk_UserInHead=small_desk.smallDesk_RightPlace
            )
            newsmallDesk_RightPlace.save()
            ######################## свободные места в малых столах ##############################################
            newMatrix_freePlaceSmallDesk.objects.create(
                freeSpaceSmallDesk_smallDesk=newsmallDesk_LeftPlace,
                freeSpaceSmallDesk_freePlace=2
            )
            newMatrix_freePlaceSmallDesk.objects.create(
                freeSpaceSmallDesk_smallDesk=newsmallDesk_RightPlace,
                freeSpaceSmallDesk_freePlace=2
            )
            ####################### создаем большой стол заказов #########################################################
            new_largeDesk = newMatix_largeDesk.objects.create(
                largeDesk_User=small_desk.smallDesk_UserInHead,
                largeDesk_RightDesk=newsmallDesk_RightPlace,
                largeDesk_LeftDesk=newsmallDesk_LeftPlace
            )
            new_largeDesk.save()

            # создаем связь большой стол - пользовательи
            newMatrix_UserLargeDesk.objects.create(
                UserLargeDesk_User=small_desk.smallDesk_UserInHead,
                UserLargeDesk_Desk=new_largeDesk
            )
            # Создаем связь малый стол - пользователь
            newMatrix_UserDesk.objects.create(
                UserDesk_Desk=newsmallDesk_LeftPlace,
                UserDesk_User=small_desk.smallDesk_LeftPlace
            )
            newMatrix_UserDesk.objects.create(
                UserDesk_Desk=newsmallDesk_RightPlace,
                UserDesk_User=small_desk.smallDesk_RightPlace
            )
            # Создаем связь малый стол - большой стол
            newMatrix_LargeDeskSmallDesk.objects.create(
                LargeDeskSmallDesk_SmallDesk=newsmallDesk_LeftPlace,
                LargeDeskSmallDesk_LargeDesk=new_largeDesk
            )
            newMatrix_LargeDeskSmallDesk.objects.create(
                LargeDeskSmallDesk_SmallDesk=newsmallDesk_RightPlace,
                LargeDeskSmallDesk_LargeDesk=new_largeDesk
            )

            # удаляем малый стол
            newMatrix_smallDesk.objects.filter(pk=small_desk.pk).delete()

            ##################### Проверка нужно ли удалять главный стол заказов ##########################
            largeDesk = newMatix_largeDesk.objects.get(pk=largeDesk.pk)
            if largeDesk.largeDesk_RightDesk is None and largeDesk.largeDesk_LeftDesk is None:
                print ("Del head desk")
                ############################### Начисляем пользователю денежку и
                ####################################################################
                # удаляем главную таблицу и связь главное и пользователя
                newMatrix_UserLargeDesk.objects.filter(pk=largeDesk.largeDesk_User.pk).delete()
                newMatix_largeDesk.objects.filter(pk=largeDesk.pk).delete()
                print ("Wallet8 ok")


        else:
            args['errors'] = "#55446. В мало столе не все места заняты, обратитесь к администратору."
            args['url_'] = "/office/"
            return render(request, 'errors.html', args)

    return redirect('/office/')


######################################################################
# Передаем параметр малого стола и текущего пользователя для регистрации
# 3 шаг регистрация пользователя в мало столе
######################################################################
def newMatrix_addUserSmallDesk(request, smallDesk=None, *args):
    if not args:
        args = {}

    # Здесь проверяем пришли ли данные по столу
    if not smallDesk:
        args['errors'] = "Кретическая ситуация - для регистрации не был передан малый стол заказов."
        args['url_'] = "/office/"
        return render(request, 'errors.html', args)

    # Ищем свободное место в малом столе заказов
    else:

        print ("Wallet ok")
        ####################################
        # Проверяем имеются ли денюжки и активирован ли кошелек
        try:
            WalletUser = UserWallet.objects.get(UserWallet_user=request.user)
            # Кошелек активен проверяем хватает ли денежек для активации
            money = int(WalletUser.UserWallet_walletPrice)
            moneyInDesk = get_object_or_404(newMatrix_smallDesk, pk=smallDesk.pk)

            if money < int(moneyInDesk.smallDesk_matrixMoneyPay.inMatrix):
                ############### Не хватает денег
                args['errors'] = "В кошельке не хватает денег."
                args['bar'] = "index"
                args['url_'] = "/office/"
                return render(request, 'errors.html', args)
            else:
                # Кошелек активен вычитаем денюжки за вход в стол заказов
                UserWallet.objects.filter(UserWallet_user=request.user).update(
                    UserWallet_walletPrice=money - int(moneyInDesk.smallDesk_matrixMoneyPay.inMatrix)
                )
                ###############################
                # начислеям пользователю товар стола
                MatrixProduct.objects.create(
                    user = request.user,
                    product = moneyInDesk.smallDesk_matrixMoneyPay.tovarMatrix
                )

                # закончили начисление
                ###############################

                #############################################################################################################

        except ObjectDoesNotExist:
            ############### Кошелек не активен
            args['errors'] = "Кошелек не активен."
            args['bar'] = "index"
            args['url_'] = "/office/"
            return render(request, 'errors.html', args)

        # закончили проверку кошелька
        ####################################

        print ("Wallet3 ok")

        # Ищем свободную сторону малого стола и регистрируем пользователя.
        if smallDesk.smallDesk_LeftPlace is None:
            newMatrix_smallDesk.objects.filter(pk=smallDesk.pk).update(smallDesk_LeftPlace=request.user)
        elif smallDesk.smallDesk_RightPlace is None:
            newMatrix_smallDesk.objects.filter(pk=smallDesk.pk).update(smallDesk_RightPlace=request.user)
        else:
            args['errors'] = "#55443. Кретическая ситуация - для регистрации не было найдено " \
                             "свободных мест в малом столе заказов."
            args['url_'] = "/office/"
            return render(request, 'errors.html', args)

    # Удалить 1 свободное место в мало столе и проверить нужно ли малый закрыть
    freePlaceSmallDesk = newMatrix_freePlaceSmallDesk.objects.get(pk=smallDesk.pk)

    newMatrix_freePlaceSmallDesk.objects.filter(pk=smallDesk.pk).update(
        freeSpaceSmallDesk_freePlace=freePlaceSmallDesk.freeSpaceSmallDesk_freePlace - 1)
    # СОздаем связь малый стол = пользователь
    newMatrix_UserDesk.objects.create(
        UserDesk_User=request.user,
        UserDesk_Desk=smallDesk
    )
    # Проверяем нужн ли малый стол закрыть
    freePlaceSmallDesk = newMatrix_freePlaceSmallDesk.objects.get(pk=smallDesk.pk)

    # Закрываем малый стол заказов
    if int(freePlaceSmallDesk.freeSpaceSmallDesk_freePlace) <= 0:
        return newMatrix_closeSmallDesk(request, smallDesk, args)
    else:
        return redirect('/office/')


######################################################################
# Ищем свободное место в столе заказов по найденному ид сонсора
# 2 шаг поиск свободного места
######################################################################
def newMatrix_FreePlace(request, largeDeskParent, parent, *args):
    if not args:
        args = {}

    # Проверяем все ли параметры до нас дошли
    if not largeDeskParent or not parent or (not largeDeskParent and not parent):
        args['errors'] = "Кретическая ситуация обратитесь к администратору сайта."
        args['url_'] = "/office/"
        return render(request, 'errors.html', args)

    # Параметры пришли все, значить можно начинать поиск свободного места
    else:
        # Родитель в глове главного стла
        if largeDeskParent.largeDesk_User == parent:
            # Проверяем имеется ли у нашего главного стола левый малый стол
            if largeDeskParent.largeDesk_LeftDesk:
                return newMatrix_addUserSmallDesk(request, largeDeskParent.largeDesk_LeftDesk, args)

            # Иначе смотрим имеется ли главного стола правый малый стол
            elif largeDeskParent.largeDesk_RightDesk:
                return newMatrix_addUserSmallDesk(request, largeDeskParent.largeDesk_RightDesk, args)

            # Иначе критическая ситуация, по идее не возможная
            else:
                args['errors'] = "Кретическая ситуация, в данном столе отсутствуют свободные места."
                args['url_'] = "/office/"
                return render(request, 'errors.html', args)



        ####################################################################
        # Проверяем существует ли правый малый стол заказов
        if largeDeskParent.largeDesk_RightDesk:

            # Родитель в глове правого Малого стола
            if largeDeskParent.largeDesk_RightDesk.smallDesk_UserInHead == parent:
                return newMatrix_addUserSmallDesk(request, largeDeskParent.largeDesk_RightDesk, args)

            # Родитель в правом плече правого малого стла
            elif largeDeskParent.largeDesk_RightDesk.smallDesk_RightPlace == parent:
                return newMatrix_addUserSmallDesk(request, largeDeskParent.largeDesk_RightDesk, args)

            # Родитель в левом плече правого малого стла
            elif largeDeskParent.largeDesk_RightDesk.smallDesk_LeftPlace == parent:
                return newMatrix_addUserSmallDesk(request, largeDeskParent.largeDesk_RightDesk, args)

        ####################################################################
        # Проверяем существует ли левый малый стол заказов
        elif largeDeskParent.largeDesk_LeftDesk:

            # Родитель в глове левого Малого стла
            if largeDeskParent.largeDesk_LeftDesk.smallDesk_UserInHead == parent:
                return newMatrix_addUserSmallDesk(request, largeDeskParent.largeDesk_LeftDesk, args)

            # Родитель в правом плече левого Малого стла
            elif largeDeskParent.largeDesk_LeftDesk.smallDesk_RightPlace == parent:
                return newMatrix_addUserSmallDesk(request, largeDeskParent.largeDesk_LeftDesk, args)

            # Родитель в левом плече левого Малого стла
            elif largeDeskParent.largeDesk_LeftDesk.smallDesk_LeftPlace == parent:
                return newMatrix_addUserSmallDesk(request, largeDeskParent.largeDesk_LeftDesk, args)

        else:
            args['errors'] = "#55444. Кретическая ситуация, не найдено свободное место в столе, " \
                             "обратитесь к администратору сайта."
            args['url_'] = "/office/"
            return render(request, 'errors.html', args)


######################################################################
# Ищем большой стол зказов в котором находится ид спонсора
# 1 шаг поиск большого стола спонсора
######################################################################
@login_required(login_url='/auth/login/')
def newMatrix_SearchUserInLargeDesk(request, id_desk=0, *args):
    if not args:
        args = {}

    try:
        # Проверяем зарегестрирован ли пользователь в большом столе заказов
        newMatrix_UserLargeDesk.objects.get(UserLargeDesk_User=request.user)

        args['errors'] = "Пользователь уже находится в столе заказов."
        args['url_'] = "/office/"
        return render(request, 'errors.html', args)

    except ObjectDoesNotExist:
        # Проверяем пользователя на наличие стола в таблице польователь - маленькоий стол заказов
        try:
            # Смотрим зарегестрирован ли за пользователем в маленьком столе
            newMatrix_UserDesk.objects.get(UserDesk_User=request.user)
            args['errors'] = "Пользователь уже находится в столе заказов."
            args['url_'] = "/office/"
            return render(request, 'errors.html', args)

        # Если стола у пользователя нет, значить ищем стол спонсора
        except ObjectDoesNotExist:
            # Нужно узнать родитель находится в большом столе или в одном из малых столов заказов
            try:
                parent = newMatrix_UserLargeDesk.objects.get(UserLargeDesk_User_id=int(id_desk))
                # Отфильтровываем стол и родителя
                largeDeskParent = parent.UserLargeDesk_Desk
                parent = parent.UserLargeDesk_User
                # Передаем параметры - большой стол - родител
                return newMatrix_FreePlace(request, largeDeskParent, parent)

            except ObjectDoesNotExist:
                try:
                    # Ищем родителя в малом стoле заказов по параметру id_desk
                    parent = newMatrix_UserDesk.objects.get(UserDesk_User_id=int(id_desk))
                    #
                    largeDeskParent = newMatrix_LargeDeskSmallDesk.objects.get(
                        LargeDeskSmallDesk_SmallDesk_id=parent.UserDesk_Desk.pk)
                    # После чего largeDeskParent имеет ссылку на большой стол заказов

                    largeDeskParent = largeDeskParent.LargeDeskSmallDesk_LargeDesk
                    parent = parent.UserDesk_User
                    # Передаем параметры - большой стол - родител
                    return newMatrix_FreePlace(request, largeDeskParent, parent)

                except ObjectDoesNotExist:
                    args['errors'] = "У данного спонсора отсутствует стол заказов."
                    args['url_'] = "/office/"
                    return render(request, 'errors.html', args)
