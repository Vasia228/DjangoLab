from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Item(models.Model):
    name = models.CharField('название товара', max_length=200)
    description = models.TextField('описание товара')
    price = models.FloatField('цена товара')
    
    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('ShopApp:detail', kwargs={'item_id': self.id})

    def average_mark(self):
        comments = Comment.objects.filter(item=self.id)
        average_score = 0
        for c in comments:
            average_score += c.mark

        length = len(comments)
        if length > 0:
            average_score = average_score/length
        else:
            average_score = 0
        return average_score


class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField('текст комента')
    added = models.DateField('дата добавления', default=timezone.now)
    mark = models.IntegerField('оценка')
    
    def __str__(self):
        return self.text


class Order(models.Model):
    name = models.CharField('имя заказчика', max_length=50)
    email = models.CharField('контакт для связи', max_length=50)
    added = models.DateField('дата добавления', default=timezone.now)
    is_done = models.BooleanField('заказ обработан', default=False)

    def __str__(self):
        return self.name


class OrderElement(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.IntegerField('Кол-ва товара', default=0)

    def __str__(self):
        return self.item.name
