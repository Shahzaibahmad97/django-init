from rest_framework import status
from rest_framework.response import Response


def dots_create(func):
    def function_wrapper(self, request, *args, **kwargs):
        data = func(self, request, *args, **kwargs)
        serializer = self.get_serializer_create(data=data)
        serializer.is_valid(raise_exception=True)
        model_obj = self.perform_create(serializer)
        func(self, request, *args, **kwargs)
        serializer_display = self.get_serializer(model_obj)
        headers = self.get_success_headers(serializer.data)
        return Response({"data": serializer_display.data}, status=status.HTTP_201_CREATED, headers=headers)
    return function_wrapper
