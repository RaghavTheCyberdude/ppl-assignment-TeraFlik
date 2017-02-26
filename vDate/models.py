from django.db import models
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from datetime import datetime
from .constants import *
from decimal import *
import math
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
	compatibility = models.FloatField(default=0)
	happiness = models.FloatField(blank=True, null=True)

	def __str__(self):
		if self.breakupOn is None:
			return "%s + %s" % (self.girl.name, self.boy.name)
		return "%s was with %s" % (self.girl.name, self.boy.name)

	def breakup(self):
		self.breakupOn = datetime.now()
		self.girl.leave()
		self.boy.leave()
		self.delete()

	def findCompatibility(self):
		self.compatibility = (self.boy.budget - self.girl.maintenanceBudget) + Decimal(abs(self.boy.attractiveness - self.boy.attractiveness)) + Decimal(abs(self.boy.intelligenceLevel - self.girl.intelligenceLevel))
		return self.compatibility

	def findHappiness(self):
		total_cost = Decimal(0)
		gifts = self.exchanges.all()
		for gift in gifts:
			total_cost = total_cost + gift.getGift().price

		if self.girl.girlType == 1:
			for gift in gifts:
				if gift.giftType == 2:
					total_cost = total_cost + gift.getGift().price
			girlHappiness = math.log(total_cost - self.girl.maintenanceBudget)
		elif self.girl.girlType == 2:
			for gift in gifts:
				total_cost = total_cost + Decimal(gift.getGift().value)
			girlHappiness = total_cost - self.girl.maintenanceBudget
		elif self.girl.girlType == 3:
			girlHappiness = math.exp(total_cost - self.girl.maintenanceBudget)

		if self.boy.boyType == 1:
			boyHappiness = self.boy.budget - total_cost
		elif self.boy.boyType == 2:
			boyHappiness = girlHappiness
		elif self.boy.boyType == 3:
			boyHappiness = self.girl.intelligenceLevel

		self.happiness = float(boyHappiness) + float (girlHappiness)
		self.save()


class Exchange(models.Model):
	relation = models.ForeignKey('vDate.Relation', related_name='exchanges')
	essentialGift = models.ForeignKey('vDate.EssentialGift', blank=True, null=True)
	luxuryGift = models.ForeignKey('vDate.LuxuryGift', blank=True, null=True)
	utilityGift = models.ForeignKey('vDate.UtilityGift', blank=True, null=True)
	giftType = models.IntegerField(choices=giftTypes, default=None)
	exchangeTime = models.DateTimeField(default = timezone.now)

	def __str__(self):
		return "%s got gift worth %.2f from %s on %s" % (self.relation.girl.name, self.getGift().price, self.relation.boy.name, self.exchangeTime)

	def getGift(self):
		if self.giftType == 1:
			return self.essentialGift
		elif self.giftType == 2:
			return self.luxuryGift
		elif self.giftType == 3:
			return self.utilityGift
		else:
			return None