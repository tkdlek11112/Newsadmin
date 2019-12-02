from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import LearnNews, RealNews
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
# Create your views here.


def list_learn_news(request):
    search_type = request.GET.get('search_type')
    search_keyword = request.GET.get('search_keyword')
    if search_keyword is None:
        search_keyword = ""

    if len(search_keyword) > 0:
        if search_type == '1':
            news_list = LearnNews.objects.order_by('pk').filter(title__contains=search_keyword)
        elif search_type == '2':
            news_list = LearnNews.objects.order_by('pk').filter(target__contains=search_keyword)

    else:
        search_type = '1'
        search_keyword = ''
        news_list = LearnNews.objects.all().order_by('pk')

    paginator = Paginator(news_list, 20)  # "5" 한페이지에서 보여줄 갯수를 정한다.
    page = request.GET.get('page')
    newses = paginator.get_page(page)
    return render(request, 'adminpage/list_learn_news.html', {'newses': newses, 'type': search_type, 'keyword': search_keyword})

@csrf_exempt
def toggle_learn_news(request):
    target = request.POST.get('target', '0')
    pk = request.POST.get('pk', '')
    if target == '1':
        next_target = 0
    else:
        next_target = 1

    update_model = LearnNews.objects.get(pk=pk)
    update_model.target = next_target
    update_model.save()

    return HttpResponse(status=200)


def list_real_news(request):
    search_type = request.GET.get('search_type')
    search_keyword = request.GET.get('search_keyword')
    if search_keyword is None:
        search_keyword = ""

    if len(search_keyword) > 0:
        if search_type == '1':
            news_list = RealNews.objects.order_by('pk').filter(title__contains=search_keyword)
        elif search_type == '2':
            news_list = RealNews.objects.order_by('pk').filter(target__contains=search_keyword)

    else:
        search_type = '1'
        search_keyword = ''
        news_list = RealNews.objects.all().order_by('pk')

    paginator = Paginator(news_list, 20)  # "5" 한페이지에서 보여줄 갯수를 정한다.
    page = request.GET.get('page')
    newses = paginator.get_page(page)
    return render(request, 'adminpage/list_real_news.html', {'newses': newses, 'type': search_type, 'keyword': search_keyword})


@csrf_exempt
def toggle_real_news(request):
    target = request.POST.get('target', '0')
    pk = request.POST.get('pk', '')
    if target == '1':
        next_target = 0
    else :
        next_target = 1

    update_model = RealNews.objects.get(pk=pk)
    update_model.target = next_target
    update_model.save()

    return HttpResponse(status=200)

@csrf_exempt
def push_real2learn(request):
    real_models = RealNews.objects.all().order_by('pk')

    for real_model in real_models:
        create_model = LearnNews.objects.create_news(real_model.date, real_model.time, real_model.title, real_model.tokens, real_model. target)
        create_model.save()

    real_models.delete()

    return HttpResponse(status=200)
