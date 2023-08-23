from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from api.core.mixin import GenericDotsViewSet, CreateDotsModelMixin
from api.support.models import ContactUs, Feedback
from api.support.serializers import ContactUsSerializer, FeedbackSerializer


class ContactUsViewSets(GenericDotsViewSet, CreateDotsModelMixin):
    serializer_class = ContactUsSerializer
    queryset = ContactUs.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.validated_data['created_by'] = self.request.user
        return super().perform_create(serializer)


class FeedbackViewSets(GenericDotsViewSet, CreateDotsModelMixin):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.validated_data['created_by'] = self.request.user
        return super().perform_create(serializer)
