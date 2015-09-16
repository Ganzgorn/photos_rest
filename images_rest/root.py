import json
import os
import zipfile

from xml.etree import ElementTree

from django import http
from django.http import HttpResponse
from django.http.response import HttpResponseBase

from images_rest.models import User
from images_rest.settings import ARCHIVE_ROOT, ARCHIVE_URL


def response_result(method='GET'):
    def decorator(func):
        def wrapped(request, username, *args, **kwargs):
            if request.method != method:
                return http.HttpResponseNotAllowed(method)
            user = User.objects.get(username=username)
            result = func(request, user, *args, **kwargs)
            if not isinstance(result, HttpResponseBase):
                # Переводим в Json или xml
                if request.path.split('.')[-1] == 'xml':
                    result = HttpResponse(to_xml(result), content_type="application/xml")
                else:
                    result = HttpResponse(json.JSONEncoder().encode(result), content_type="application/json")

            return result

        return wrapped
    return decorator


def crate_archive(files, user):
    """
    Создает zip архив, возвращает строку
    """
    arch_name = user.username + '.zip'
    archive_path = os.path.join(ARCHIVE_ROOT, arch_name)
    archive = zipfile.ZipFile(archive_path, mode='w')
    for file in files:
        archive.write(file.path, file.name.replace(' ', '_')+'.'+file.type)

    archive.close()
    archive_url = ''.join([ARCHIVE_URL, arch_name])
    return archive_url


def to_xml(data):
    """
    Преобразует dict в xml
    """
    if not isinstance(data, list):
        data = [data]

    xml_data = ElementTree.Element('data')
    for obj in data:
        xml_photo = ElementTree.SubElement(xml_data, 'photo')
        for key, val in obj.items():
            xml_key = ElementTree.SubElement(xml_photo, key)
            xml_key.text = val

    result = bytes('<?xml version="1.1" encoding="UTF-8" ?>', 'utf-8') + ElementTree.tostring(xml_data)
    return result