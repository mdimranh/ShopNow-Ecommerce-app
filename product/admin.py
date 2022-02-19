from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import *

# admin.site.register(Images)

class productImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ['image_tag']
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'enable', 'created_at', 'updated_at', 'price_per', 'image_tag']
    list_filter = ['title', 'created_at']
    list_per_page = 10
    search_fields = ['title', 'new_price', 'detail']
    inlines = [productImageInline]
    class Media:
        js=("product_category.js",)
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Product, ProductAdmin)
admin.site.register(Review)

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['pro', 'image_tag']
admin.site.register(Images, ImagesAdmin)


# class CategoryAdmin(DraggableMPTTAdmin):
#     mptt_indent_field = "title"
#     list_display = ('tree_actions', 'indented_title',
#                     'related_products_count', 'related_products_cumulative_count')
#     list_display_links = ('indented_title',)

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)

#         # Add cumulative product count
#         qs = Category.objects.add_related_count(
#                 qs,
#                 Product,
#                 'category',
#                 'products_cumulative_count',
#                 cumulative=True)

#         # Add non cumulative product count
#         qs = Category.objects.add_related_count(qs,
#                  Product,
#                  'category',
#                  'products_count',
#                  cumulative=False)
#         return qs

#     def related_products_count(self, instance):
#         return instance.products_count
#     related_products_count.short_description = 'Related products (for this specific category)'

#     def related_products_cumulative_count(self, instance):
#         return instance.products_cumulative_count
#     related_products_cumulative_count.short_description = 'Related products (in tree)'

# admin.site.register(Category, CategoryAdmin)

class GroupInline(admin.TabularInline):
    model = Group
    extra = 0
    readonly_fields = ['total_subcategory']
    # classes = ['collapse']

class SubctegoryInline(admin.TabularInline):
    model = Subcategory
    extra = 0
    readonly_fields = ['total_product']
    # classes = ['collapse']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'Total_Group', 'Total_Subcategory', 'image_tag']
    inlines = [GroupInline, SubctegoryInline]
    prepopulated_fields = {'slug':('name',)}
    class Media:
        js=("category.js",)
admin.site.register( Category, CategoryAdmin)

class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_tag']
admin.site.register(Brands, BrandAdmin)

class RecentlyViewAdmin(admin.ModelAdmin):
    list_display = ['product', 'on_create']
admin.site.register(RecentlyView, RecentlyViewAdmin)
