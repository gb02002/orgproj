from .views import *
from django.urls import path

urlpatterns = ([
    # API for DRF
    path('api/listlocations/', LocationListApiView.as_view(), name="list_loc.api"),
    path('api/filterlocation/', LocationBoundsFiltersView.as_view(), name="filter_map.api"),
    path('api/filters/', GetFiltersApiView.as_view(), name='filterapi'),

    # Lists
    path('organisations/', OrganisationListView.as_view(), name='organisation_list_filtered'),
    path('organisation/<int:pk>-<slug:slug>/', OrganisationDetailView.as_view(),
         name='organisation-detail'),

    # For_orgs
    path('for_orgs/edit-choice/', ChoiceEditView.as_view(), name='edit-choice'),
    path('for_orgs/edit-choice/add-org-1/', AddOrg.as_view(), name='add-org-1'),
    path('for_orgs/edit-choice/add-org-1/<int:pk>/', AddLocforExistingOrgView.as_view(), name='add-loc'),
    path('for_orgs/edit-choice/delete-org/<int:pk>/', DelOrgView.as_view(), name='del-org'),
    path('for_orgs/edit-choice/delete-loc/<int:pk>/', DelLocOfOrgView.as_view(), name='del-loc'),
    path('for_orgs/edit-choice/edit-org/<int:pk>/', EditOrgView.as_view(), name='edit-org'),
    path('for_orgs/edit-choice/edit-loc/<int:pk>/', EditLocView.as_view(), name='edit-loc'),
    path('for_orgs/edit-choice/add-loc-media/<int:pk>/', AddLocMedia.as_view(), name='add-loc-media'),
    path('for_orgs/edit-choice/edit-loc-media/<int:pk>/', EditLocMediaView.as_view(),
         name='edit-loc-media'),
    path('for_orgs/edit-choice/del-loc-media/<int:pk>/', DelLocMediaView.as_view(),
         name='del-loc-media'),
])
