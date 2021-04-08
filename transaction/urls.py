from django.conf.urls import url, include
from transaction import views


urlpatterns = [
    url(r'^transaction/(?P<transaction_id>[0-9]+)' , views.transaction),
    url(r'^types/(?P<type>.*$)' , views.transaction_list),
    url(r'^sum/(?P<transaction_id>[0-9]+)' , views.related_transaction_sum),
]