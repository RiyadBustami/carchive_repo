from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.showroom_login),
    path('logging/',views.logging),
    path('logout/',views.showroom_logout),
    path('change_password/',views.change_password),
    path('update_password/',views.update_password),
    path('dashboard/',views.cars_dashboard),
    path('find_by_vin/',views.find_by_vin),
    path('add_new_car/',views.add_new_car),
    path('create_new_car/',views.create_car),
    path('edit_car/<id>/',views.edit_car),
    path('get_models/',views.get_models),
    path('update_car/<id>/',views.update_car),
    path('delete_car/<id>/',views.delete_car),
    path('show_car/<id>/',views.show_car),
    path('upload_doc/<id>/',views.upload_doc),
    path('delete_document/<id>/',views.delete_document),
] 


# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)