from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    cat_name = models.CharField(("Category Name"), max_length=50, unique=True)
    cat_slug = models.SlugField(("Category Slug"), max_length=50, unique=True) 
    cat_image = models.ImageField(("Category Image"), upload_to='photos/categories', blank=True)
    description = models.TextField(("Description"), blank=True)
    cat_icon = models.CharField(("Category Icon"), max_length=50, blank=True)


    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def get_url(self):
        return reverse('products_by_category', args=[self.cat_slug])

    def __str__(self):
        return self.cat_name
