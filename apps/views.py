from django.shortcuts import render
from .models import Item
import datetime
import pytz

from django.http import HttpResponse
from django.core import serializers

from el_pagination.decorators import page_template


def about(request):
    return render(request, 'apps/about.html')

@page_template('apps/index_xxx_game_page.html')
def index_xxx_game(request, template='apps/index_xxx_game.html', extra_context=None):
    if request.method == 'GET':
#        todate = str(datetime.datetime.today())
        TODATE = datetime.datetime.now()
        LAST_DATE = datetime.datetime.now()+datetime.timedelta(weeks=48)
#        last_week_date = str(datetime.datetime.today()-datetime.timedelta(days=2))

        #item_list = Item.objects.filter(updated_at__range=(LAST_DATE, TODATE), amino_price__range=('0', '1000000'), item_type=Item.ItemType.XXX_GAME, active=True).order_by('-updated_at', 'amino_price')
        print(TODATE)
        print(LAST_DATE)
        item_list = Item.objects.filter(period_at__range=(TODATE, LAST_DATE), amino_price__range=('0', '1000000'), item_type=Item.ItemType.XXX_GAME, active=True).order_by('period_at', 'amino_price')

        context = {
              'item': item_list,
                  }

        if extra_context is not None:
            context.update(extra_context)

        return render(request, template, context)

@page_template('apps/index_xxx_book_page.html')
def index_xxx_book(request, template='apps/index_xxx_book.html', extra_context=None):
    if request.method == 'GET':
        TODATE = pytz.timezone('Asia/Tokyo').localize(datetime.datetime.now())
        LAST_DATE = pytz.timezone('Asia/Tokyo').localize(datetime.datetime.now()+datetime.timedelta(weeks=48))

        print(TODATE)
        print(LAST_DATE)
        item_list = Item.objects.filter(period_at__range=(TODATE, LAST_DATE), amino_price__range=('0', '1000000'), item_type=Item.ItemType.XXX_BOOK, active=True).order_by('period_at', 'amino_price')

        context = {
              'item': item_list,
                  }

        if extra_context is not None:
            context.update(extra_context)

        return render(request, template, context)

@page_template('apps/index_alcohol_gel_page.html')
def index_alcohol_gel(request, template='apps/index_alcohol_gel.html', extra_context=None):
    if request.method == 'GET':
        todate = str(datetime.datetime.today())
        last_week_date = str(datetime.datetime.today()-datetime.timedelta(days=2))

        item_list = Item.objects.filter(updated_at__range=(last_week_date, todate), amino_price__range=('0', '1000000'), item_type=Item.ItemType.ALCOHOL_GEL, active=True).order_by('amino_price', '-updated_at')

        context = {
              'item': item_list,
                  }

        if extra_context is not None:
            context.update(extra_context)

        return render(request, template, context)

@page_template('apps/index_thermometer_page.html')
def index_thermometer(request, template='apps/index_thermometer.html', extra_context=None):
    if request.method == 'GET':
        todate = str(datetime.datetime.today())
        last_week_date = str(datetime.datetime.today()-datetime.timedelta(days=2))

        item_list = Item.objects.filter(updated_at__range=(last_week_date, todate), amino_price__range=('0', '1000000'), item_type=Item.ItemType.THERMOMETER, active=True).order_by('amino_price', '-updated_at')

        context = {
              'item': item_list,
                  }

        if extra_context is not None:
            context.update(extra_context)

        return render(request, template, context)

def api(request):
    if request.method == 'GET':
        todate=str(datetime.datetime.today())
        last_week_date=str(datetime.datetime.today()-datetime.timedelta(days=2))

        item_list=Item.objects.filter(updated_at__range=(last_week_date, todate), active=True).order_by('amino_price', '-updated_at')

        amino_price_lower = request.GET.get('amino_price_lower', '0')
        amino_price_upper = request.GET.get('amino_price_upper', '1000000')
        price_lower      = request.GET.get('price_lower', '0')
        price_upper      = request.GET.get('price_upper', '1000000')
        num              = request.GET.get('num', '1000')

        print(request.GET.getlist('distributor'))
        distributor_list=[]
        for d in request.GET.getlist('distributor', ['amazon', 'rakuten', 'yahoo']):
            distributor_list.append(d)

        condition={
                      'amino_price_lower': amino_price_lower,
                      'amino_price_upper': amino_price_upper,
                      'price_lower': price_lower,
                      'price_upper': price_upper,
                      'distributor_list': distributor_list,
                      'num': num
                  }

        #print(list_create(condition))
        item_list=list_create(condition)

        return HttpResponse(serializers.serialize('json', item_list), content_type="application/json")

# ランキングリスト生成
def list_create(condition):

    print(condition)
    item_list = Item.objects.filter(amino_price__range=(condition['amino_price_lower'], condition['amino_price_upper']), price__range=(condition['price_lower'], condition['price_upper']), distributor__in=condition['distributor_list'], active=True).order_by('amino_price')[:int(condition['num'])]
#    for ml in item_list:
#        print(str(ml))

    """
    # hot 全ての診断を対象に最近の数時間での診断回数を集計しTOP200まで表示しています。1時間に1回、毎時0分～10分くらいの間に更新されます。
    # 診断履歴を何処かに取っておかないと見れないねコレ
    if mode == 'hot':
        item_list = Item.objects.filter(created_at__range=(datetime.date.today()-datetime.timedelta(days=31), datetime.date.today()), active=True).order_by('count')[:int(num)]
    # new 最近登録された診断だけを対象に集計しています。
    elif mode == 'new':
        item_list = Item.objects.filter(active=True).order_by('-created_at')[:int(num)]
    # count 診断回数だけを対象に集計しています。
    elif mode == 'count':
        item_list = Item.objects.filter(active=True).order_by('-count')[:int(num)]
    # pickup 最近登録された診断だけを対象に診断回数が多いものを集計しています。
    elif mode == 'pickup':
        item_list = Item.objects.filter(active=True).order_by('-created_at', '-count')[:int(num)]
    # daily 過去一日で診断された中で診断回数が多いものを集計しています。
    elif mode == 'daily':
        last_day=str(datetime.date.today()-datetime.timedelta(days=1))
        todate=str(datetime.datetime.today())
        item_list = Item.objects.filter(updated_at__range=(last_day, todate), active=True).order_by('-count')[:int(num)]
    # weekly 過去一週間で診断された中で診断回数が多いものを集計しています。
    elif mode == 'weekly':
        last_week=str(datetime.date.today()-datetime.timedelta(days=7))
        todate=str(datetime.datetime.today())
        item_list = Item.objects.filter(updated_at__range=(last_week, todate), active=True).order_by('-count')[:int(num)]
    # monthly 過去一ヶ月間で診断された中で診断回数が多いものを集計しています。
    elif mode == 'monthly':
        last_month=str(datetime.date.today()-datetime.timedelta(days=7))
        todate=str(datetime.datetime.today())
        item_list = Item.objects.filter(updated_at__range=(last_month, todate), active=True).order_by('-count')[:int(num)]
    #my自分が作成したリスト
    elif mode == 'my':
        item_list = Item.objects.filter(created_user=user).filter(active=True).order_by('-created_at')[:int(num)]
    # search 検索
    elif mode == 'search':
        item_list = Item.objects.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(result_text__icontains=q)).filter(active=True).order_by('-count', '-created_at')[:int(num)]
    #オプション無しで新着
    else:
        item_list = Item.objects.filter(active=True).order_by('-created_at')[:int(num)]
    """

    return item_list

