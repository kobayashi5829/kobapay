from django.urls import path
from . import views

app_name = 'paycash'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('home/', views.HomeView.as_view(), name="home"),
    path('history/', views.HistoryView.as_view(), name="history"),
    path('detail/<int:pk>/', views.DetailView.as_view(), name="detail"),
    path('charge/', views.ChargeView.as_view(), name="charge"),
    path('pay/', views.PayView.as_view(), name="pay"),
    path('send/', views.SendView.as_view(), name="send"),
    path('update/<int:pk>/', views.UpdateView.as_view(), name="update"),
    path('delete/<int:pk>/', views.DeleteView.as_view(), name="delete"),
]
