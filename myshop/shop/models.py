from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from modeltranslation.translator import translator, TranslationOptions


class Category(models.Model):
    name = models.CharField(_('Category name'), max_length=200, db_index=True)
    slug = models.SlugField(_('Slug'), max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(_('Product name'), max_length=200, db_index=True)
    slug = models.SlugField(_('Slug'), max_length=200, db_index=True)
    image = models.ImageField(_('Image'), upload_to='media/products/%Y/%m/%d', blank=True)
    description = models.TextField(_('Description'), blank=True)
    price = models.DecimalField(_('Price'), max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(_('Stock'))
    available = models.BooleanField(_('Available'), default=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])


