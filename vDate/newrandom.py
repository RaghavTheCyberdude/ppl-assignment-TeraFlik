from .models import *
import random
from vDate.names.name import get_full_name

attractionMin = 1
attractionMode = 7
attractionMax = 10

intelligenceMin = 1
intelligenceMode = 7
intelligenceMax = 10

maintenanceBudgetMin = 500
maintenanceBudgetMode = 2000
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
ratingMax = 10
ratingMode = 5

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
	EssentialGift.objects.create(price=price, value=price)

def newLuxuryGift():
	price =  random.triangular(giftMin, giftMax, giftMode)
	rating = random.triangular(ratingMin, ratingMax, ratingMode)
	difficultyToObtain = random.triangular(ratingMin, ratingMax, ratingMode)
	value = price * rating
	EssentialGift.objects.create(price=price, value=price, luxuryRating=luxury, difficultyToObtain=difficultyToObtain)

def newUtilityGift():
	price =  random.triangular(giftMin, giftMax, giftMode)
	utilityRating = random.triangular(ratingMin, ratingMax/2, ratingMode/2)
	utilityClass = random.randint(1,5)
	value = price * rating
	EssentialGift.objects.create(price=price, value=price, luxuryRating=rating, utilityClass=utilityClass)

