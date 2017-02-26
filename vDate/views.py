from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from vDate.newrandom import *
# Create your views here.

def home(request):
	return render(request, 'vDate/base.html')

def boys(request):
	manual = False	
	boyForm = BoyForm(prefix='manual')
	if request.method == 'POST':
		boyForm = BoyForm(request.POST, prefix='manual')
		if boyForm.is_valid():
			boyForm.save()
			manual = True
		numForm = GetNumberForm(request.POST, prefix='auto')
		if not manual and numForm.is_valid():
			number = numForm.cleaned_data['number']
			if isinstance(number, int):
				for i in range(number):
					newRandomBoy()
			boyForm = BoyForm(prefix='manual')
	numForm = GetNumberForm(prefix='auto')
	boysList = Boy.objects.all().order_by('name')
	return render(request, 'vDate/boys.html', {'boysList': boysList, 'boyForm': boyForm, 'getNumberForm': numForm})

def girls(request):
	manual = False	
	girlForm = GirlForm(prefix='manual')
	if request.method == 'POST':
		girlForm = GirlForm(request.POST, prefix='manual')
		if girlForm.is_valid():
			girlForm.save()
			manual = True
		numForm = GetNumberForm(request.POST, prefix='auto')
		if not manual and numForm.is_valid():
			number = numForm.cleaned_data['number']
			for i in range(number):
				newRandomGirl()
			girlForm = GirlForm(prefix='manual')
	numForm = GetNumberForm(prefix='auto')
	girlsList = Girl.objects.all().order_by('name')
	return render(request, 'vDate/girls.html', {'girlsList': girlsList, 'girlForm': girlForm, 'getNumberForm': numForm})


def gifts(request):
	if request.method == 'POST':
		giftNumForm = GetGiftNumberForm(request.POST)
		if numForm.is_valid():
			giftType = numForm.cleaned_data['giftType']
			number = numForm.cleaned_data['number']
			for i in range(number):
				if giftType == 1:
					newEssentialGift()
				elif giftType == 2:
					newLuxuryGift()
				else:
					newUtilityGift()
	else:
		giftNumForm = GetGiftNumberForm(request.POST)
	essentialGiftslist = EssentialGift.objects.all()
	luxuryGiftslist = LuxuryGift.objects.all()
	utilityGiftslist = UtilityGift.objects.all()
	return render(request, 'vDate/gifts.html',{
		'essentialGiftslist': essentialGiftslist,
		'luxuryGiftslist': luxuryGiftslist,
		'utilityGiftslist': utilityGiftslist,
		'giftNumberForm': giftNumForm
		})

def newGift(request):
	handled = False
	if request.method == 'POST':
		essentialGiftForm = EssentialGiftForm(request.POST, prefix='essentialGift')
		if essentialGiftForm.is_valid():
			essentialGiftForm.save()
			handled = True
			return HttpResponseRedirect('vDate/gifts.html')
		luxuryGiftForm = LuxuryGiftForm(request.POST, prefix='luxuryGift')
		if not handled and luxuryGiftForm.is_valid():
			luxuryGiftForm.save()
			handled = True
			return HttpResponseRedirect('vDate/gifts.html')
		utilityGiftForm = UtilityGiftForm(request.POST, prefix='utilityGift')
		if not handled and utilityGiftForm.is_valid():
			utilityGiftForm.save()
			handled = True
			return HttpResponseRedirect('vDate/gifts.html')
	else:
		essentialGiftForm = EssentialGiftForm(prefix='essentialGift')
		luxuryGiftForm = LuxuryGiftForm(prefix='luxuryGift')
		utilityGiftForm = UtilityGiftForm(prefix='utilityGift')
	return render(request, 'vDate/gifts-new.html', {'essentialGiftForm': essentialGiftForm, 'luxuryGiftForm': luxuryGiftForm, 'utilityGiftForm': utilityGiftForm})

def relationships(request):
	relationsList = Relation.objects.all()
	return render(request, 'vDate/relationships.html', {'relationsList': relationsList})