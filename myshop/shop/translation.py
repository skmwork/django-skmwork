from modeltranslation.translator import translator, TranslationOptions
from shop.models import Product, Category


class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


translator.register(Product, ProductTranslationOptions)


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Category, CategoryTranslationOptions)