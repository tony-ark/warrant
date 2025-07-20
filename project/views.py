from django.shortcuts import render

from django.http import HttpResponse
from . import models
from django.utils import timezone

from catboost import CatBoostClassifier
import numpy as np

# Load the model once (at module level, not inside the view)
catboost_model = CatBoostClassifier()
catboost_model.load_model('catboost_model.cbm')

def predict_claim_likelihood(request, product_id):
    try:
        client = models.session.get('client_id')
        product = models.Product.objects.get(id=product_id)
    except (models.Client.DoesNotExist, models.Product.DoesNotExist):
        return HttpResponse("Client or Product not found", status=404)

    # Example: Prepare features for prediction
    # You must match the features used during training!
    client_purchase_count = models.Order.objects.filter(client_id=client.id).count()
    client_claim_count = models.Claim.objects.filter(client_id=client.id).count()
    product_info_length = len(product.info)
    order_date = timezone.now()  # Assuming you want to use the current date
    days_since_purchase = (timezone.now() - order_date).days
    is_repeat_purchase = models.Order.objects.filter(client_id=client.id, product_id=product.id).exists()
    client_product_claim_count = models.Claim.objects.filter(client_id=client.id, product_id=product.id).count()
    client_product_purchase_count = models.Order.objects.filter(client_id=client.id, product_id=product.id).count()
    has_claim = models.Claim.objects.filter(client_id=client.id, product_id=product.id).exists()
    
    features = [
        product.price,
        product.warranty,
        client.address,  # Assuming address is a string, you might need to encode it
		product.brand,
		client_purchase_count,
		client_claim_count,
		product_info_length,
		order_date.year,  # Example: using year as a feature
		days_since_purchase,
		is_repeat_purchase,
		client_product_claim_count,
		client_product_purchase_count,
		has_claim
    ]
    features = np.array([features])

    proba = catboost_model.predict_proba(features)[0][1]  # Probability of class 1 (claim)
    likelihood_percent = round(proba * 100, 2)
    return HttpResponse(f"Likelihood of warranty claim: {likelihood_percent}%")

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
				return HttpResponse(f"Welcome back, {client.name}!")
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
			return HttpResponse(f"Client {client.name} created successfully!")
	else:
		return HttpResponse("Method not allowed", status=405)
	
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