from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
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
	essentialGiftsList = EssentialGift.objects.all().order_by('price')
	luxuryGiftsList = LuxuryGift.objects.all().order_by('price')
	utilityGiftsList = UtilityGift.objects.all().order_by('price')
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
				messages.error(request, "Not enough single girls!")
			else:
				girlList = Girl.objects.filter(isCommitted=False)[:number]	
				for girl in girlList:
					findMatch(girl)
	else:
		numForm = GetNumberForm()
	relationsList = Relation.objects.all()
	return render(request, 'vDate/relations.html', {
		'relationsList': relationsList,
		'getNumberForm': numForm,
		})

def deleteEntries(request):
	if request.method == 'POST':
		if request.POST.get('type') == 'boys':
			Boy.objects.all().delete()
			return HttpResponseRedirect(reverse('boys'))
		elif request.POST.get('type') == 'girls':
			Girl.objects.all().delete()
			return HttpResponseRedirect(reverse('girls'))
		elif request.POST.get('type') == 'gifts':
			EssentialGift.objects.all().delete()
			LuxuryGift.objects.all().delete()
			UtilityGift.objects.all().delete()
			return HttpResponseRedirect(reverse('gifts'))
		elif request.POST.get('type') == 'relations':
			for relation in Relation.objects.all():
				relation.breakup()
			return HttpResponseRedirect(reverse('relations'))
	return HttpResponseRedirect(reverse('home'))