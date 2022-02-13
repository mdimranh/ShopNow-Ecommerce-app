from django.db import models
from django.utils.safestring import mark_safe
from PIL import Image

from django.contrib.auth.models import User

from django.template.defaultfilters import slugify

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from fontawesome_5.fields import IconField
from django.db.models import Q, Sum, Avg

class Category(models.Model):
    name = models.CharField(max_length=200)
    banner = models.ImageField(upload_to = 'category/banner/', blank=True, null=True)
    icon = IconField()
    slug= models.SlugField(null=True, unique=True)
    searchable = models.BooleanField(default=True)
    enable = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def Total_Group(self):
        return Group.objects.filter(category__id=self.id).count()

    def Total_Subcategory(self):
        return Group.objects.filter(category__id=self.id).count()

    def image_tag(self):
        if self.banner:        
            return mark_safe('<img src="{}" heights="100" width="60" />'.format(self.banner.url))
        else:
            return 'Null'
    image_tag.short_description = 'Banner'


class Group(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='groups')
    slug = models.SlugField(null=True)
    searchable = models.BooleanField(default=True)
    enable = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def total_subcategory(self):
        return Subcategory.objects.filter(group__id=self.id).count()

class Subcategory(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, related_name='subcategorys')
    slug= models.SlugField(null=True)
    searchable = models.BooleanField(default=True)
    enable = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def total_product(self):
        return Product.objects.filter(category__id=self.id).count()

class Brands(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="product/brand")

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe('<img src="{}" heights="60" width="60" />'.format(self.logo.url))
    image_tag.short_description = 'Image'


class Product(models.Model):
    dis_type = (
        ('Fixed', 'Fixed'),
        ('Percentage', 'Percentage')
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_categorys', blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, blank=True, null=True, related_name = 'product_groups')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.DO_NOTHING, blank=True, null=True, related_name = 'product_subcategorys')
    title = models.CharField(max_length=200)
    keywords = models.CharField(max_length=100)
    image = models.CharField(max_length=500, blank = True, null=True)
    main_price = models.DecimalField(decimal_places=2, max_digits=15)
    discount = models.DecimalField(decimal_places=0, max_digits=3, blank=True, null=True)
    discount_type = models.CharField(max_length=10, choices=dis_type, default="Percentage")
    hot_deal = models.DateTimeField(blank=True, null=True)
    amount = models.IntegerField(default=3)
    short_info = models.TextField()
    description = RichTextUploadingField()
    additional_info = RichTextUploadingField()
    shipping_info = RichTextUploadingField()
    size = models.CharField(max_length=200, null=True, blank=True)
    color = models.CharField(max_length=500, null=True, blank=True)
    enable = models.BooleanField(default=True)
    slug = models.SlugField(null=True, unique=True)
    meta_title = models.CharField(max_length=200, null=True, blank=True)
    meta_keywords = models.CharField(max_length=200, null=True, blank=True)
    meta_descriptions = models.CharField(max_length=500, null=True, blank=True)
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

    def rating(self):
        rating = Review.objects.filter(product=self).aggregate(Avg('rating'))['rating__avg']
        return rating if type(rating) == float else 0

    def total_review(self):
        return Review.objects.filter(product=self).count()

    # def ImageUrl(self):
    #     if self.image:
    #         return self.image.url
    #     else:
    #         return ""

    def image_tag(self):
        return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.image))
    image_tag.short_description = 'Image'

    # def save(self, *args, **kwargs):
    #     if self.image:
    #         super(Product, self).save(*args, **kwargs)
    #         img = Image.open(self.image.path)
    #         if img.height != 600 and img.width != 600:
    #             output_size = (600,600)
    #             img.thumbnail(output_size)
    #             img.save(self.image.path)

class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(blank=True, upload_to='product/')

    def __str__(self):
        return self.product.title

    def image_tag(self):
        return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.image.url))
    image_tag.short_description = 'Image'

class RecentlyView(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    on_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title
    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, null=True)
    user_name = models.CharField(max_length=200)
    rating = models.IntegerField()
    comment = models.TextField()
    add_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_name
    
    
    