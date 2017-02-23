from django.db import models
from django import forms
from .choices import *
# Create your models here.

class Person(models.Model):
	"""The Basic Person Model/Class for representing both Boys and Girls"""
	name = models.CharField(max_length=100)
	attractivenes = models.FloatField()
	intelligenceLevel = models.FloatField()
	isCommitted = models.BooleanField(default=False)

	def __str__(self):
		return self.name
		
	def commit(self):
		self.isCommitted = True
		self.save()

class Girl(Person):
	maintenanceBudget = models.DecimalField(max_digits=13, decimal_places=2)
	datingCriteria = models.IntegerField(choices=datingCriteriaChoices)
	girlType = models.IntegerField(choices=committedGirlTypes, default=None)
	
class Boy(Person):
	budget = models.DecimalField(max_digits=13, decimal_places=2)
	attractionRequirement = models.FloatField()
	boyType = models.IntegerField(choices=committedBoyTypes, default=None)

	def increaseBudget(self, increase):
		budget = budget + increase;

class Gift(models.Model):
	price = models.DecimalField(max_digits=13, decimal_places=2)
	value = models.FloatField()

	def __str__(self):
		return self.value

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
		return "%s is with %s" % (self.girl.name, self.boy.name)

	def addRelation(boy, girl):
		if boy.budget >= girl.maintenanceBudget:
			raise Exception("Boy's budget not enough!")
		elif girl.attractivenes >= boy.attractionRequirement:
			raise Exception("Girl not attractive enough!")
		elif girl.isCommitted:
			raise Exception("Girl already committed!")
		elif boy.isCommitted:
			raise Exception("Boy already committed!")
		else:
			boy.commit()
			girl.commit()
			self.save()
			
class Exchanges(models.Model):
	relation = models.ForeignKey('vDate.Relation', related_name='relation')
	gift = models.ForeignKey('vDate.Gift', related_name='gift')

	def __str__(self):
		return "%s got gift worth %f from %s" % (self.relation.girl.name, self.gift.value, self.relation.boy.name)