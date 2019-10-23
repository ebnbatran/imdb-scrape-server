from django.db import models


class Movie(models.Model):
	title = models.CharField(max_length=100)
	url = models.CharField(max_length=100)
	year = models.CharField(max_length=100)
	rating = models.CharField(max_length=100)
	synopsis = models.CharField(max_length=300)
	image = models.CharField(max_length=100)


class ScrapeDate(models.Model):
	date = models.CharField(max_length=100)