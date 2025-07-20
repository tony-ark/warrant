from django.urls import path

from.import views
urlpatterns = [
    path('',views.index, name='index'),
    path('about/',views.about, name='about'),
    path('gallery/',views.gallery, name='gallery'),  
    path('contact/',views.contact, name='contact'),
    path('sign/',views.sign, name='sign'),
    path('auth/', views.auth, name='auth'),
    path('product/<int:product_id>/', views.product, name='product'),
    path('purchase/', views.purchase, name='purchase'),
    path('predict_claim/<int:product_id>/', views.predict_claim_likelihood, name='predict_claim'),
]