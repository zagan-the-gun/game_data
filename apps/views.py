from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, LargeCategory, MediumCategory, SmallCategory, Site
import datetime
import pytz
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from el_pagination.decorators import page_template
#from django.http import Http404



def item_redirect(request, item_id=None):
    item = get_object_or_404(Item, pk = item_id, active = True)
    tag_list=[]
    for tag in item.tags.all():
        tag_list.append(tag)
    small_category = SmallCategory.objects.filter(tags__name__in=tag_list, is_view = True)[:1][0]
    site = Site.objects.get(pk=1)
    d = {
      'site'          : site,
      'item'          : item,
      'small_category': small_category,
    }
    return render(request, 'apps/redirect.html', d)


def index(request):
    return redirect('/stock-news/')


def about(request):
    site = Site.objects.get(pk=1)
    d = {
      'site': site,
    }
    return render(request, 'apps/default_about.html', d)


def index_large_default(request):

    if request.method == 'GET':

        site = Site.objects.get(pk=1)
        large_category_list = LargeCategory.objects.filter(is_view = True)
        d = {
          'site': site,
          'large_category_list': large_category_list,
        }
        return render(request, 'apps/index_large_default.html', d)


@page_template('apps/index_default_page.html')
def index_default(request, l_category, m_category=None, s_category=None, template='apps/index_default.html', extra_context=None):

    if request.method == 'GET':

        # カテゴリ取得
        if m_category is not None:
            medium_category = MediumCategory.objects.get(name = m_category)
        else:
            medium_category = MediumCategory.objects.filter(large_category__name = l_category, is_view = True)[:1][0]

        if s_category is not None:
            small_category = SmallCategory.objects.get(name = s_category)
        else:
            small_category = SmallCategory.objects.filter(medium_category = medium_category, is_view = True)[:1][0]

        # カテゴリリスト取得
#        print(l_category)
#        print(m_category)
#        print(s_category)
        large_category = LargeCategory.objects.get(name = l_category)
        medium_category_list = MediumCategory.objects.filter(large_category = large_category, is_view = True)
        small_category_list = SmallCategory.objects.filter(medium_category = medium_category, is_view = True)

        TODATE = datetime.datetime.now()
        LAST_DATE = datetime.datetime.now()-datetime.timedelta(days=5)

#        print(small_category.tags.all())
#        print(u", ".join(lc.name for lc in small_category.tags.all()))

#        print('DEBUG DEBUG DEBUG tags: ')
#        print(small_category)
        tag_list = u", ".join(lc.name for lc in small_category.tags.all())
#        print(tag_list)
        item_list = Item.objects.filter(updated_at__range=(LAST_DATE, TODATE), amino_price__range=('0', '1000000'), tags__name__in=[tag_list], active=True).order_by('amino_price', '-updated_at').distinct()
#        print('DEBUG DEBUG DEBUG item_list : ')
#        print(item_list)

        site = Site.objects.get(pk=1)
        context = {
                    'site'                : site,
                    'large_category'      : large_category,
                    'medium_category_list': medium_category_list,
                    'small_category_list' : small_category_list,
                    'medium_category'     : medium_category,
                    'small_category'      : small_category,
                    'item'                : item_list,
                  }

        if extra_context is not None:
            context.update(extra_context)

        #return render(request, 'apps/index_default.html')
        return render(request, template, context)


