from django.db import models
from django import forms
from .choices import *
# Create your models here.

class Girl(models.Model):
	name = models.CharField(max_length=100)
	attractivenes = models.FloatField()
	maintenanceBudget = models.DecimalField(max_digits=13, decimal_places=2)
	intelligenceLevel = models.FloatField()
	datingCriteria = models.IntegerField(choices=datingCriteriaChoices)
	isCommitted = models.BooleanField(default=False)
	girlType = models.IntegerField(choices=committedGirlTypes, default=None)

	def __str__(self):
		return self.name
	
class Boy(models.Model):
	name = models.CharField(max_length=100)
	attractivenes = models.FloatField()
	budget = models.DecimalField(max_digits=13, decimal_places=2)
	intelligenceLevel = models.FloatField()
	attractionRequirement = models.FloatField()
	isCommitted = models.BooleanField(default=False)
	boyType = models.IntegerField(choices=committedBoyTypes, default=None)
	
	def __str__(self):
		return self.name
	
	def increaseBudget(self, increase):
		budget = budget + increase;

class Gift(models.Model):
	price = models.DecimalField(max_digits=13, decimal_places=2)
	value = models.FloatField()

	def __str__(self):
		return self.price

class EssentialGift(Gift):
	def blankFn():
		return None

class LuxuryGift(Gift):
	luxuryRating = models.FloatField()
	difficultyToObtain = models.FloatField()

class UtilityGift(Gift):
	utilityValue = models.FloatField()
	utilityClass = models.IntegerField(choices=utilityClasses)

class Relation(models.Model):
	girl = models.OneToOneField(Boy, on_delete=models.CASCADE)
	boy = models.OneToOneField(Girl, on_delete=models.CASCADE)

	def __str__(self):
		return "%s with %s" % (self.girl.name, self.boy.name)

	def addRelation(boy, girl):
		if(boy.budget < girl.maintenanceBudget):
			return "Error!"

class Exchanges(models.Model):
	relation = models.ForeignKey('vDate.Relation', related_name='relation')
	gift = models.ForeignKey('vDate.Gift', related_name='gift')

	def __str__(self):
		return "%s got gift worth %f from %s" % (self.relation.girl.name, self.gift.value, self.relation.boy.name)