from django.urls import path
from .views import *

urlpatterns = [
	path('login/', LoginView.as_view(), name='login'),
	path('register/', RegisterView.as_view(), name='register'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('task/', ToDoTaskView.as_view(), name='index'),
	path('todo/add/', ToDoTaskCreateView.as_view(), name='add'),
	path('todo/delete/<int:pk>/', ToDoTaskDeleteView.as_view(), name='delete'),
	path('todo/update/<int:pk>/', ToDoTaskUpdateView.as_view(), name='update'),
	path('user/change/password/', changePasswordView, name='change_password'),
	path('task/completed', CompletedTasksView.as_view(), name='completed_task'),
	path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
	path('deactivate/profile/<int:pk>/', DeactivateProfileView.as_view(), name="deactivate"),
	path('edit/profile/<int:pk>/', EditProfileView.as_view(), name='edit_profile'),
]
