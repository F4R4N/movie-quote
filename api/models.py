from django.db import models
import random
import string
from django.utils.text import slugify


def random_key():
	all_digits = list(string.digits)
	random_key = ""
	return random_key.join(random.sample(all_digits, 10))


class RoleAndShowBase(models.Model):
	name = models.CharField(max_length=100, unique=True)
	slug = models.SlugField(max_length=100)

	class Meta:
		abstract = True


class Show(RoleAndShowBase):
	def save(self, *args, **kwargs):  # Slugify
		self.slug = slugify(self.name)
		super(Show, self).save(*args, **kwargs)

	def __str__(self):
		return self.name


class Role(RoleAndShowBase):

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Role, self).save(*args, **kwargs)

	def __str__(self):
		return self.name


class QuoteBaseClass(models.Model):
	key = models.CharField(default=random_key, max_length=10, unique=True)
	quote = models.CharField(max_length=500, unique=True)

	contain_adult_lang = models.BooleanField(
		verbose_name="Contain adult language", default=False)

	class Meta:
		abstract = True


class Quote(QuoteBaseClass):
	show = models.ForeignKey(
		Show, on_delete=models.DO_NOTHING)
	role = models.ForeignKey(
		Role, on_delete=models.DO_NOTHING)

	def __str__(self):
		return str(self.key)


class Ticket(QuoteBaseClass):
	SUGGESTION_TYPE = (
		("edit", "Edit"),
		("add", "Add"),
	)
	sug_type = models.CharField(max_length=4, choices=SUGGESTION_TYPE)
	show = models.CharField(max_length=100)
	role = models.CharField(max_length=100)

	def __str__(self) -> str:
		return str(self.key)
