from datetime import datetime

from django.http import Http404
from rest_framework import serializers
from . import models


class EstablishmentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=30)
    description = serializers.CharField()
    service_price = serializers.IntegerField()
    delivery_price = serializers.IntegerField()

    def create(self, validated_data):
        return models.Establishment.objects.create(**validated_data)


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    price = serializers.IntegerField()
    cafe = serializers.CharField()

    def create(self, validated_data):
        try:
            validated_data['cafe'] = models.Establishment.objects.get(id=validated_data['cafe'])
        except models.Establishment.objects.get(id=validated_data['cafe']).DoesNotExist:
            raise Http404
        return models.Product.objects.create(**validated_data)


class DeliverySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    address = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=13)
    description = serializers.CharField(max_length=255)
    order = serializers.CharField()

    def create(self, validated_data):
        try:
            validated_data['order'] = models.Order.objects.get(id=validated_data['order'])
        except models.Order.objects.get(id=validated_data['order']).DoesNotExist:
            raise Http404
        validated_data['order'].order_type = 2
        validated_data['order'].save()
        return models.Delivery.objects.create(**validated_data)


class OrderItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order = serializers.CharField()
    product = serializers.CharField()
    amount = serializers.IntegerField()

    def create(self, validated_data):
        try:
            validated_data['order'] = models.Order.objects.get(id=validated_data['order'])
        except models.Order.objects.get(id=validated_data['order']).DoesNotExist:
            raise Http404
        try:
            validated_data['product'] = models.Product.objects.get(id=validated_data['product'])
        except models.Product.objects.get(id=validated_data['product']).DoesNotExist:
            raise Http404

        return models.OrderItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.order = validated_data.get('order', instance.order)
        instance.product = validated_data.get('product', instance.product)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.save()
        return instance


class DelivSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    address = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=13)
    description = serializers.CharField(max_length=255)


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order_type = serializers.IntegerField(max_value=3, min_value=1)
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)
    total = serializers.IntegerField(read_only=True)
    paid = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        return models.Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.order_type = validated_data.get('order_type', instance.order_type)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super(OrderSerializer, self).to_representation(instance)
        if instance.delivery_address.exists():
            representation['delivery_address'] = DelivSerializer(instance.delivery_address.all(), many=True).data
        if instance.order_items.exists():
            representation['order_items'] = OrderItemSerializer(instance.order_items.all(), many=True).data
        return representation


class OrderDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order_type = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)
    total = serializers.IntegerField(read_only=True)
    paid = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        return models.Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.order_type = validated_data.get('order_type', instance.order_type)
        instance.modified_at = datetime.now()
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super(OrderDetailSerializer, self).to_representation(instance)
        if instance.delivery_address.exists():
            representation['delivery_address'] = DelivSerializer(instance.delivery_address.all(), many=True).data
        if instance.order_items.exists():
            representation['order_items'] = OrderItemSerializer(instance.order_items.all(), many=True).data
        return representation


class CreateOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order_type = serializers.IntegerField(read_only=True)
    product = serializers.CharField()
    amount = serializers.IntegerField()
    price = serializers.IntegerField(read_only=True)

    def createOrderOrderItem(self, validated_data):
        validated_data['order_type'] = 1
        order = models.Order.objects.create(**validated_data)
        validated_data2 = validated_data['product']
        validated_data2['product'] = validated_data['product']
        validated_data2['amount'] = validated_data['amount']
        validated_data2['order'] = order
        order_item = models.OrderItem.objects.create(**validated_data2)
        return {'order': order,'order_item': order_item}


class CreateDeliveryOrder(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order_type = serializers.IntegerField(max_value=3, min_value=1)
    address = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=13)
    description = serializers.CharField(max_length=255)
    order = serializers.CharField()

    def create(self, validated_data):
        try:
            validated_data['order'] = models.Order.objects.get(id=validated_data['order'])
        except models.Order.objects.get(id=validated_data['order']).DoesNotExist:
            raise Http404
        validated_data['order'].order_type = 2
        validated_data['order'].save()
        return models.Delivery.objects.create(**validated_data)


class CreatePickUpOrder(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order_type = serializers.IntegerField(max_value=3, min_value=1)
    address = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=13)
    description = serializers.CharField(max_length=255)
    order = serializers.CharField()

    def create(self, validated_data):
        try:
            validated_data['order'] = models.Order.objects.get(id=validated_data['order'])
        except models.Order.objects.get(id=validated_data['order']).DoesNotExist:
            raise Http404
        validated_data['order'].order_type = 2
        validated_data['order'].save()
        return models.Delivery.objects.create(**validated_data)

