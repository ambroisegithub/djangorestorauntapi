from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items/',views.MenuItemView.as_view()),
    path('menu-items/<int:pk>',views.SingletMenuItemView.as_view()),
    path('menu-item/', views.menu_items),
    path('menu-itemp/',views.create_item),
    path('menu-item/<int:id>', views.update_item),
    path('menu-item/<int:id>',views.delete_item),
    path('secret/',views.secret),
    path('api-token-auth/',obtain_auth_token),
    path('manager-view/',views.manager_view),
    path('groups/manager/users',views.managers)
    
    
]
