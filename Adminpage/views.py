from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from .models import LearnNews, RealNews
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.functions import TruncMonth, TruncDate
import simplejson as json
from django.db.models import Q, DateTimeField, DateField, Count


# Create your views here.

@csrf_exempt
def list_learn_news(request):
    search_type = request.GET.get('search_type')
    search_keyword = request.GET.get('search_keyword')
    if search_keyword is None:
        search_keyword = ""

    if len(search_keyword) > 0:
        if search_type == '1':
            news_list = LearnNews.objects.order_by('-pk').filter(title__contains=search_keyword)
        elif search_type == '2':
            news_list = LearnNews.objects.order_by('-pk').filter(target__contains=search_keyword)

    else:
        search_type = '1'
        search_keyword = ''
        news_list = LearnNews.objects.all().order_by('-pk')

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

@csrf_exempt
def list_real_news(request):
    search_type = request.GET.get('search_type')
    search_keyword = request.GET.get('search_keyword')
    if search_keyword is None:
        search_keyword = ""

    if len(search_keyword) > 0:
        if search_type == '1':
            news_list = RealNews.objects.order_by('-pk').filter(title__contains=search_keyword)
        elif search_type == '2':
            news_list = RealNews.objects.order_by('-pk').filter(target__contains=search_keyword)

    else:
        search_type = '1'
        search_keyword = ''
        news_list = RealNews.objects.all().order_by('-pk')

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

@csrf_exempt
def statisticsnews(request):

    # 로그인 인증
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect('/')

    stat_type = request.GET.get('stat_type')
    stat_gbn = request.GET.get('optionRadios')
    to_date = request.GET.get('to_date')
    from_date = request.GET.get('from_date')
    total_count = 0
    cnt = 0
    total_count2 = 0
    cnt2 = 0
    if stat_type == 'M':
        if stat_gbn == 'period':
            stats = LearnNews.objects \
                .filter(date__range=[from_date, to_date]) \
                .annotate(stat_date=TruncMonth('ldate')) \
                .order_by('-stat_date') \
                .values('stat_date') \
                .annotate(stat_count=Count('title')
                          ).values('stat_date', 'stat_count')

            stats2 = LearnNews.objects \
                .filter(date__range=[from_date, to_date]) \
                .annotate(stat_date=TruncMonth('ldate')) \
                .filter(target=1) \
                .order_by('-stat_date') \
                .values('stat_date') \
                .annotate(stat_count=Count('title')
                          ).values('stat_date', 'stat_count')
        else:
            stats = LearnNews.objects \
                .annotate(stat_date=TruncMonth('date')) \
                .order_by('-stat_date') \
                .values('stat_date') \
                .annotate(stat_count=Count('title')
                          ).values('stat_date', 'stat_count')

            stats2 = LearnNews.objects \
                .annotate(stat_date=TruncMonth('date')) \
                .filter(target=1)\
                .order_by('-stat_date') \
                .values('stat_date') \
                .annotate(stat_count=Count('title')
                          ).values('stat_date', 'stat_count')
    else:
        if stat_gbn == 'period':
            stats = LearnNews.objects \
                .filter(date__range=[from_date, to_date])\
                .annotate(stat_date=TruncDate('date')) \
                .order_by('-stat_date') \
                .values('stat_date') \
                .annotate(stat_count=Count('title')
                          ).values('stat_date', 'stat_count')

            stats2 = LearnNews.objects \
                .filter(date__range=[from_date, to_date]) \
                .annotate(stat_date=TruncDate('date')) \
                .filter(target=1) \
                .order_by('-stat_date') \
                .values('stat_date') \
                .annotate(stat_count=Count('title')
                          ).values('stat_date', 'stat_count')
        else:
            stats = LearnNews.objects \
                .annotate(stat_date=TruncDate('date')) \
                .order_by('-stat_date')\
                .values('stat_date') \
                .annotate(stat_count=Count('title')
                          ).values('stat_date', 'stat_count')
            stats2 = LearnNews.objects \
                .annotate(stat_date=TruncDate('date')) \
                .filter(target=1) \
                .order_by('-stat_date') \
                .values('stat_date') \
                .annotate(stat_count=Count('title')
                          ).values('stat_date', 'stat_count')

    date_list = []
    date_count = []

    for stat in stats:
        date_list.append(str(stat['stat_date']))
        date_count.append(str(stat['stat_count']))
        total_count = total_count + int(stat['stat_count'])
        cnt = cnt + 1

    if cnt > 0:
        total_mean = round(total_count / cnt)
    else:
        total_mean = 0
    date_list.reverse()
    date_count.reverse()

    date_list2 = []
    date_count2 = []

    for stat in stats2:
        date_list2.append(str(stat['stat_date']))
        date_count2.append(str(stat['stat_count']))
        total_count2 = total_count2 + int(stat['stat_count'])
        cnt2 = cnt2 + 1

    if cnt2 > 0:
        total_mean2 = round(total_count2 / cnt2)
    else:
        total_mean2 = 0
    date_list2.reverse()
    date_count2.reverse()


    # 전체 뉴스 조회
    LearnNews_spams = LearnNews.objects.filter(target=1)
    LearnNews_normals = LearnNews.objects.filter(target=0)
    RealNews_spams = RealNews.objects.filter(target=1)
    RealNews_normals = RealNews.objects.filter(target=0)



    context = {'stats': stats,
               'stat_type': stat_type,
               'optionRadios': stat_gbn,
               'to_date': to_date,
               'from_date': from_date,
               'date_list': json.dumps(date_list),
               'date_count': json.dumps(date_count),
               'total_count': total_count,
               'total_mean': total_mean,
               'stats2': stats2,
               'date_list2': json.dumps(date_list2),
               'date_count2': json.dumps(date_count2),
               'total_count2': total_count2,
               'total_mean2': total_mean2,
               'ln_total_spams': len(LearnNews_spams),
               'ln_total_normals': len(LearnNews_normals),
               'rl_total_spams': len(RealNews_spams),
               'rl_total_normals': len(RealNews_normals),
               }
    return render(request, 'adminpage/statistics_news.html', context)
