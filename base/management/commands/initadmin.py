"""Script to create superuser"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

import os


class Command(BaseCommand):
	"""Defines initadmin command that creates admin account"""

	def handle(self, *args, **kwargs):
		"""
		Creates an admin account if no user is present
		"""
		user = get_user_model()
		if user.objects.count() == 0:
			admin = user.objects.create_superuser(
				username=os.environ["SUPERUSER_USERNAME"],
				email=os.environ["SUPERUSER_EMAIL"],
				password=os.environ["SUPERUSER_PASSWORD"]
			)

			self.stdout.write(
				self.style.SUCCESS('Geez Rick! You just created a superuser admin account')
			)
		else:
			error = 'Morty! You already hava some accounts ' \
					'You can create superuser using initadmin only during first migration'
			self.stdout.write(self.style.ERROR('Error:- ' + str(error)))
