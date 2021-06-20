from django.shortcuts import render
from django.http import HttpResponse
import json
# Create your views here.
from News.NewsService import *
from News.CreateModel import create_model
from Adminpage.models import LearnLog
from distutils.dir_util import copy_tree
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt


#뉴스를 받으면 실행됨
@csrf_exempt
def receive_news(request):
    data = json.loads(request.body)
    title = data['title']
    ns = NewsService()
    ns.classify_news(title)
    return HttpResponse(status=200)

@csrf_exempt
def learn_news(request):
    stats = LearnLog.objects.all().order_by('-pk')
    learning = stats[0].learn_status
    versions = LearnLog.objects.filter(apply_status='Y')
    for vers in versions:
        now_version = vers
    context = {'stats': stats, 'now_version': now_version, 'learning' : learning}
    return render(request, 'adminpage/learn_news.html', context)

@csrf_exempt
def apply_version(request):
    pk = request.POST['pk']
    src = 'News/trainfiles/' + str(pk)
    dst = 'News/trainfiles/current/'
    copy_tree(src, dst)
    print("apply")
    LearnLog.objects.update_apply(pk)
    stats = LearnLog.objects.all().order_by('-pk')
    versions = LearnLog.objects.filter(apply_status='Y')
    for ver in versions:
        now_version = ver
    context = {'stats': stats, 'now_version': now_version}
    return HttpResponse(status=200)
    # return render(request, 'adminpage/learn_news.html',context)


def learn(request):
    now_version = 0
    #학습 버전 생성
    version = LearnLog.objects.create_learnlog()
    #학습하기
    create_model(version)

    stats = LearnLog.objects.all().order_by('-pk')
    versions = LearnLog.objects.filter(apply_status='Y')
    learning = stats[0].learn_status
    for ver in versions:
        now_version = ver
    context = {'stats': stats, 'now_version': now_version, 'learning' : learning}
    return render(request, 'adminpage/learn_news.html', context)

@csrf_exempt
def web_news(request):
    if request.method == 'POST':
        input1 = request.POST['input1']
        print(input1)
        ns = NewsService()
        ns.classify_news(input1)
        return HttpResponse(status=200)
    else:
        return render(request, 'adminpage/chat_web.html')
