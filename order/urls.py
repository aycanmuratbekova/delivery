from django.urls import path


from . import views


urlpatterns = [
    path('order/', views.OrderListAPIView.as_view()),
    path('order/<int:pk>/', views.OrderDetailAPIView.as_view()),

    path('order-item/', views.OrderItemAPIView.as_view()),
    path('order-item/<int:pk>/', views.OrderItemDetailAPIView.as_view()),

    path('product/', views.ProductAPIView.as_view()),
    path('product/<int:pk>/', views.ProductCRUDAPIView.as_view()),

    path('delivery/', views.DeliveryAPIView.as_view()),
    path('delivery/<int:pk>/', views.DeliveryCRUDAPIView.as_view()),

    path('establishment/', views.EstablishmentAPIView.as_view()),
    path('establishment/<int:pk>/', views.EstablishmentCRUDAPIView.as_view()),

    path('get/delivery-orders/', views.DeliveryOrderListAPIView.as_view()),
    path('get/in-place-orders/', views.InPlaceOrderListAPIView.as_view()),
    path('get/pick-up-orders/', views.PickUpOrderListAPIView.as_view()),
    path('get/establishment-orders/<int:pk>/', views.EstablishmentOrderListAPIView.as_view()),

    path('api/create-order/', views.CreateOrderAPIView.as_view()),

 ]
