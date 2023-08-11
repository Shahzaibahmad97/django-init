import traceback

from django.conf import settings
from django.http import JsonResponse
from rest_framework import status

from api.core.constants import DeviceType


class DeviceTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path != '/' and not request.path.__contains__('admin'):
            device_type = request.headers.get('Device-Type', None)

            if device_type is None or device_type not in dict(DeviceType.choices).keys():
                return JsonResponse({
                    "detail": "Header Device-Type is required"
                }, status=status.HTTP_403_FORBIDDEN)

            request.device_type = device_type

        response = self.get_response(request)

        return response


class ApiMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    @staticmethod
    def process_exception(request, response):
        print(f"\033[93m{traceback.format_exc()}\033[0m")

        return JsonResponse({
            "messages": {"non_field": ["Something bad happened ¯\_( ❛︣ . ❛︣ )_/¯"
                                       ", please contact support"]}
        }, status=500)


class PrintSQlMiddleware:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if settings.DEBUG and settings.DEBUG_LEVEL.lower() == 'debug':
            from django.db import connection
            count = 0
            total_time = float()
            for queries in connection.queries:
                count += 1
                print(f"{self.GREEN} sql: {self.END} {self.WARNING}{queries['sql']} {self.END}")
                print(f"{self.GREEN} time: {self.END} {self.WARNING}{queries['time']} {self.END}")
                print(f"{self.FAIL}---------------------------------------------------{self.END}")

                total_time += float(queries['time'])

                if count == len(connection.queries):
                    print()

            print(f"{self.BOLD}Total queries: {count} {self.END}")
            print(f"{self.BOLD}Total time of execution: {total_time} {self.END}\n")

        return response
