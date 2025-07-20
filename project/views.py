from django.shortcuts import redirect, render

from django.http import HttpResponse
from . import models
from django.utils import timezone

from catboost import CatBoostClassifier
import numpy as np

# Load the model once (at module level, not inside the view)
claim_catboost_model = CatBoostClassifier()
claim_catboost_model.load_model('claim_catboost_model.cbm')
defect_catboost_model = CatBoostClassifier()
defect_catboost_model.load_model('defect_catboost_model.cbm')

def predict_claim_likelihood(request, product_id):
	try:
		client = models.session.get('client_id')
		product = models.Product.objects.get(id=product_id)
	except (models.Client.DoesNotExist, models.Product.DoesNotExist):
		return HttpResponse("Client or Product not found", status=404)

	# Example: Prepare features for prediction
	region = client.address.split(',')[-1].strip() if client.address else ""
	category = product.category
	warranty = product.warranty
	product_quality = 6
	previous_repairs = product.previous_repairs
	product_age_days = (timezone.now().date() - product.manufacture_date).days
	days_since_purchase = (timezone.now().date() - models.Order.objects.get(client=client, product=product).order_date).days
	total_brand_claims = models.Claim.objects.filter(product__brand=product.brand).count()
	brand_defect_rate = total_brand_claims / models.Order.objects.filter(product__brand=product.brand).count() if models.Order.objects.filter(product__brand=product.brand).count() > 0 else 0
	category_defect_rate = models.Claim.objects.filter(product__category=product.category).count() / models.Order.objects.filter(product__category=product.category).count() if models.Order.objects.filter(product__category=product.category).count() > 0 else 0
	client_total_purchases = models.Order.objects.filter(client=client).count()
	client_total_claims = models.Claim.objects.filter(client=client).count()
	client_claim_ratio = client_total_claims / client_total_purchases if client_total_purchases > 0 else 0
	time_to_first_claim = (timezone.now().date() - models.Claim.objects.filter(client=client, product=product).order_by('claim_date').first().claim_date).days if models.Claim.objects.filter(client=client, product=product).exists() else 0

	features = [
		region,
		category,
		warranty,
		product_quality,
		previous_repairs,
		product_age_days,
		days_since_purchase,
		total_brand_claims,
		brand_defect_rate,
		category_defect_rate,
		client_total_purchases,
		client_total_claims,
		client_claim_ratio,
		time_to_first_claim
	]
	features = np.array([features])

	proba = claim_catboost_model.predict_proba(features)[0][1]  # Probability of class 1 (claim)
	likelihood_percent = round(proba * 100, 2)
	return HttpResponse(f"Likelihood of warranty claim: {likelihood_percent}%")


def predict_product_defect(request, product_id):
	try:
		client = models.session.get('client_id')
		product = models.Product.objects.get(id=product_id)
	except models.Product.DoesNotExist:
		return HttpResponse("Product not found", status=404)

	# Example: Prepare features for prediction
	region = client.address.split(',')[-1].strip() if client.address else ""
	category = product.category
	warranty = product.warranty
	product_quality = 6  # Example value, adjust as needed
	previous_repairs = product.previous_repairs
	product_age_days = (timezone.now().date() - product.manufacture_date).days
	days_since_purchase = (timezone.now().date() - models.Order.objects.get(client=client, product=product).order_date).days
	total_brand_claims = models.Claim.objects.filter(product__brand=product.brand).count()
	brand_defect_rate = total_brand_claims / models.Order.objects.filter(product__brand=product.brand).count() if models.Order.objects.filter(product__brand=product.brand).count() > 0 else 0
	category_defect_rate = models.Claim.objects.filter(product__category=product.category).count() / models.Order.objects.filter(product__category=product.category).count() if models.Order.objects.filter(product__category=product.category).count() > 0 else 0
	client_total_purchases = models.Order.objects.filter(client=client).count()
	client_total_claims = models.Claim.objects.filter(client=client).count()
	price_to_warranty_ratio = product.price / product.warranty if product.warranty > 0 else 0
	repairs_per_year = product.previous_repairs / (product_age_days / 365) if product_age_days > 0 else 0

	features = [
		region,
		category,
		warranty,
		product_quality,
		previous_repairs,
		product_age_days,
		days_since_purchase,
		total_brand_claims,
		brand_defect_rate,
		category_defect_rate,
		client_total_purchases,
		client_total_claims,
		price_to_warranty_ratio,
		repairs_per_year
	]
	features = np.array([features])
	proba = defect_catboost_model.predict_proba(features)[0][1]  # Probability of defect
	defect_percent = round(proba * 100, 2)
	return HttpResponse(f"Likelihood of product defect: {defect_percent}%")

# Create your views here.
def index(request):
	return render(request, 'index.html')

def about(request):
	return render(request, 'about.html')

def contact(request):
	return render(request, 'contact.html')

def gallery(request):
	product_list = models.Product.objects.all()
	context = {"product_list": product_list}
	return render(request, 'gallery.html', context)

def contact(request):
	return render(request, 'contact.html')

def product(request, product_id):
	try:
		product = models.Product.objects.get(id=product_id)
	except models.Product.DoesNotExist:
		return HttpResponse("Product not found", status=404)
	context = {'product': product}
	return render(request, 'product.html', context)

def sign(request):
	action = request.POST.get('action')
	context = {'action': action}
	return render(request, 'sign.html', context)

def auth(request):
	if request.method == 'POST':
		if request.POST.get('action') == 'sign_in':
			email = request.POST.get('email')
			client = models.Client.objects.get(email=email)
			if client:
				request.session['client_id'] = client.id
				return redirect('dashboard')
			else:
				return HttpResponse("Client not found", status=404)
		elif request.POST.get('action') == 'sign_up':
			phone= request.POST.get('phone')
			address = request.POST.get('address')
			name= request.POST.get('name')
			email = request.POST.get('email')
			client = models.Client(name=name, email=email, phone=phone, address=address)
			client.save()
			request.session['client_id'] = client.id
			return redirect('dashboard')
	else:
		return HttpResponse("Method not allowed", status=405)


def dashboard(request):
	client_id = request.session.get('client_id')
	if not client_id:
		return redirect('sign')
	try:
		client = models.Client.objects.get(id=client_id)
	except models.Client.DoesNotExist:
		return redirect('sign')
	return render(request, 'dashboard.html')
	
def purchase(request):
	if request.method == 'POST':
		product_id = request.POST.get('product_id')

		try:
			product = models.Product.objects.get(id=product_id)
			client = models.Client.objects.get(id=request.session['client_id'])
		except (models.Product.DoesNotExist, models.Client.DoesNotExist):
			return HttpResponse("Product or Client not found", status=404)

		order = models.Order(client=client, product=product, order_date=timezone.now())
		order.save()
		
		return HttpResponse(f"Order placed successfully for {product.name}!")
	else:
		return HttpResponse("Method not allowed", status=405)