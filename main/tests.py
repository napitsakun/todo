from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import ToDoTask

User = get_user_model()

# Create your tests here.


# testing ToDoTask model
class ToDoTaskModelTest(TestCase):
	def create_user(self):
		user = User.objects.create(username='abc')
		return user

	def test_create_task(self):
		t = ToDoTask()
		t.task = 'def'
		t.created_by = self.create_user()
		t.save()

		self.assertEqual(t.id, 1)
		self.assertEqual(t.task, 'def')
		self.assertTrue(isinstance(t, ToDoTask))
		self.assertTrue(isinstance(t.created_by, User))
