from django.contrib import admin
from subscriptions.models import Category, Subscription

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('service_name','user', 'category', 'price', 'billing_cycle', 'renewal_date', 'status')
    search_fields = ('service_name', 'user__username')
    list_filter = ('status','billing_cycle','category', 'currency')
    list_per_page = 20
    ordering = ('renewal_date',)
    date_hierarchy = 'renewal_date'