from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.safestring import mark_safe
from PIL import Image

from ckeditor.fields import RichTextField

class Category(MPTTModel):
    status = (
        ('True', 'True'),
        ('False', 'False')
    )

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    title = models.CharField(max_length=250)
    keywords = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category', blank = True)
    details = models.TextField()
    status = models.CharField(max_length=10, choices=status)
    slug = models.SlugField(null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']
        
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title

class Product(models.Model):
    status = (
        ('True', 'True'),
        ('False', 'False')
    )
    category = TreeForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    keywords = models.CharField(max_length=100)
    image = models.ImageField(blank = True, upload_to = 'product/')
    main_price = models.DecimalField(decimal_places=2, max_digits=15)
    discount = models.DecimalField(decimal_places=0, max_digits=3)
    hot_deal = models.DateTimeField(blank=True, null=True)
    amount = models.IntegerField(default=3)
    description = models.TextField()
    detail = RichTextField()
    status = models.CharField(max_length=10, choices=status)
    slug = models.SlugField(null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def price(self):
        if self.main_price > 0:
            return self.main_price - (self.main_price * self.discount / 100)
        else:
            return 0
    
    def price_per(self):
        if self.main_price > 0:
            return f"{self.main_price - (self.main_price * self.discount / 100)} (-{self.discount}%)"
        else:
            return 0

    def ImageUrl(self):
        if self.image:
            return self.image.url
        else:
            return ""

    def image_tag(self):
        return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.image.url))
    image_tag.short_description = 'Image'

    def save(self, *args, **kwargs):
        if self.image:
            super(Product, self).save(*args, **kwargs)
            img = Image.open(self.image.path)
            if img.height != 600 and img.width != 600:
                output_size = (600,600)
                img.thumbnail(output_size)
                img.save(self.image.path)

class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(blank=True, upload_to='product/')

    def __str(self):
        return self.title
    
    