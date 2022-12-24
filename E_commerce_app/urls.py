from django.urls import path
from .views import post_category,MultiplefilterAPI,delete_table


urlpatterns = [

    path('post_category/',post_category.as_view(),name='post_category'),

    path('MultiplefilterAPI',MultiplefilterAPI.as_view(),name="MultiplefilterAPI"),

    path('delete/',delete_table)
]
