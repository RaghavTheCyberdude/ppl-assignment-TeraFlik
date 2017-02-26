from .models import *
import random
from datetime import datetime
from vDate.names.name import get_full_name

attractionMin = 1
attractionMode = 7
attractionMax = 10

intelligenceMin = 1
intelligenceMode = 7
intelligenceMax = 10

maintenanceBudgetMin = 500
maintenanceBudgetMode = 5000
maintenanceBudgetMax = 50000

budgetMin = 1000
budgetMode = 5000
budgetMax = 100000

giftMin = 20
giftMode = 200
giftMax = 5000

luxuryGiftMin = 2500
luxuryGiftMode = 5000
luxuryGiftMax = 50000

ratingMin = 1
ratingMax = 5
ratingMode = 2

def newRandomBoy():
	name = get_full_name('male')
	attractiveness = random.triangular(attractionMin, attractionMax, attractionMode)
	intelligenceLevel = random.triangular(intelligenceMin, intelligenceMax, intelligenceMode)
	budget = random.triangular(budgetMin, budgetMax, budgetMode)
	attractionRequirement = random.triangular(attractionMin, attractionMax, attractionMode)
	boyType = random.randint(1,3)
	boy = Boy.objects.create(name=name, attractiveness=attractiveness, intelligenceLevel=intelligenceLevel, budget=budget, attractionRequirement=attractionRequirement, boyType=boyType)
	return boy

def newRandomGirl():
	name = get_full_name('female')
	attractiveness = random.triangular(attractionMin, attractionMax, attractionMode)
	intelligenceLevel = random.triangular(intelligenceMin, intelligenceMax, intelligenceMode)
	maintenanceBudget = random.triangular(maintenanceBudgetMin, maintenanceBudgetMax, maintenanceBudgetMode)
	datingCriteria = random.randint(1,3)
	girlType = random.randint(1,3)
	Girl.objects.create(name=name, attractiveness=attractiveness, intelligenceLevel=intelligenceLevel, maintenanceBudget=maintenanceBudget, datingCriteria=datingCriteria, girlType=girlType)

def newEssentialGift():
	price =  random.triangular(giftMin, giftMax, giftMode)
	value = price
	EssentialGift.objects.create(price=price, value=value)

def newLuxuryGift():
	price =  random.triangular(luxuryGiftMin, luxuryGiftMax, luxuryGiftMode)
	rating = random.triangular(ratingMin, ratingMax, ratingMode)
	difficultyToObtain = random.triangular(ratingMin, ratingMax, ratingMode)
	value = price * rating
	LuxuryGift.objects.create(price=price, value=value, luxuryRating=rating, difficultyToObtain=difficultyToObtain)

def newUtilityGift():
	price =  random.triangular(giftMin, giftMax, giftMode)
	utilityValue = random.triangular(ratingMin, ratingMax/2, ratingMode/2)
	utilityClass = random.randint(1,5)
	value = price * utilityValue
	UtilityGift.objects.create(price=price, value=value, utilityValue=utilityValue, utilityClass=utilityClass)

def findMatch(girl):
	if girl.isCommitted:
		return None
	boyList = Boy.objects.filter(isCommitted=False)
	if girl.datingCriteria == 1:
		boyList.order_by('attractiveness')
	if girl.datingCriteria == 2:
		boyList.order_by('budget')
	if girl.datingCriteria == 3:
		boyList.order_by('intelligence')
	for boy in boyList:
		if boy.isCommitted:
			continue
		if boy.budget >= girl.maintenanceBudget and girl.attractiveness >= boy.attractionRequirement:
			boy.commit()
			girl.commit()
			newRelation = Relation(boy=boy, girl=girl, commitOn=datetime.now())
			newRelation.findCompatibility()
			newRelation.save(force_insert=True)
			return newRelation
	return None

def breakupAll():
	for relation in Relation.objects.all():
		relation.breakup()