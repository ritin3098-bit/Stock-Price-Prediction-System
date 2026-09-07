from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone

class StockData(models.Model):
    symbol = models.CharField(max_length=10, db_index=True)
    company_name = models.CharField(max_length=200)
    date = models.DateField()
    open = models.FloatField(validators=[MinValueValidator(0.0)])
    high = models.FloatField(validators=[MinValueValidator(0.0)])
    low = models.FloatField(validators=[MinValueValidator(0.0)])
    close = models.FloatField(validators=[MinValueValidator(0.0)])
    # allow null/blank in case CSV has missing volumes
    volume = models.BigIntegerField(null=True, blank=True, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ['symbol', 'date']
        constraints = [
            models.UniqueConstraint(fields=['symbol', 'date'], name='unique_symbol_date')
        ]
        indexes = [
            models.Index(fields=['symbol', 'date']),
            models.Index(fields=['date']),
        ]
        verbose_name_plural = "Stock Data"

    def __str__(self):
        # include company name to make admin list easier to read
        return f"{self.symbol} - {self.company_name} - {self.date}"


class Prediction(models.Model):
    ALGORITHM_CHOICES = [
        ('linear', 'Linear Regression'),
        ('lstm', 'LSTM Neural Network'),
    ]

    symbol = models.CharField(max_length=10, db_index=True)
    company_name = models.CharField(max_length=200)
    algorithm = models.CharField(max_length=20, choices=ALGORITHM_CHOICES)
    prediction_date = models.DateField()
    predicted_price = models.FloatField(validators=[MinValueValidator(0.0)])
    actual_price = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0)])
    accuracy = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['symbol']),
            models.Index(fields=['algorithm']),
        ]

    def __str__(self):
        return f"{self.symbol} - {self.algorithm} - {self.prediction_date}"

    def calculate_accuracy(self):
        """
        Computes accuracy as percentage closeness: (1 - abs(error)/actual) * 100
        Guards against division by zero and missing actual_price.
        """
        if self.actual_price is None:
            return None
        try:
            if self.actual_price == 0:
                self.accuracy = None
            else:
                error = abs(self.predicted_price - self.actual_price)
                self.accuracy = (1 - error / self.actual_price) * 100
            self.save(update_fields=['accuracy'])
            return self.accuracy
        except Exception:
            # don't crash on unexpected values
            self.accuracy = None
            self.save(update_fields=['accuracy'])
            return None


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Profile"


class SearchHistory(models.Model):
    # reuse the same choices to keep algorithm values consistent
    ALGORITHM_CHOICES = Prediction.ALGORITHM_CHOICES

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')
    symbol = models.CharField(max_length=10, db_index=True)
    company_name = models.CharField(max_length=200)
    algorithm = models.CharField(max_length=20, choices=ALGORITHM_CHOICES)
    forecast_days = models.IntegerField(validators=[MinValueValidator(1)])
    predicted_price = models.FloatField(validators=[MinValueValidator(0.0)])
    current_price = models.FloatField(validators=[MinValueValidator(0.0)])
    price_change_percent = models.FloatField()
    searched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-searched_at']
        verbose_name_plural = "Search Histories"
        indexes = [
            models.Index(fields=['user', 'symbol']),
            models.Index(fields=['-searched_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.symbol} - {self.searched_at.isoformat()}"
