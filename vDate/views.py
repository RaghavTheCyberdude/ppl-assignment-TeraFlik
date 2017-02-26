from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from vDate.new import *
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
	handled = False
	giftNumForm = GetGiftNumberForm(prefix='auto')
	essentialGiftForm = EssentialGiftForm(prefix='essentialGift')
	luxuryGiftForm = LuxuryGiftForm(prefix='luxuryGift')
	utilityGiftForm = UtilityGiftForm(prefix='utilityGift')
	if request.method == 'POST':
		giftNumForm = GetGiftNumberForm(request.POST, prefix='auto')
		if giftNumForm.is_valid():
			handled = True
			giftType = giftNumForm.cleaned_data['giftType']
			number = giftNumForm.cleaned_data['number']
			for i in range(number):
				if giftType == '1':
					newEssentialGift()
				elif giftType == '2':
					newLuxuryGift()
				elif giftType == '3':
					newUtilityGift()
		if not handled:
			essentialGiftForm = EssentialGiftForm(request.POST, prefix='essentialGift')
			if essentialGiftForm.is_valid():
				handled = True
				essentialGiftForm.save()
		if not handled:
			luxuryGiftForm = LuxuryGiftForm(request.POST, prefix='luxuryGift')
			if luxuryGiftForm.is_valid():
				handled = True
				luxuryGiftForm.save()
		if not handled:	
			utilityGiftForm = UtilityGiftForm(request.POST, prefix='utilityGift')
			if utilityGiftForm.is_valid():
				utilityGiftForm.save()
				handled = True
	essentialGiftsList = EssentialGift.objects.all()
	luxuryGiftsList = LuxuryGift.objects.all()
	utilityGiftsList = UtilityGift.objects.all()
	return render(request, 'vDate/gifts.html',{
		'essentialGiftsList': essentialGiftsList,
		'luxuryGiftsList': luxuryGiftsList,
		'utilityGiftsList': utilityGiftsList,
		'essentialGiftForm': essentialGiftForm,
		'luxuryGiftForm': luxuryGiftForm,
		'utilityGiftForm': utilityGiftForm,
		'giftNumberForm': giftNumForm
		})

def relations(request):
	#breakupAll()
	numForm = GetNumberForm()
	if request.method == 'POST':
		numForm = GetNumberForm(request.POST)
		if numForm.is_valid():
			number = numForm.cleaned_data['number']
			girlCount = Girl.objects.filter(isCommitted=False).count()
			if number > girlCount:
				raise Exception("Not enough girls!")
			girlList = Girl.objects.filter(isCommitted=False)[:number]	
			for girl in girlList:
				findMatch(girl)

	relationsList = Relation.objects.all()
	return render(request, 'vDate/relations.html', {
		'relationsList': relationsList,
		'getNumberForm': numForm,
		})