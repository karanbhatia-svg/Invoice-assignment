from django.urls import path
from . import views


urlpatterns = [
    path('', views.getInvoiceList, name="invoice-list"),
    path('create/', views.createInvoice, name="create-invoice"),
    path('update/', views.updateInvoice, name="update-invoice"),
    path('delete/', views.deleteInvoice, name="delete-invoice"),
]