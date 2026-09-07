from django.urls import path

from . import views

app_name = 'predictor'

urlpatterns = [
    # Authentication URLs
   
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Main URLs
    path('', views.index, name='index'),
    path('predict/linear/', views.predict_linear_regression, name='predict_linear'),
    path('predict/lstm/', views.predict_lstm, name='predict_lstm'),
    path('company/info/', views.get_company_info, name='company_info'),
    
    # History URLs
    path('history/', views.search_history, name='history'),
    path('history/delete/<int:history_id>/', views.delete_history, name='delete_history'),
    path('history/clear/', views.clear_all_history, name='clear_history'),
]