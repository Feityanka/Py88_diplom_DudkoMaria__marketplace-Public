from django.test import TestCase

from django.contrib.auth import get_user_model

User = get_user_model()


class TestRegistration(TestCase):
    def setUp(self) -> None:
        self.user_first = {
            'email': 'alex@mail.ru',
            'password': 'Hffosl'
        }
        self.user_second = {
            'email': 'dima@mail.ru',
            'password': 'HFPHSDFbpdf'
        }
        self.article = {
            'title': 'Some Title',
            'content': 'This is good content'
        }

    def test_registration_user(self):
        self.client.post('http://localhost:8000/sign-up/', data=self.user_first)
        self.client.post('http://localhost:8000/sign-up/', data=self.user_second)

        self.client.login(email=self.user_first['email'], password=self.user_first['password'])
        self.client.post('https://localhost:8000/create-article', self.article)

        art = Article.objects.first()
        response = self.client.post('https://localhost:8000/create-collaboration', {
            'collaborator_email': self.user_first['email'],
            'article_id': art.id,
        })

        self.assertEqual(response.status_code, 302)

        user_first = User.objects.get(email=self.user_first['email'])
        self.assertEqual(user_first.articles.get_queryset().count(), 1)
