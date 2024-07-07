from django.conf import settings
from django.utils import translation
from django.shortcuts import redirect

class DefaultLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path_info = request.path_info.split('/')
        language = path_info[1] if len(path_info) > 1 else ''
        if language not in dict(settings.LANGUAGES).keys():
            language = settings.LANGUAGE_CODE
            new_path = '/' + language + request.path_info
            return redirect(new_path)

        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()
        response = self.get_response(request)
        translation.deactivate()
        return response


