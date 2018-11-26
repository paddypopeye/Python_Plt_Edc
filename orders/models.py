# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from shop.models import Product
from coupons.models import Coupon

# Create your models here.
class Order(models.Model):
	objects = models.Manager()
	first_name = models.CharField(_('first_name'),max_length=50)
	last_name = models.CharField(_('last_name'),max_length=50)
	email = models.EmailField(_('email'),)
	address = models.CharField(_('address'),max_length=250)
	postal_code = models.CharField(_('postal_code'),max_length=250)
	city = models.CharField(_('city'),max_length=100)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	paid = models.BooleanField(default=False)
	coupon = models.ForeignKey(Coupon, related_name='orders', null=True, blank=True)
	discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	


	class Meta:
		ordering = ('-created',)

	def __unicode__(self):
		return 'Order {}'.format(self.id)

	def get_total_cost(self):
		total_cost  = sum(item.get_cost() for item in self.items.all())
		return total_cost - total_cost *(self.discount)

class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name='items')
	product = models.ForeignKey(Product, related_name='order_items')
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1)

	def __unicode__(self):
		return '{}'.format(self.id)

	def get_cost(self):
		return self.price * self.quantity