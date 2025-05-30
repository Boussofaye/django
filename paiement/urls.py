from django.urls import path
from .views import (
    initier_paiement,
    paiement_success,
    paiement_fail,
    paiement_callback
)

urlpatterns = [
    path('payer/', initier_paiement, name='initier_paiement'),
    path('success/', paiement_success, name='paiement_success'),
    path('fail/', paiement_fail, name='paiement_fail'),
    path('callback/', paiement_callback, name='paiement_callback'),
]