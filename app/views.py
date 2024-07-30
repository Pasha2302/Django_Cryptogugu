import json

from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpRequest, JsonResponse, HttpResponse

from .controllers_views.controllers_base import BaseContextManager
from .controllers_views.controllers_header_search import HeaderSearchManager
from .controllers_views.controllers_index import IndexContextManager, PromotedCoinsTableManager, VoteManager
from .controllers_views.controllers_settings_user import save_user, clear_data, SettingsManager
from .models import Coin


def clear_settings(request: HttpRequest):
    clear_data()
    return HttpResponse("All user settings have been cleared.")


def reset_all_votes(request: HttpRequest):
    Coin.objects.update(votes=0)
    Coin.objects.update(votes24h=0)
    Coin.objects.update(selected_auto_voting=False)
    return JsonResponse({'data': 'Голосование обнулено'}, status=200)


def get_user_id(request: HttpRequest):
    user_id = request.COOKIES.get('userId')
    data = save_user(user=user_id)
    return JsonResponse(data, status=200)


def set_theme_site(request: HttpRequest):
    if request.method == 'POST':
        SettingsManager(request)
        data = {'data': 'done | scheme installed'}
        return JsonResponse(data, status=200)


def show_more(request: HttpRequest):
    if request.method == 'POST':
        user_id_str = request.COOKIES.get('userId')
        current_page = json.loads(request.body)['data']['morePage']
        print(f"\n[show_more() method = 'POST']:\nData POST: {current_page}\nUser ID: {user_id_str}")

        context = IndexContextManager(request).get_context()
        html_data = render_to_string('app/components_html/coins_trending_component.html', context)
        data = {'coins_html': html_data}
        return JsonResponse(data=data, status=200)

    else:
        return JsonResponse(data={'status': 'Incorrect request'}, status=402)


def set_settings_user(request: HttpRequest):
    print("\nLog >> def set_options_trending_coins(request: HttpRequest):")

    if request.method == 'POST':
        context = IndexContextManager(request).get_context()
        print("[method = 'POST'] Current URL: ", context['current_uri'])
        html_data = render_to_string('app/components_html/coins_trending_component.html', context)
        pagination_html = render_to_string('app/components_html/pagination_component.html', context)
        data = {'html': html_data, 'pagination': pagination_html}
        return JsonResponse(data, status=200)


def index(request: HttpRequest):
    index_manager = IndexContextManager(request)
    context = index_manager.get_context() | BaseContextManager().get_context()
    return render(request, 'app/index.html', context=context, status=200)


def get_header_search_component(request: HttpRequest):
    if request.method == 'POST':
        context = HeaderSearchManager(request).get_context()
        html_data = render_to_string('app/components_html/header_search_component.html', context)
        data = {'coins_html': html_data}
        return JsonResponse(data=data, status=200)

    else:
        return JsonResponse(data={'status': 'Incorrect request'}, status=402)


def get_table_promoted_coins_component(request: HttpRequest):
    if request.method == 'POST':
        context = PromotedCoinsTableManager(request).get_context()
        html_data = render_to_string('app/components_html/table_coins_component.html', context)
        data = {'coins_html': html_data}
        return JsonResponse(data=data, status=200)

    else:
        return JsonResponse(data={'status': 'Incorrect request'}, status=402)


def voting(request: HttpRequest):
    if request.method == 'POST':
        vote_manager = VoteManager(request=request)
        vote_manager.check_and_save_vote()
        data_vote = vote_manager.get_data_vote()
        return JsonResponse(data=data_vote, status=200)

    else:
        return JsonResponse(data={'status': 'Incorrect request'}, status=402)


def airdrops(request: HttpRequest):
    return render(request, 'app/airdrops.html', status=200)


def promote(request: HttpRequest):
    return render(request, 'app/promote.html', status=200)


def handler404(request: HttpRequest, exception):
    print("\nHandler 404")
    return render(request, 'app/example/404.html', status=404)
