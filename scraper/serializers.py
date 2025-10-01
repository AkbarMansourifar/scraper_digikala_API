from rest_framework import serializers

class ProductSerializer(serializers.Serializer):
    title = serializers.CharField(allow_null=True, allow_blank=True)
    product_url = serializers.CharField(allow_null=True, allow_blank=True)
    category = serializers.CharField(allow_null=True, allow_blank=True)
    image_url = serializers.CharField(allow_null=True, allow_blank=True)
    rating = serializers.FloatField(allow_null=True)
    price = serializers.IntegerField(allow_null=True)
