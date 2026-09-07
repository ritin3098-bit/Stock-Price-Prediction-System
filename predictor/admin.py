from django.contrib import admin
from .models import StockData, Prediction, UserProfile, SearchHistory

@admin.register(StockData)
class StockDataAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'company_name', 'date', 'open', 'high', 'low', 'close', 'volume']
    list_filter = ['symbol', 'date']
    search_fields = ['symbol', 'company_name']
    ordering = ['symbol', '-date']
    date_hierarchy = 'date'
    
    list_per_page = 100
    
    fieldsets = (
        ('Company Information', {
            'fields': ('symbol', 'company_name', 'date')
        }),
        ('Price Data', {
            'fields': ('open', 'high', 'low', 'close')
        }),
        ('Trading Volume', {
            'fields': ('volume',)
        }),
    )

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'company_name', 'algorithm', 'prediction_date', 'predicted_price', 'actual_price', 'accuracy', 'created_at']
    list_filter = ['algorithm', 'symbol', 'created_at']
    search_fields = ['symbol', 'company_name']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    list_per_page = 50
    
    readonly_fields = ['created_at', 'accuracy']
    
    fieldsets = (
        ('Prediction Details', {
            'fields': ('symbol', 'company_name', 'algorithm', 'prediction_date')
        }),
        ('Price Information', {
            'fields': ('predicted_price', 'actual_price')
        }),
        ('Accuracy Metrics', {
            'fields': ('accuracy', 'created_at')
        }),
    )
    
    actions = ['calculate_accuracy']
    
    def calculate_accuracy(self, request, queryset):
        count = 0
        for prediction in queryset:
            if prediction.actual_price:
                prediction.calculate_accuracy()
                count += 1
        self.message_user(request, f'{count} predictions updated with accuracy.')
    calculate_accuracy.short_description = "Calculate accuracy for selected predictions"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'created_at']
    search_fields = ['user__username', 'user__email']
    list_filter = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'phone')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
    
    readonly_fields = ['created_at']

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'symbol', 'company_name', 'algorithm', 'forecast_days', 'predicted_price', 'price_change_percent', 'searched_at']
    list_filter = ['algorithm', 'user', 'searched_at']
    search_fields = ['symbol', 'company_name', 'user__username']
    ordering = ['-searched_at']
    date_hierarchy = 'searched_at'
    
    list_per_page = 50
    
    readonly_fields = ['searched_at']
    
    fieldsets = (
        ('User & Company', {
            'fields': ('user', 'symbol', 'company_name')
        }),
        ('Prediction Details', {
            'fields': ('algorithm', 'forecast_days')
        }),
        ('Price Information', {
            'fields': ('current_price', 'predicted_price', 'price_change_percent')
        }),
        ('Timestamp', {
            'fields': ('searched_at',)
        }),
    )