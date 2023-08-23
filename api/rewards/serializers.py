from rest_framework import serializers


class ReturnRewardsSerializer(serializers.Serializer):
    total_points = serializers.IntegerField(default=750)
    free_products = serializers.IntegerField(default=3)
