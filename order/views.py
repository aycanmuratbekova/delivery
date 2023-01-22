from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from order import models, serializers
from order.models import get_totall


class OrderListAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, format=None):
        """
            Return a list of all Orders.
        """
        orders = models.Order.objects.all()
        for order in orders:
            order.total = get_totall(order.id)
            order.save()
        serializer = serializers.OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=serializers.OrderSerializer)
    def post(self, request, format=None):
        serializer = serializers.OrderSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    """
    Retrieve, update or delete a order instance.
    """
    def get_object(self, pk):
        try:
            return models.Order.objects.get(pk=pk)
        except models.Order.objects.get(pk=pk).DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):

        order = self.get_object(pk)
        order.total = get_totall(order.id)

        serializer = serializers.OrderDetailSerializer(order)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializers.OrderDetailSerializer)
    def put(self, request, pk, format=None):

        order = self.get_object(pk)

        serializer = serializers.OrderDetailSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=serializers.OrderDetailSerializer)
    def patch(self, request, pk, format=None):

        order = self.get_object(pk)
        self.check_object_permissions(request, order)

        serializer = serializers.OrderDetailSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):

        order = self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EstablishmentAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, format=None):
        """
            Return a list of all Establishments.
        """
        establishment = models.Establishment.objects.all()
        serializer = serializers.EstablishmentSerializer(establishment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=serializers.EstablishmentSerializer)
    def post(self, request, format=None):
        serializer = serializers.EstablishmentSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EstablishmentCRUDAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    """
    Retrieve, update or delete a Establishment instance.
    """
    def get_object(self, pk):
        try:
            return models.Establishment.objects.get(pk=pk)
        except models.Establishment.objects.get(pk=pk).DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):

        establishment = self.get_object(pk)

        serializer = serializers.EstablishmentSerializer(establishment)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializers.EstablishmentSerializer)
    def put(self, request, pk, format=None):

        order = self.get_object(pk)

        serializer = serializers.EstablishmentSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=serializers.EstablishmentSerializer)
    def patch(self, request, pk, format=None):

        establishment = self.get_object(pk)
        self.check_object_permissions(request, establishment)

        serializer = serializers.EstablishmentSerializer(establishment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):

        establishment = self.get_object(pk)
        establishment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderItemAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, format=None):
        """
        Return a list of all OrderItems.
        """
        order_items = models.OrderItem.objects.all()
        serializer = serializers.OrderItemSerializer(order_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=serializers.OrderItemSerializer)
    def post(self, request, format=None):
        serializer = serializers.OrderItemSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            order = models.Order.objects.get(id=request.data['order'])
            order.total = get_totall(order.id)
            print(f"\n\norder.total: {order.total}\n\n")
            order.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderItemDetailAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    """
    Retrieve, update or delete a order instance.
    """
    def get_object(self, pk):
        try:
            return models.OrderItem.objects.get(pk=pk)
        except models.OrderItem.objects.get(pk=pk).DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):

        order = self.get_object(pk)

        serializer = serializers.OrderItemSerializer(order)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializers.OrderItemSerializer)
    def put(self, request, pk, format=None):

        order = self.get_object(pk)

        serializer = serializers.OrderItemSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=serializers.OrderItemSerializer)
    def patch(self, request, pk, format=None):

        order = self.get_object(pk)
        self.check_object_permissions(request, order)

        serializer = serializers.OrderItemSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):

        order = self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, format=None):
        """
        Return a list of all OrderItems.
        """
        order_items = models.Product.objects.all()
        serializer = serializers.ProductSerializer(order_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=serializers.ProductSerializer)
    def post(self, request, format=None):
        serializer = serializers.ProductSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCRUDAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    """
    Retrieve, update or delete a order instance.
    """
    def get_object(self, pk):
        try:
            return models.Product.objects.get(pk=pk)
        except models.Product.objects.get(pk=pk).DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):

        order = self.get_object(pk)

        serializer = serializers.ProductSerializer(order)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializers.ProductSerializer)
    def put(self, request, pk, format=None):

        order = self.get_object(pk)

        serializer = serializers.ProductSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=serializers.ProductSerializer)
    def patch(self, request, pk, format=None):

        order = self.get_object(pk)
        self.check_object_permissions(request, order)

        serializer = serializers.ProductSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):

        order = self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeliveryAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, format=None):
        """
        Return a list of all OrderItems.
        """
        deliveries = models.Delivery.objects.all()
        serializer = serializers.DeliverySerializer(deliveries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=serializers.DeliverySerializer)
    def post(self, request, format=None):
        serializer = serializers.DeliverySerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeliveryCRUDAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    """
    Retrieve, update or delete a order instance.
    """

    def get_object(self, pk):
        try:
            return models.Delivery.objects.get(pk=pk)
        except models.Delivery.objects.get(pk=pk).DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):

        order = self.get_object(pk)

        serializer = serializers.DeliverySerializer(order)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializers.DeliverySerializer)
    def put(self, request, pk, format=None):

        order = self.get_object(pk)

        serializer = serializers.DeliverySerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=serializers.DeliverySerializer)
    def patch(self, request, pk, format=None):

        order = self.get_object(pk)
        self.check_object_permissions(request, order)

        serializer = serializers.DeliverySerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):

        order = self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeliveryOrderListAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, format=None):
        """
        Return a list of all DeliveryOrderListAPIView.
        """
        orders = models.Order.objects.filter(order_type=2)
        serializer = serializers.OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InPlaceOrderListAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, format=None):
        """
        Return a list of all InPlaceOrderListAPIView.
        """
        orders = models.Order.objects.filter(order_type=1)
        serializer = serializers.OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PickUpOrderListAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, format=None):
        """
        Return a list of all PickUpOrderListAPIView.
        """
        orders = models.Order.objects.filter(order_type=3)
        serializer = serializers.OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EstablishmentOrderListAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    """
    Return a list of all Orders by Establishment.
    """

    def get_object(self, pk):
        try:
            return models.Establishment.objects.get(pk=pk)
        except models.Establishment.objects.get(pk=pk).DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):

        establishment = self.get_object(pk)

        orders = models.Order.objects.filter(order_items=establishment.products.order_items.orders)

        serializer = serializers.OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#######################################################################################################################


#######################################################################################################################


class CreateOrderAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(request_body=serializers.CreateOrderSerializer)
    def post(self, request, format=None):
        order = models.Order.objects.create(
            order_type=1
        )
        order.save()
        data = request.data.copy()
        data['order'] = order.id
        print(f"\n\ndata:{data}\norderid:{order.id}\n")
        serializer = serializers.OrderItemSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








