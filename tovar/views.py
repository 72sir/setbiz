# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
import hashlib, datetime, random

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import csrf

from tovar.models import Product, Attribute, OrderProduct, FotoTovar
from django.utils import timezone
from accounts.models import User


# Create your views here.


###################################################################
# Вся продукция
def product(request, *args, **kwargs):
    # Проверяем передавались ли нам параметры
    # если нет то активируем переменную
    if args is None:
        args = {}
    # Выбираем из базы данные и передаем в переменную
    products = Product.objects.filter(company_id=4, published_date__lte=timezone.now()).order_by('published_date')[:3]
    # Передаем все данные в шаблон
    infotovars = Attribute.objects.filter(destination=True)
    samsung = Product.objects.filter(company_id=25, published_date__lte=timezone.now()).order_by('published_date')[:3]

    virt = Product.objects.filter(destination_id=33, published_date__lte=timezone.now()).order_by('published_date')[:3]

    return render(request, 'product.html', {'products': products, 'infotovars': infotovars, 'samsung': samsung,
                                            'bar': "katalog_bar", 'virt': virt})


###################################################################
# Продукция по назначению
def view_destination(request, id_destination=None, *args, **kwargs):
    # Проверяем на наличие destination в базе
    destination = get_object_or_404(Attribute, pk=id_destination)
    products = Product.objects.filter(destination_id=id_destination)
    # база не поддерживает на прямую distinct и ForeigenKey
    infotovarscompany = Product.objects.filter(destination_id=id_destination) \
        .values('company__name', 'company').distinct().order_by('company')

    return render(request, 'product.html',
                  {'products': products, 'infotovarscompany': infotovarscompany, 'id_destination': id_destination
                      , 'destination': destination,
                   'bar': "katalog_bar"})


###################################################################
# Прдукция по компании
def view_company(request, id_destination=None, id_company=None, *args, **kwargs):
    # Проверяем на наличие destination в базе
    destination = get_object_or_404(Attribute, pk=id_destination)
    # Проверяем на наличие company в базе
    company = get_object_or_404(Attribute, pk=id_company)
    # Делаем выборку в запросе по нужным товарам
    products = Product.objects.filter(destination_id=id_destination, company_id=id_company)
    # база не поддерживает на прямую distinct и ForeigenKey
    # ищем всякие хитрые методы
    infotovarstype = Product.objects.filter(destination_id=id_destination, company_id=id_company) \
        .values('type__name', 'type').distinct().order_by('type')
    #     products - Выборка продукта по запросу
    #     infotovarstype - выборка уникальных значений для левого меню
    #     id_destination - требуется при построеннии ссылки на тип товара в левом меню
    #     id_company - требуется при построеннии ссылки на тип товара в левом меню

    string = u'' + products[0].destination.name + u' фирмы ' + products[0].company.name
    return render(request, 'product.html',
                  {'products': products, 'infotovarstype': infotovarstype, 'id_destination': id_destination,
                   'id_company': id_company, 'nameUrl': string, 'destination': destination, 'company': company,
                   'bar': "katalog_bar"})


###################################################################
# Продукция по типу
def view_type(request, id_destination=None, id_company=None, id_type=None, *args, **kwargs):
    # Проверяем на наличие destination в базе
    destination = get_object_or_404(Attribute, pk=id_destination)
    # Проверяем на наличие company в базе
    company = get_object_or_404(Attribute, pk=id_company)
    # Проверяем на наличие type в базе
    type = get_object_or_404(Attribute, pk=id_type)
    # Делаем выборку в запросе по нужным товарам
    products = Product.objects.filter(destination_id=id_destination, company_id=id_company, type=id_type)
    # база не поддерживает на прямую distinct и ForeigenKey
    # ищем всякие хитрые методы
    infotovarsmodel = Product.objects.filter(destination_id=id_destination, company_id=id_company, type=id_type) \
        .values('model__name', 'model').distinct().order_by('model')
    #     products - Выборка продукта по запросу
    #     infotovarsmodel - выборка уникальных значений для левого меню
    #     id_type - требуется при построеннии ссылки на тип товара в левом меню
    #     id_destination - требуется при построеннии ссылки на тип товара в левом меню
    #     id_company - требуется при построеннии ссылки на тип товара в левом меню
    string = u'' + products[0].destination.name + u' фирмы ' + products[0].company.name + u' товар ' \
             + products[0].type.name
    return render(request, 'product.html',
                  {'products': products, 'id_type': id_type, 'id_destination': id_destination,
                   'id_company': id_company, 'infotovarsmodel': infotovarsmodel, 'nameUrl': string,
                   'destination': destination, 'company': company, 'type': type, 'bar': "katalog_bar"})


###################################################################
# Показываем товар
def view_model(request, id_destination=None, id_company=None, id_type=None, id_model=None, *args, **kwargs):
    # Проверяем на наличие destination в базе
    destination = get_object_or_404(Attribute, pk=id_destination)
    # Проверяем на наличие company в базе
    company = get_object_or_404(Attribute, pk=id_company)
    # Проверяем на наличие type в базе
    type = get_object_or_404(Attribute, pk=id_type)
    # Проверяем на наличие model в базе
    model = get_object_or_404(Attribute, pk=id_model)

    # Делаем выборку в запросе по нужным товарам
    products = Product.objects.filter(destination_id=id_destination, company_id=id_company, type=id_type,
                                      model=id_model)
    # база не поддерживает на прямую distinct и ForeigenKey
    # ищем всякие хитрые методы
    infotovarsmodel = Product.objects.filter(destination_id=id_destination, company_id=id_company, type=id_type) \
        .values('model__name', 'model').distinct().order_by('model')
    #     products - Выборка продукта по запросу
    #     infotovarsmodel - выборка уникальных значений для левого меню
    #     id_type - требуется при построеннии ссылки на тип товара в левом меню
    #     id_destination - требуется при построеннии ссылки на тип товара в левом меню
    #     id_company - требуется при построеннии ссылки на тип товара в левом меню
    product = get_object_or_404(Product, destination_id=id_destination, company_id=id_company, type=id_type,
                                model=id_model)

    infoproducts = Product.objects.filter(company_id=id_company, published_date__lte=timezone.now()) \
                       .order_by('published_date')[:3]

    #################################################################
    # Находи все фотографии по продукту

    fotoProduct = FotoTovar.objects.filter(product=product)

    return render(request, 'view_product.html',
                  {'product': product, 'id_type': id_type, 'id_destination': id_destination,
                   'id_company': id_company, 'infotovarsmodel': infotovarsmodel,
                   'destination': destination, 'company': company, 'type': type, 'model': model,
                   'infoproducts': infoproducts, 'bar': "katalog_bar", 'fotoProduct': fotoProduct
                   })


###################################################################
# Создаем заказ на продукцию
@login_required(login_url='/auth/login/')
def orders_product(request, id_destination=None, id_company=None, id_type=None, id_model=None, *args, **kwargs):
    if args is None:
        args = {}

    # Проверяем на наличие destination в базе
    destination = get_object_or_404(Attribute, pk=id_destination)
    # Проверяем на наличие company в базе
    company = get_object_or_404(Attribute, pk=id_company)
    # Проверяем на наличие type в базе
    type = get_object_or_404(Attribute, pk=id_type)
    # Проверяем на наличие model в базе
    model = get_object_or_404(Attribute, pk=id_model)

    # Проверяем количество не оплаченных предзаказов у пользователя
    count = OrderProduct.objects.filter(user=request.user, payment=False).count()
    if count >= 9:
        url = "/tovar/destination/" + str(destination.pk) + "/company/" + str(company.pk) + "/type/" + str(
            type.pk) + "/model/" + str(model.pk) + "/"

        return render(request, 'errors.html', {'bar': "katalog_bar",
                                               'errors': "Максимальное количество предзаказов достигнуто.",
                                               'url_': url})

    # Делаем выборку в запросе по нужным товарам
    product = Product.objects.get(destination_id=id_destination, company_id=id_company, type=id_type, model=id_model)

    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    activation_key = hashlib.sha1(salt + request.user.email).hexdigest()
    key_expires = datetime.datetime.today() + datetime.timedelta(2)

    user = User.objects.get(username=request.user)

    # Create and save user profile
    new_profile = OrderProduct(
        user=user,
        product=product,
        activation_key=activation_key,
        key_expires=key_expires,
        status="Ждет оплаты."
    )
    new_profile.save()

    return redirect('/office/', args, kwargs)


#################################################################
# Создаем ссылку для поиска товара по запросу
def searchProducrt(request, *args, **kwargs):
    if not args:
        args = {}

    args.update(csrf(request))

    if request.method == 'GET':
        if request.GET['q']:
            # Выполняем поиск по товару
            search = request.GET['q']
            products = Product.objects.filter(Q(name__icontains=search))
            if products.count() == 0:
                return render(request, 'errors.html', {'bar': "katalog_bar",
                                                       'errors': "По запросу ни чего не найдено.",
                                                       'url_': "/tovar/"})

            return render(request, 'product.html',
                          {'products': products, 'bar': "katalog_bar"})

    else:
        return
