from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard, name="dashboard"),
    path('nip/',views.nip, name="nip"),
    path('sdd/',views.sdd, name="sdd"),
    path('srd/',views.srd, name="srd"),
    path('learning/',views.learning, name="learning"),
    path('workflow/',views.workflow, name="workflow"),
    path('rf_assessment/',views.rf_assessment, name="rf_assessment")
]
