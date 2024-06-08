import time
from django.utils.deprecation import MiddlewareMixin


class LogLongRequestsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        total_time = time.time() - request.start_time
        if total_time > 5:  # Логировать запросы, которые занимают больше 1 секунды
            print(f"Long request: {request.path} took {total_time:.2f} seconds")
        return response

