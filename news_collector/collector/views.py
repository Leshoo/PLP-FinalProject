from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.http import JsonResponse
import requests
from .constants import BLOGS


def index(request):
    return render(request, "index.html", {
    })


def news_collector_sync_view(request):

    data = {}
    for name, link in BLOGS.items():
        print('Downloading "%s" from "%s" ...' % (name, link))
        response = requests.get(link)
        if response.status_code != 200:
            data[name] = 'Download error'
        else:
            data[name] = response.content.decode("utf-8")
    print('Download completed')

    return JsonResponse(data)
