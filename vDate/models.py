from django.db import models
from django import forms
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from datetime import datetime
from .choices import *
# Create your models here.

class Girl(models.Model):
	name = models.CharField(max_length=100)
	attractiveness = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(10)])
	intelligenceLevel = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(10)])
	isCommitted = models.BooleanField(default=False)
	maintenanceBudget = models.DecimalField(max_digits=13, decimal_places=2)
	datingCriteria = models.IntegerField(choices=datingCriteriaChoices)
	girlType = models.IntegerField(choices=committedGirlTypes, default=None)

	def __str__(self):
		return self.name
		
	def commit(self):
		self.isCommitted = True
		self.save()

	def leave(self):
		self.isCommitted = False
		self.save()
	
class Boy(models.Model):
	name = models.CharField(max_length=100)
	attractiveness = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(10)])
	intelligenceLevel = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(10)])
	isCommitted = models.BooleanField(default=False)
	budget = models.DecimalField(max_digits=13, decimal_places=2)
	attractionRequirement = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(10)])
	boyType = models.IntegerField(choices=committedBoyTypes, default=None)

	def __str__(self):
		return self.name
		
	def commit(self):
		self.isCommitted = True
		self.save()

	def leave(self):
		self.isCommitted = False
		self.save()

	def increaseBudget(self, increase):
		budget = budget + increase;


class EssentialGift(models.Model):
	price = models.DecimalField(max_digits=13, decimal_places=2)
	value = models.FloatField()

	def __str__(self):
		return "Price: " + str(self.price) + ", Value: " + str(self.value)

class LuxuryGift(models.Model):
	price = models.DecimalField(max_digits=13, decimal_places=2)
	value = models.FloatField()
	luxuryRating = models.FloatField()
	difficultyToObtain = models.FloatField()

	def __str__(self):
		return "Price: " + str(self.price) + ", Value: " + str(self.value)

class UtilityGift(models.Model):
	price = models.DecimalField(max_digits=13, decimal_places=2)
	value = models.FloatField()
	utilityValue = models.FloatField()
	utilityClass = models.IntegerField(choices=utilityClasses)

	def __str__(self):
		return "Price: " + str(self.price) + ", Value: " + str(self.value)

class Relation(models.Model):
	boy = models.ForeignKey(Boy, on_delete=models.CASCADE)
	girl = models.ForeignKey(Girl, on_delete=models.CASCADE)
	commitOn = models.DateTimeField(default=timezone.now)
	breakupOn = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		if self.breakupOn is None:
			return "%s is with %s" % (self.girl.name, self.boy.name)
		return "%s was with %s" % (self.girl.name, self.boy.name)

	def breakup(self):
		self.breakupOn = datetime.now()
		self.girl.leave()
		self.boy.leave()
		self.delete()

class Exchange(models.Model):
	relation = models.ForeignKey('vDate.Relation', related_name='exchanges')
	limit = models.Q(app_label='vDate', model='essentialgift') | models.Q(app_label='vDate', model='luxurygift') | models.Q(app_label='vDate', model = 'utilitygift')
	giftType = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=limit)
	giftID = models.PositiveIntegerField()
	gift = GenericForeignKey('giftType', 'giftID')
	exchangeTime = models.DateTimeField(default = timezone.now)

	def __str__(self):
		return "%s got gift worth %.2f from %s on %s" % (self.relation.girl.name, self.gift.value, self.relation.boy.name, self.exchangeTime)