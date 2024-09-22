from django.contrib import admin
from django.urls import path, include
from .views import user_check_view, register_view

admin.site.site_header ="Login to Golden Penny User Check Portal"
admin.site.site_title ="Welcome to Goden Penny REGISTRATION Dashboard"
admin.site.index_title ="Welcome to Golden Penny User's Dashboard"

urlpatterns = [
    path('', user_check_view, name='user_check_page'),  # URL for the HTML page
    # path('api/user_check', UserCheckView.as_view(), name='user_check'),  # URL for the API
    path('register/', register_view, name='register_page'),  # Registration page

]