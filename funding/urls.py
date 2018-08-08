from . import views

from django.urls import path

urlpatterns = [
    path(
        'create-funding-source/',
        views.FundingSourceCreateView.as_view(),
        name='create-funding-source',
    ),
    path(
        'create-publication/',
        views.PublicationCreateView.as_view(),
        name='create-publication',
    ),
    path(
        'list/',
        views.AttributionListView.as_view(),
        name='list-attributions',
    ),
    path(
        'list/publications/',
        views.PublicationListView.as_view(),
        name='list-publications',
    ),
    path(
        'list/fundingsources/',
        views.FundingSourceListView.as_view(),
        name='list-funding_sources',
    ),
    path(
        '<int:pk>/update/',
        views.AttributionUpdateView.as_view(),
        name='update-attribution',
    ),
    path(
        '<int:pk>/delete/',
        views.AttributioneDeleteView.as_view(),
        name='delete-attribution',
    ),
]