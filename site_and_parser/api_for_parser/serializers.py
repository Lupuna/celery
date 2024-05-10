from rest_framework import serializers
from . import models, tasks, services


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = ('name', 'price', 'description', 'image_url', 'discount')


class UpdateProductListSerializer(serializers.Serializer):
    products_count = serializers.IntegerField(default=10)

    def create(self, validated_data):
        items = tasks.simulate_user_app.delay(services.parsing_url, validated_data['products_count'])
        instances = [models.Product(**item) for item in items]
        return models.Product.objects.bulk_create(instances)
