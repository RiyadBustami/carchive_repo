from django.urls import path
from . import views

urlpatterns=[
    path('',views.admins_login),
    path('login/',views.login),
    path('logout/',views.logout),
    path('dashboard/',views.admin_dashboard),
    path('add_showroom/',views.add_showroom),
    path('create_showroom/',views.create_showroom),
    path('edit_showroom/<id>/',views.edit_showroom),
    path('update_showroom/<id>/', views.update_showroom),
    path('add_items/',views.add_items),
    path('process_items/',views.process_items),
    path('display_showroom/<id>/', views.display_showroom),
    path('delete_showroom/<id>/', views.delete_showroom),
]