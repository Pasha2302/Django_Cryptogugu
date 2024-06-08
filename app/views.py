# import json
import json
import uuid

from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpRequest, JsonResponse

from .controllers_views.controllers_index import IndexContextManager
from .models import UserSettings


def get_user_id(request: HttpRequest):
    user_id = uuid.uuid4()
    data = { 'user_id': str(user_id) }
    data_id, created = UserSettings.objects.get_or_create(user_id=user_id)
    print(f"\n{data_id=}\n{created=}")
    return JsonResponse(data, status=200)


def show_more(request: HttpRequest):
    if request.method == 'POST':
        user_id_str = request.COOKIES.get('userId')
        current_page = json.loads(request.body)['data']['morePage']
        print(f"\n[show_more() method = 'POST']:\nData POST: {current_page}\nUser ID: {user_id_str}")

        context = IndexContextManager(request, current_page).get_context()
        html_data = render_to_string('app/add_html/showMore_trending_coins.html', context)
        data = {'coins_html': html_data}
        return JsonResponse(data=data, status=200)

    else:
        return JsonResponse(data={'status': 'Incorrect request'}, status=402)



def set_settings_user(request: HttpRequest):
    print("\nLog >> def set_options_trending_coins(request: HttpRequest):")
    if request.method == 'POST':
        user_id_str = request.COOKIES.get('userId')
        data = json.loads(request.body)

        # print("[method = 'POST'] COOKIES: ", request.COOKIES)
        # print("[method = 'POST'] User ID: ", user_id_str)
        print("\n[method = 'POST'] Data POST:", data)
        # print(f"Тип user_id: {type(user_id_str)}")

        per_page = data['data']['per_page']
        current_page = data['data'].get('currentPage')
        if user_id_str != 'null':
            try:
                user_id = uuid.UUID(user_id_str)
                user_settings = UserSettings.objects.get(user_id=user_id)
                user_settings.per_page = per_page
                user_settings.save()
            except UserSettings.DoesNotExist as err:
                print(err)
                print("[method = 'POST'] Пользователь не найден в базе!")

        context = IndexContextManager(request, current_page).get_context()
        print("[method = 'POST'] Current URL: ",context['current_uri'])
        html_data = render_to_string('app/add_html/showMore_trending_coins.html', context)
        data = {'html': html_data}
        return JsonResponse(data, status=200)


def index(request: HttpRequest):
    context = IndexContextManager(request).get_context()
    return render(request, 'app/index.html', context=context, status=200)



def airdrops(request: HttpRequest):
    return render(request, 'app/airdrops.html', status=200)


def promote(request: HttpRequest):
    return render(request, 'app/promote.html', status=200)


def handler404(request: HttpRequest, exception):
    print("\nHandler 404")
    return render(request, 'app/example/404.html', status=404)
