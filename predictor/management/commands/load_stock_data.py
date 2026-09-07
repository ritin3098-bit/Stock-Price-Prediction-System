"""
Django management command to load stock data from CSV
Place this file in: predictor/management/commands/load_stock_data.py

Create directories if they don't exist:
predictor/management/__init__.py
predictor/management/commands/__init__.py
predictor/management/commands/load_stock_data.py
"""

from django.core.management.base import BaseCommand
from predictor.models import StockData
import pandas as pd
from datetime import datetime

class Command(BaseCommand):
    help = 'Load stock data from CSV file into database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv-path',
            type=str,
            default=r"C:\Users\LOQ\Desktop\stock_data.csv",
            help='Path to the CSV file'
        )

    def handle(self, *args, **options):
        csv_path = options['csv_path']
        
        self.stdout.write(self.style.WARNING(f'Loading data from: {csv_path}'))
        
        try:
            # Read CSV file
            df = pd.read_csv(csv_path)
            
            self.stdout.write(self.style.SUCCESS(f'Found {len(df)} records in CSV'))
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            
            # Clear existing data
            StockData.objects.all().delete()
            
            # Load new data
            records_created = 0
            batch_size = 1000
            stock_objects = []
            
            for idx, row in df.iterrows():
                stock_obj = StockData(
                    symbol=row['symbol'],
                    date=pd.to_datetime(row['date']).date(),
                    open=float(row['open']),
                    high=float(row['high']),
                    low=float(row['low']),
                    close=float(row['close']),
                    volume=int(row['volume'])
                )
                stock_objects.append(stock_obj)
                
                # Bulk create in batches
                if len(stock_objects) >= batch_size:
                    StockData.objects.bulk_create(stock_objects, ignore_conflicts=True)
                    records_created += len(stock_objects)
                    stock_objects = []
                    self.stdout.write(f'Loaded {records_created} records...')
            
            # Create remaining records
            if stock_objects:
                StockData.objects.bulk_create(stock_objects, ignore_conflicts=True)
                records_created += len(stock_objects)
            
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {records_created} stock records!'))
            
            # Show summary
            companies = StockData.objects.values('symbol').distinct().count()
            self.stdout.write(self.style.SUCCESS(f'Total companies: {companies}'))
            
            # Show sample data
            self.stdout.write(self.style.WARNING('\nSample data:'))
            for stock in StockData.objects.all()[:5]:
                self.stdout.write(f'  {stock.symbol} - {stock.date} - Close: ${stock.close}')
                
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Error: File not found at {csv_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading data: {str(e)}'))

"""
Usage:
    python manage.py load_stock_data
    
Or with custom path:
    python manage.py load_stock_data --csv-path "path/to/your/file.csv"
"""