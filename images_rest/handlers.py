import datetime
import os

from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from django.core.servers.basehttp import FileWrapper

from piston3.handler import BaseHandler
from piston3.utils import rc

from images_rest.models import User, Photo
from images_rest.root import response_result, crate_archive
from images_rest.settings import MEDIA_ROOT, MEDIA_URL, ARCHIVE_ROOT


def create_path(root, directory, file_name, file_type):
    return os.path.join(root, directory, file_name.replace(' ', '_')+'.'+file_type)


@response_result(method='POST')
def photo_upload(request, user):
    """
    Загрузить фото
    """
    if not request.body:
        return HttpResponseBadRequest()

    name_photo = request.GET.get('name')
    border_color = request.GET.get('border-color')
    alpha = request.GET.get('alpha')
    type_photo = request.GET.get('type', 'jpg')

    if not name_photo or not border_color:
        return HttpResponseBadRequest()

    path = os.path.join(MEDIA_ROOT, user.username)
    if not os.path.exists(path):
        os.mkdir(path)

    media_path = create_path(MEDIA_ROOT, user.username, name_photo, type_photo)
    media_url = '/'.join([MEDIA_URL+user.username, name_photo+'.'+type_photo])

    photo_f = open(media_path, 'wb')
    photo_f.write(request.body)
    photo_f.close()

    photo = Photo.objects.get_or_create(path=media_path, name=name_photo, url=media_url, user=user)[0]
    photo.border_color = border_color

    if alpha:
        photo.alpha = alpha

    if type_photo:
        photo.type = type_photo

    photo.save()

    return photo.get_dict()


@response_result()
def photo_info(request, user):
    """
    Получить ифнормацию о фото
    """
    name_photo = request.GET.get('name')
    type_photo = request.GET.get('type', 'jpg')

    if not name_photo:
        return HttpResponseBadRequest()

    media_path = create_path(MEDIA_ROOT, user.username, name_photo, type_photo)
    try:
        photo = Photo.objects.get(path=media_path, name=name_photo, user=user)
    except Photo.DoesNotExist:
        return HttpResponseNotFound()

    return photo.get_dict()


@response_result(method='POST')
def photo_edit(request, user):
    """
    Изменить информацию о фото
    """
    name_photo = request.GET.get('name')
    border_color = request.GET.get('border-color')
    alpha = request.GET.get('alpha')
    type_photo = request.GET.get('type', 'jpg')

    if not name_photo:
        return HttpResponseBadRequest()

    media_path = create_path(MEDIA_ROOT, user.username, name_photo, type_photo)

    try:
        photo = Photo.objects.get(path=media_path, name=name_photo, user=user)
    except Photo.DoesNotExist:
        return HttpResponseNotFound()

    if border_color:
        photo.border_color = border_color

    if alpha:
        photo.alpha = alpha

    if type_photo:
        photo.type = type_photo

    photo.save()

    return photo.get_dict()


@response_result(method='POST')
def photo_delete(request, user):
    """
    Удалить фото
    """
    name_photo = request.GET.get('name')
    type_photo = request.GET.get('type', 'jpg')

    if not name_photo:
        return HttpResponseBadRequest()

    media_path = create_path(MEDIA_ROOT, user.username, name_photo, type_photo)

    try:
        photo = Photo.objects.get(path=media_path, name=name_photo, user=user)
    except Photo.DoesNotExist:
        return HttpResponseNotFound()

    photo.delete()

    return rc.ALL_OK


@response_result()
def photo_list(request, user):
    """
    Список фото
    date - все фотографии пользователя за дату
    sort - сортировка по конкретному полю (name, date - либо другому полю из модели)
    page - текущая страница
    count - количество элементов на странице
    """
    date_str = request.GET.get('date')
    sort = request.GET.get('sort', 'name')
    page = int(request.GET.get('page', '1'))
    count = int(request.GET.get('count', '10'))

    filter_dict = {
        'user': user
    }
    if date_str:
        date = datetime.datetime.strptime(date_str[:10], '%Y-%m-%d')
        filter_dict['date__gte'] = date
        filter_dict['date__lte'] = date + datetime.timedelta(1)

    photos = Photo.objects.filter(**filter_dict).order_by(sort)
    result = [photo.get_dict() for photo in photos[(page-1)*count:page*count]]
    return result


@response_result()
def photo_search(request, user):
    """
    Поиск по фотографиям
    name - поиск по имени
    color - по цвету
    """
    search_name = request.GET.get('name')
    search_color = request.GET.get('color')
    search_dict = {'user': user}

    if search_name:
        search_dict['name__icontains'] = search_name

    if search_color:
        search_dict['border_color'] = search_color

    photos = Photo.objects.filter(**search_dict)
    result = [photo.get_dict() for photo in photos]
    return result


@response_result()
def photo_archive(request, user):
    """
    Получить архив за период от date_from по date_to
    Возвращает ссылку на скачивание архива
    """
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    date_from = datetime.datetime.strptime(date_from[:10], '%Y-%m-%d')
    # Если нам нужно включительно по "дату" - прибавляем день
    date_to = datetime.datetime.strptime(date_to[:10], '%Y-%m-%d') + datetime.timedelta(1)

    photos = Photo.objects.filter(user=user, date__gte=date_from, date__lte=date_to)

    archive_url = crate_archive(photos, user)

    host = request.META['HTTP_HOST']
    result = {
        'archive_url': host + archive_url
    }
    return result


class UserHandler(BaseHandler):
    """
    Классический REST api для модели User
    """
    model = User

    def read(self, request, username=None, *args, **kwargs):

        if username:
            result = self.queryset(request).get(username=username)
        else:
            result = self.queryset(request).all()

        return result

    def update(self, request, username=None, *args, **kwargs):
        if not username:
            return rc.BAD_REQUEST

        attrs = self.flatten_dict(request.GET)
        self.queryset(request).filter(username=username).update(**attrs)

        return rc.ALL_OK

    def delete(self, request, username=None, *args, **kwargs):
        if not username:
            return rc.BAD_REQUEST

        self.queryset(request).get(username=username).delete()
        return rc.ALL_OK


def download_archive(request, archive_name):
    """
    Скачать архив
    """
    archive_path = os.path.join(ARCHIVE_ROOT, archive_name + '.zip')
    archive = open(archive_path, 'rb')
    response = HttpResponse(FileWrapper(archive), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=' + archive_name + '.zip'
    return response