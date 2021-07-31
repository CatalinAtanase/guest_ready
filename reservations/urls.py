from django.urls import path

from . import views

app_name='reservations'

urlpatterns = [
    path('total-commission/', views.total_commission, name="total_commission"),
    path('commission-per-month/', views.commission_per_month,
         name="commission_per_month"),
    path('commission-by-city/', views.commission_by_city,
         name="commission_by_city"),
    path('commission-for-city/<city>/', views.commission_for_city,
         name="commission_for_city"),
    path('load-csv/', views.load_csv, name='load_csv'),
]
