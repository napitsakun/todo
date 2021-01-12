from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# Create your models here.


class RegisteredUser(models.Model):
	user = models.OneToOneField(to=User, on_delete=models.CASCADE)
	date_of_birth = models.DateField()

	def __str__(self):
		return self.user.username


class ToDoTask(models.Model):
	created_at = models.DateTimeField(editable=False)
	updated_at = models.DateTimeField(editable=False)
	created_by = models.ForeignKey(to=User, on_delete=models.CASCADE)
	task = models.TextField()
	is_active = models.BooleanField(default=True)

	def save(self, *args, **kwargs):
		if not self.created_at:
			self.created_at = timezone.now()
		self.updated_at = timezone.now()
		return super(ToDoTask, self).save(*args, **kwargs)
