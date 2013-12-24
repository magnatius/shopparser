# -*- coding: utf-8 -*-
from django.db import models

class Source(models.Model):
    title = models.CharField(u'Название источника', max_length=255)
    url = models.URLField(u'Ссылка')
    sync_date = models.DateTimeField(u'Дата последней синхронизации', blank=True, null=True)
    parser = models.CharField(max_length=250)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = u"Источник данных"
        verbose_name_plural = u"Источники данных"

class Category(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    source = models.ForeignKey(Source, related_name='categories')
    external_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    updated = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = u"Категория"
        verbose_name_plural = u"Категории"

class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products')
    source = models.ForeignKey(Source, related_name='products')
    external_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    updated = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = u"Товар"
        verbose_name_plural = u"Товары"

class Param(models.Model):
    product = models.ForeignKey(Product, related_name='params')
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    updated = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = u"Параметр товара"
        verbose_name_plural = u"Параметры товара"