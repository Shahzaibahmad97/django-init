from django.http import JsonResponse


def error404(request, exception):
    response = {
        "messages": {"non_field": [f"Path {request.path} does not exist ¯\_( ❛︣ . ❛︣ )_/¯  "]} # noqa
    }
    return JsonResponse(response, status=404)
