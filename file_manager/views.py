from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404,JsonResponse
import binascii
import os
from rest_framework import views
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
# Create your views here.
from file_manager.storage_service import StorageService
import pathlib
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.decorators import permission_classes, authentication_classes
from creators.authentication import TokenAuthentication

@api_view(['POST'])
@parser_classes([MultiPartParser])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def content_upload_view(request, filename, format=None):
    file_obj = request.FILES['file']
    extension = pathlib.Path(file_obj.name).suffix
    result = StorageService.upload(file_obj, resource_type='raw',public_id='%s%s' % (binascii.hexlify(os.urandom(20)).decode(), extension))
    # result = {
    # 'secure_url' :'https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Placeholder_book.svg/792px-Placeholder_book.svg.png'
    # }
    data = {
        'url': result['secure_url']
    }
    
    return Response(data, status=201)

@api_view(['POST'])
@parser_classes([MultiPartParser])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def image_upload_view(request, filename, format=None):
    file_obj = request.FILES['file']
    result = StorageService.upload(file_obj, resource_type='image')
    # result = {
    # 'secure_url' :'https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Placeholder_book.svg/792px-Placeholder_book.svg.png'
    # }
    data = {
        'url': result['secure_url']
    }
    return Response(data, status=201)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def file_delete_view(request, id, format=None):
    public_id = id
    if public_id:
        StorageService.destroy(public_id=public_id)
        return Response(status=204)
