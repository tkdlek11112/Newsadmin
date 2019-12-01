from django.shortcuts import render
from .models import LearnNews
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
        news_list = LearnNews.objects.all()

    paginator = Paginator(news_list, 20)  # "5" 한페이지에서 보여줄 갯수를 정한다.
    page = request.GET.get('page')
    newses = paginator.get_page(page)
    return render(request, 'adminpage/list_learn_news.html', {'newses': newses, 'type': search_type, 'keyword': search_keyword})
