from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from . import serializers, models


class ProductsView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    queryset = models.Product.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.UpdateProductListSerializer
        else:
            return serializers.ProductSerializer

    def create(self, request, *args, **kwargs):
        if int(request.data.get('products_count')) < 10:
            raise ValidationError('products_count too small')
        elif 50 < int(request.data.get('products_count')):
            raise ValidationError('products_count too big')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
