from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import *
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from .models import *
from .forms import *

User = get_user_model()

# Create your views here.


class LogoutView(View):
	def get(self, request):
		logout(request)
		return redirect('login')


class LoginView(TemplateView):
	template_name = 'login.html'

	def get(self, request):
		if request.user.is_authenticated:
			return redirect('index')
		return render(request, self.template_name)

	def post(self, request):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)

		if User.objects.filter(username=username).exists():
			if user:
				if user.is_active:
					login(request, user)
					return redirect('index')
				else:
					messages.add_message(request, messages.INFO, 'Profile is deactivated')
			else:
				messages.add_message(request, messages.INFO, 'Wrong Password')

		else:
			messages.add_message(request, messages.INFO, 'User does not exist')

		return render(request, self.template_name)



class RegisterView(TemplateView):
	template_name = 'register.html'

	def get(self, request):
		if request.user.is_authenticated:
			return redirect('index')
		return render(request, self.template_name)

	def post(self, request):
		username = request.POST['username']
		email = request.POST['email']
		first_name = request.POST['fname']
		last_name = request.POST['lname']
		date_of_birth = request.POST['dob']
		password1 = request.POST['password1']
		password2 = request.POST['password2']

		if password1 == password2:
			user = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
			user.set_password(password1)
			user.save()

			user = User.objects.get(username=username)

			detail = RegisteredUser.objects.create(user=user, date_of_birth=date_of_birth)
			detail.save()

			return redirect('login')

		else:
			messages.add_message(request, messages.INFO, 'Passwords did not match')

		return render(request, self.template_name)


class ToDoTaskView(LoginRequiredMixin, ListView):
	template_name = 'index.html'
	model = ToDoTask
	paginate_by = 3
	context_object_name = 'tasks'

	def get_queryset(self, *args, **kwargs):
		return self.model.objects.filter(created_by=self.request.user, is_active=True).order_by('-updated_at')


class ToDoTaskCreateView(LoginRequiredMixin, CreateView):
	template_name = 'index.html'
	model = ToDoTask

	def post(self, request):
		task = request.POST['todo']
		todo = self.model.objects.create(created_by=self.request.user, task=task)
		return redirect('index')


class ToDoTaskDeleteView(LoginRequiredMixin, TemplateView):
	model = ToDoTask
	template_name = 'task_delete_confirm.html'

	def post(self, request, pk):
		user = self.model.objects.get(pk=pk).created_by
		if user != self.request.user:
			raise PermissionDenied

		# try:
		task = self.model.objects.get(pk=pk)
		task.is_active = False
		task.save()
		return redirect('index')
			# return JsonResponse({'success': True})
		# except:
			# return JsonResponse({'success': False})


class CompletedTasksView(LoginRequiredMixin, ListView):
	template_name = 'index.html'
	model = ToDoTask
	context_object_name = 'tasks'
	paginate_by = 3

	def get_queryset(self):
		return self.model.objects.filter(created_by=self.request.user, is_active=False).order_by('-updated_at')


class ToDoTaskUpdateView(LoginRequiredMixin, UpdateView):
	model = ToDoTask
	form_class = AddTodoForm
	template_name = 'todotask_update.html'
	success_url = reverse_lazy('index')

	def get(self, *args, **kwargs):
		user = self.model.objects.get(pk=kwargs.get('pk')).created_by
		if user != self.request.user:
			raise PermissionDenied
		return super().get(*args, **kwargs)

	def form_valid(self, form):
		form.save()
		return super().form_valid(form)


class ProfileView(LoginRequiredMixin, DetailView):
	template_name = 'profile.html'
	model = User

	def get(self, request, pk):
		if self.model.objects.get(pk=pk) != request.user:
			raise PermissionDenied
		return super().get(pk)

	def get_context_data(self, *args, **kwargs):
		context = super(ProfileView, self).get_context_data(*args, **kwargs)
		context['detail'] = RegisteredUser.objects.get(user=self.request.user)
		return context


class DeactivateProfileView(LoginRequiredMixin, DetailView):
	model = User
	template_name = 'confirm.html'

	def post(self, request, pk):
		user = self.model.objects.get(pk=pk)
		user.is_active = False
		user.save()
		return redirect('login')
		# return JsonResponse({'success': True})


class EditProfileView(LoginRequiredMixin, UpdateView):
	model = User
	form_class = ProfileUpdateForm
	template_name = 'profile_update.html'

	def get_success_url(self, *args, **kwargs):
		return reverse_lazy('profile', kwargs = {'pk': self.object.id })

	def get(self, *args, **kwargs):
		form_dob = ProfileDetailForm()
		user = self.model.objects.get(pk=kwargs.get('pk'))
		if user != self.request.user:
			raise PermissionDenied
		return super().get(*args, **kwargs)


@login_required
def changePasswordView(request):
	if request.method == 'POST':
		form = PasswordChangeFormEdit(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)

			return HttpResponse('password change success')
	else:
		form = PasswordChangeFormEdit(request.user)

	return render(request, 'change_password.html', {'form': form })
