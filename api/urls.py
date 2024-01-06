from django.urls import path
from .views import signup_view, login_view, search_users, manage_friend_request, list_friends, pending_requests, send_request

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('search-users/', search_users, name='search_users'),
    path('manage-friend-requests/', manage_friend_request, name='manage_friend_request'),
    path('list-friends/', list_friends, name='list_friends'),
    path('pending-requests/', pending_requests, name='pending_requests'),
    path('send-request/', send_request, name='send_request')
]