from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, Subscription


class SubscriptionAPITests(APITestCase):

    def test_unauthenticated_user_cannot_access_subscriptions(self):
        url = reverse('subscription-list-create')

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
    def test_authenticated_user_can_access_subscriptions(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()

        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )

        self.client.force_authenticate(user=user)

        url = reverse('subscription-list-create')

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
    def test_authenticated_user_can_create_subscription(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()

        user = User.objects.create_user(
            username='creator',
            email='creator@example.com',
            password='testpassword123'
        )

        category = Category.objects.create(
            name='Entertainment',
            slug='entertainment'
        )

        self.client.force_authenticate(user=user)

        url = reverse('subscription-list-create')

        data = {
            'service_name': 'Spotify Premium',
            'category': category.id,
            'price': '199.00',
            'billing_cycle': 'MONTHLY',
            'currency': 'INR',
            'start_date': '2026-11-20',
            'renewal_date': '2026-12-20',
            'payment_method': 'UPI',
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        subscription = Subscription.objects.get(
            service_name='Spotify Premium'
        )

        self.assertEqual(subscription.user, user)

    def test_user_cannot_access_another_users_subscription(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()

        user_a = User.objects.create_user(
            username='user_a',
            email='usera@example.com',
            password='testpassword123'
        )

        user_b = User.objects.create_user(
            username='user_b',
            email='userb@example.com',
            password='testpassword123'
        )

        category = Category.objects.create(
            name='Entertainment',
            slug='entertainment'
        )

        subscription = Subscription.objects.create(
            user=user_a,
            category=category,
            service_name='Netflix',
            price='199.00',
            billing_cycle='MONTHLY',
            currency='INR',
            start_date='2026-11-20',
            renewal_date='2026-12-20',
            payment_method='UPI'
        )

        self.client.force_authenticate(user=user_b)

        url = reverse(
            'subscription-detail',
            kwargs={'pk': subscription.id}
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
    def test_user_cannot_update_another_users_subscription(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()

        user_a = User.objects.create_user(username='user_a')
        user_b = User.objects.create_user(username='user_b')

        category = Category.objects.create(
            name='Entertainment',
            slug='entertainment'
        )

        subscription = Subscription.objects.create(
            user=user_a,
            category=category,
            service_name='Netflix',
            price='199.00',
            billing_cycle='MONTHLY',
            currency='INR',
            start_date='2026-11-20',
            renewal_date='2026-12-20',
            payment_method='UPI'
        )

        self.client.force_authenticate(user=user_b)

        url = reverse('subscription-detail', kwargs={'pk': subscription.id})

        response = self.client.patch(
            url,
            {'price': '299.00'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_delete_another_users_subscription(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()

        user_a = User.objects.create_user(username='user_a')
        user_b = User.objects.create_user(username='user_b')

        category = Category.objects.create(
            name='Entertainment',
            slug='entertainment'
        )

        subscription = Subscription.objects.create(
            user=user_a,
            category=category,
            service_name='Netflix',
            price='199.00',
            billing_cycle='MONTHLY',
            currency='INR',
            start_date='2026-11-20',
            renewal_date='2026-12-20',
            payment_method='UPI'
        )

        self.client.force_authenticate(user=user_b)

        url = reverse('subscription-detail', kwargs={'pk': subscription.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(
            Subscription.objects.filter(pk=subscription.id).exists()
        )