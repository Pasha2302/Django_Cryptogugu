from django.urls import path, re_path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("get-user-id/", views.get_user_id, name="get_user_id"),
    path("set-theme-site/", views.set_theme_site, name="set_theme_site"),

    path("set-settings-user/", views.set_settings_user, name="set_settings_user"),
    path("show-more/", views.show_more, name="show_more"),

    path("airdrops/", views.airdrops, name="airdrops"),
    path("promote/", views.promote, name="promote"),

    path("clear-settings/", views.clear_settings, name="clear_settings"),
    path("reset-all-votes/", views.reset_all_votes, name="reset_all_votes"),


    path("header-search-component/", views.get_header_search_component, name="header_search_component"),
    path("table-promoted-coins-component/", views.get_table_promoted_coins_component, name="get_table_promoted_coins_component"),

    path("voting/", views.voting, name="voting"),

    # path('accounts/profile/', views.profile_view, name='profile'),
    # path("slots/<slug:slug_slot>", views.one_slot, name="one_slot"),
    # path(r"test_paginator/slots", views.SlotsListView.as_view(), name="slots_list"),

]
