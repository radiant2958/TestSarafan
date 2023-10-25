from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Category, Product, Cart, CartItem, SubCategory

class CartTests(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category', image='path/to/test/image.jpg')
        self.subcategory = SubCategory.objects.create(name='Test Subcategory', slug='test-subcategory', category=self.category, image='path/to/test/image.jpg')
        self.product = Product.objects.create(name='Test Product', slug='test-product', price=100, subcategory=self.subcategory, image_small='path/to/test/small_image.jpg', image_medium='path/to/test/medium_image.jpg', image_large='path/to/test/large_image.jpg')
       
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.cart = Cart.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_add_product_to_cart(self):
        url = reverse('cartitem-list')  
        data = {'product': self.product.id, 'quantity': 1, 'cart': self.cart.id}
        response = self.client.post(url, data, format='json')
        print(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)

    def test_update_product_quantity_in_cart(self):
        cart_item = CartItem.objects.create(cart=self.user.cart, product=self.product, quantity=1)
        url = reverse('cartitem-detail', args=[cart_item.id])
        data = {'quantity': 2}
        response = self.client.patch(url, data, format='json')  
        print(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 2)

    def test_delete_product_from_cart(self):
        cart_item = CartItem.objects.create(cart=self.user.cart, product=self.product, quantity=1)
        url = reverse('cartitem-detail', args=[cart_item.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CartItem.objects.count(), 0)

