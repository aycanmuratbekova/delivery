from django.db import models


class Establishment(models.Model):
    """ Модель для Заведения """
    name = models.CharField(max_length=30, verbose_name='Название Карточки', unique=True)
    description = models.TextField(verbose_name='Описание Карточки', null=True, blank=True)
    service_price = models.PositiveIntegerField(verbose_name='%  за обслуживание')
    delivery_price = models.PositiveIntegerField(verbose_name='Цена за доставку')
    # container_price = models.PositiveIntegerField(verbose_name='Цена за 1 контейнер')

    class Meta:
        verbose_name = 'Заведение'
        verbose_name_plural = 'Заведения'

    def __str__(self):
        return f"id: {self.id}, name: {self.name}"


class Product(models.Model):
    """ Модель для Product """

    name = models.CharField(max_length=100, verbose_name='Название продукта')
    price = models.PositiveIntegerField(verbose_name='Цена продукта', default=0)
    cafe = models.ForeignKey(Establishment, related_name='products', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f"id: {self.id}, name: {self.name}"


def get_totall(order_id):
    total = 0
    order = Order.objects.get(id=order_id)
    order_itmems = order.order_items.all()

    if order.order_type == 1:
        """если тип заказа: обслуживание"""

        for item in order_itmems:
            total += item.product.price * item.amount
        return total + int(total/100) * order_itmems[0].product.cafe.service_price

    elif order.order_type == 2:
        """если тип заказа: доставка"""

        for item in order_itmems:
            total += item.product.price * item.amount
        return total + order_itmems[0].product.cafe.delivery_price
    else:
        """если тип заказа: pick up - то есть клиент сам забирает"""

        for item in order_itmems:
            total += item.product.price * item.amount
        return total


class Order(models.Model):
    """ Модель для OrderDetails """

    TYPE_CHOICES = [
        (1, 'Service'),
        (2, 'Delivery'),
        (3, 'Pickup'),
    ]
    order_type = models.IntegerField(verbose_name='Тип Заказа', choices=TYPE_CHOICES, default=1)
    created_at = models.DateTimeField(verbose_name='создан в ', auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name='обнавлен в ', auto_now_add=True)
    total = models.PositiveIntegerField(verbose_name='Общая сумма заказа', default=0)
    paid = models.BooleanField(verbose_name='Оплачено', default=False)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"id: {self.id}, order_type: {self.order_type}"


class OrderItem(models.Model):
    """ Модель для OrderItem """
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name='Количество продукта', default=1)

    class Meta:
        verbose_name = 'Единица Заказа'
        verbose_name_plural = 'Единицы Заказа'

    def __str__(self):
        return str(self.id)


class Delivery(models.Model):
    """ Модель для Доставки """

    address = models.CharField(max_length=100, verbose_name='Адрес')
    phone = models.CharField(max_length=13, verbose_name='Номер Телефона')
    description = models.TextField(max_length=255, verbose_name='Описание для Доставщика', null=True, blank=True)
    order = models.ForeignKey(Order, related_name='delivery_address', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'

    def __str__(self):
        return str(self.id)

