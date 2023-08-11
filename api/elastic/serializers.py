from rest_framework import serializers


class ElasticSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        document = None
        return_serializer = None
        search_nested_field = None
        search_field = None

    def get_items(self, obj):
        queryset = self.get_default_queryset(obj)
        return self.Meta.return_serializer(queryset.to_queryset(), many=True).data

    def get_default_queryset(self, obj):
        if self.context['request'].query_params.get('search', None) and \
                not self.context['request'].query_params['search'].lower() in obj.title.lower():
            queryset = self.Meta.document.search().query(
                "match_phrase_prefix", **{self.Meta.search_field: obj.title}
            ).query(
                "match_phrase_prefix", **{
                    self.Meta.search_nested_field: self.context['request'].query_params.get('search', None)
                }
            )
        else:
            queryset = self.Meta.document.search().query(
                "match_phrase_prefix", **{self.Meta.search_field: obj.title}
            )

        return queryset[0:5000]
