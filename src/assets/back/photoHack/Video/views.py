from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotFound
from .forms import UploadFileForm
from .models import Video
from .effects.compose_effects import run
import os

from django.conf import settings
import globals
import json


@csrf_exempt
def upload_video(request):
    file_name = 'None'
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_name = request.FILES['file'].name
            instance = Video(video_file=request.FILES['file'])
            instance.save()
    else:
        return HttpResponseNotFound()

    response = JsonResponse({'url': globals.HOST+'/media/videos/'+file_name})
    response = globals.ser_cors_headers(response)
    return response


@csrf_exempt
def apply_actions(request):
    file_name = 'None'

    if request.method == 'POST':
        data = json.loads(request.body)

        if data.get('url') and data.get('actions'):
            url = data['url']
            actions = data['actions']

            videos_root = settings.MEDIA_ROOT + 'videos\\'
            file_name = str(len(os.listdir(videos_root)) + 1) + '.mp4'

            video_dir = videos_root + url.split('/')[-1]
            target_dir = videos_root + file_name

            run(video_dir, target_dir, actions)
    elif request.method == 'OPTIONS':
        pass
    else:
        return HttpResponseNotFound()

    response = JsonResponse({'url': globals.HOST+'/media/videos/'+file_name})
    response = globals.ser_cors_headers(response)
    return response
