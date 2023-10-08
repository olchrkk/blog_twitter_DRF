from django.views import View
from django.shortcuts import render
from .models import Upload
from django.http import HttpResponseRedirect


class UploadView(View):

    def post(self, request):
        image = request.FILES['userPhoto']
        Upload.upload_image(image, image.name)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
