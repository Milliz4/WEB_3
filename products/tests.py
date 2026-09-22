import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from products.models import Category, Product, Order, OrderItem, Review


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
class TestCategoryViewSet:

    def test_list_categories(self, client):
        category = baker.make('products.Category', _quantity=10)
        response = client.get('/api/categories/')
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 10

    def test_create_category(self, client):
        data = {'name': 'Ноутбуки'}
        response = client.post('/api/categories/', data)
        assert response.status_code == 201

    def test_update_category(self, client):
        category = baker.make('products.Category')
        data = {'name': 'Смартфоны'}
        response = client.put(f'/api/categories/{category.id}/', data)
        assert response.status_code == 200
        category.refresh_from_db()
        assert category.name == data['name']

    def test_delete_category(self, client):
        categories = baker.make('products.Category', _quantity=10)
        response = client.delete(f'/api/categories/{categories[0].id}/')
        assert response.status_code == 204
        assert Category.objects.count() == 9
        get_response = client.get('/api/categories/')
        assert categories[0].id not in [i['id'] for i in get_response.data]


@pytest.mark.django_db
class TestProductViewSet:

    def test_list_products(self, client):
        product = baker.make('products.Product', _quantity=10)
        response = client.get('/api/products/')
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 10

    def test_create_product(self, client):
        category = baker.make('products.Category')
        data = {
            'name': 'iPhone',
            'description': 'Смартфон',
            'price': '999.99',
            'stock': 10,
            'category': category.id
        }
        response = client.post('/api/products/', data)
        assert response.status_code == 201

    def test_update_product(self, client):
        product = baker.make('products.Product')
        data = {
            'name': 'Samsung',
            'description': 'Телефон',
            'price': '799.99',
            'stock': 5,
            'category': product.category.id
        }
        response = client.put(f'/api/products/{product.id}/', data)
        assert response.status_code == 200
        product.refresh_from_db()
        assert product.name == data['name']

    def test_delete_product(self, client):
        products = baker.make('products.Product', _quantity=10)
        response = client.delete(f'/api/products/{products[0].id}/')
        assert response.status_code == 204
        assert Product.objects.count() == 9
        get_response = client.get('/api/products/')
        assert products[0].id not in [i['id'] for i in get_response.data]


@pytest.mark.django_db
class TestOrderViewSet:

    def test_list_orders(self, client):
        order = baker.make('products.Order', _quantity=10)
        response = client.get('/api/orders/')
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 10

    def test_create_order(self, client):
        data = {'status': 'Новый', 'total': '1000.00'}
        response = client.post('/api/orders/', data)
        assert response.status_code == 201

    def test_update_order(self, client):
        order = baker.make('products.Order')
        data = {'status': 'Доставлен', 'total': '1500.00'}
        response = client.put(f'/api/orders/{order.id}/', data)
        assert response.status_code == 200
        order.refresh_from_db()
        assert order.status == data['status']

    def test_delete_order(self, client):
        orders = baker.make('products.Order', _quantity=10)
        response = client.delete(f'/api/orders/{orders[0].id}/')
        assert response.status_code == 204
        assert Order.objects.count() == 9
        get_response = client.get('/api/orders/')
        assert orders[0].id not in [i['id'] for i in get_response.data]


@pytest.mark.django_db
class TestOrderItemViewSet:

    def test_list_order_items(self, client):
        order_item = baker.make('products.OrderItem', _quantity=10)
        response = client.get('/api/order-items/')
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 10

    def test_create_order_item(self, client):
        order = baker.make('products.Order')
        product = baker.make('products.Product')
        data = {
            'order': order.id,
            'product': product.id,
            'quantity': 2,
            'price': '599.99'
        }
        response = client.post('/api/order-items/', data)
        assert response.status_code == 201

    def test_update_order_item(self, client):
        order_item = baker.make('products.OrderItem')
        data = {
            'order': order_item.order.id,
            'product': order_item.product.id,
            'quantity': 5,
            'price': '299.99'
        }
        response = client.put(f'/api/order-items/{order_item.id}/', data)
        assert response.status_code == 200
        order_item.refresh_from_db()
        assert order_item.quantity == data['quantity']

    def test_delete_order_item(self, client):
        order_items = baker.make('products.OrderItem', _quantity=10)
        response = client.delete(f'/api/order-items/{order_items[0].id}/')
        assert response.status_code == 204
        assert OrderItem.objects.count() == 9
        get_response = client.get('/api/order-items/')
        assert order_items[0].id not in [i['id'] for i in get_response.data]


@pytest.mark.django_db
class TestReviewViewSet:

    def test_list_reviews(self, client):
        review = baker.make('products.Review', _quantity=10)
        response = client.get('/api/reviews/')
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 10

    def test_create_review(self, client):
        category = baker.make('products.Category')
        product = baker.make('products.Product', category=category)
        data = {
            'product': product.id,
            'rating': 5,
            'text': 'Отличный товар!'
        }
        response = client.post('/api/reviews/', data, format='json')
        assert response.status_code == 201

    def test_update_review(self, client):
        review = baker.make('products.Review')
        data = {
            'product': review.product.id,
            'rating': 4,
            'text': 'Хороший товар'
        }
        response = client.put(f'/api/reviews/{review.id}/', data)
        assert response.status_code == 200
        review.refresh_from_db()
        assert review.rating == data['rating']

    def test_delete_review(self, client):
        reviews = baker.make('products.Review', _quantity=10)
        response = client.delete(f'/api/reviews/{reviews[0].id}/')
        assert response.status_code == 204
        assert Review.objects.count() == 9
        get_response = client.get('/api/reviews/')
        assert reviews[0].id not in [i['id'] for i in get_response.data]