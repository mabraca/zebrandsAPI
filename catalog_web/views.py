from django.shortcuts import render
from django.views.generic import View
import requests





class ProductListCreateAPIView(View):
    def get(self, request):
        # Call API REST to obtain product list
        response = requests.get('http://localhost:8000/api/product/list/')
        products = response.json()
        return render(request, 'product_list.html', {'products': products})


class ProductDetailAPIView(View):
    def get(self, request, pk):
        # Call API REST to obtain detail from a product
        url = f'http://localhost:8000/api/product/{pk}/'
        response = requests.get(url)
        product = response.json()
        return render(request, 'product_detail.html', {'product': product})
