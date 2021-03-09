from django.db import models
import random
import string
def random_key():
	all_digits = list(string.digits)
	random_key = ""
	return random_key.join(random.sample(all_digits, 10))

class Show(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return self.name

class Role(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return self.name


class Quote(models.Model):
	key = models.CharField(default=random_key,max_length=10)
	quote = models.CharField(max_length=500, unique=True)
	show = models.ForeignKey(Show, on_delete=models.DO_NOTHING)
	role = models.ForeignKey(Role, on_delete=models.DO_NOTHING, related_name="role")

	def __str__(self):
		return str(self.key)
		