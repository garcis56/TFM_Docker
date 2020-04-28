# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 22:05:51 2020

@author: clboe
"""

from django.urls import path
from django.contrib import admin

from . import views

from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('about/', views.about_view),
    path('contact/', views.contact),
    path('hard_skills/', views.hard_skills_view),
    path('soft_skills/', views.soft_skills_view),
    path('events/', views.events_view),
    path('languages/', views.languages_view),
    path('sports/', views.sports_view),
    path('home/', views.home),
    path('activation_sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('profile/',views.view_profile),
    path('edit-profile/',views.edit_profile),
    path('change-password/',views.change_password),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('reset-password/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',
             PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

