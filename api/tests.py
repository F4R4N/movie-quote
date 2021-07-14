from rest_framework.test import APITestCase
from django.shortcuts import reverse
from .models import Show, Role, Quote

random_quote = "api:random_quote"
test_quote_text = "test quote"


class MainPageTestCase(APITestCase):
    url = reverse("api:main_page")

    def setUp(self):
        self.show_name1 = "test_show1"
        self.show_name2 = "test_show2"

        self.create_show()

    def create_show(self):
        Show.objects.create(name=self.show_name1)
        Show.objects.create(name=self.show_name2)

    def test_path_accessibility(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            200,
            f"expected status code 200, got {response.status_code}")

    def test_shows_list(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.json()["showSlugs"], [self.show_name1, self.show_name2])


class RandomQuoteTestCase(APITestCase):
    url = reverse(random_quote)
    url_censored = "%s?censored" % reverse(random_quote)

    def setUp(self):
        self.show_name = "test_show"
        self.role_name = "test_role"
        self.quote = test_quote_text
        self.contain_adult_lang = True

        self.create_quote()

    def create_quote(self):
        show = Show.objects.create(name=self.show_name)
        role = Role.objects.create(name=self.role_name)
        Quote.objects.create(
            quote=self.quote,
            show=show,
            role=role,
            contain_adult_lang=self.contain_adult_lang
        )

    def test_quote(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code, 200,
            f"expected status code 200, got {response.status_code}")

        self.assertEqual(
            response.json()["quote"], self.quote, "quote don't match")

        self.assertEqual(
            response.json()["show"], self.show_name, "show name don't match")

        self.assertEqual(
            response.json()["role"], self.role_name, "role name don't match")

        self.assertTrue(response.json()["contain_adult_lang"])

    def test_censored_quote_not_accessible(self):
        response = self.client.get(self.url_censored)
        self.assertEqual(
            response.status_code, 200,
            f"expected status code 200, got {response.status_code}")

        self.assertEqual(response.json()["status"], "no_quote")


class CensoredQuoteTestCase(APITestCase):
    url = "%s?censored" % reverse(random_quote)

    def setUp(self):
        self.show_name = "test_show"
        self.role_name = "test_role"
        self.quote = test_quote_text
        self.contain_adult_lang = False

        self.create_quote()

    def create_quote(self):
        show = Show.objects.create(name=self.show_name)
        role = Role.objects.create(name=self.role_name)
        Quote.objects.create(
            quote=self.quote,
            show=show,
            role=role,
            contain_adult_lang=self.contain_adult_lang
        )

    def test_censored_quote_accessible(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code, 200,
            f"expected status code 200, got {response.status_code}")

        self.assertEqual(response.json()["quote"], self.quote)


class SpecificShowQuotesTestCase(APITestCase):
    url_path = "api:show_quote"

    def setUp(self):
        self.show_name = "test_show"
        self.role_name = "test_role"
        self.quote = test_quote_text
        self.contain_adult_lang = False
        self.alter_show_name = "alter_test_show_name"
        self.create_objects()

    def create_objects(self):
        show = Show.objects.create(name=self.show_name)
        role = Role.objects.create(name=self.role_name)
        Quote.objects.create(
            quote=self.quote,
            show=show,
            role=role,
            contain_adult_lang=self.contain_adult_lang
        )
        Show.objects.create(name=self.alter_show_name)

    def test_quote_valid(self):
        url = reverse(self.url_path, kwargs={"slug": self.show_name})
        response = self.client.get(url)

        self.assertEqual(
            response.status_code, 200,
            f"expected status code 200, got {response.status_code}")

        self.assertEqual(
            response.json()["quote"],
            self.quote
        )

        self.assertEqual(
            response.json()["show"],
            self.show_name
        )

    def test_quote_invalid(self):
        url = reverse(self.url_path, kwargs={"slug": "invalid_show_slug"})
        response = self.client.get(url)

        self.assertEqual(
            response.status_code, 404,
            f"expected status code 404, got {response.status_code}")

        self.assertEqual(
            response.json()["detail"],
            "Not found."
        )

    def test_no_quote_associate_with_show(self):
        url = reverse(self.url_path, kwargs={"slug": self.alter_show_name})
        response = self.client.get(url)

        self.assertEqual(
            response.status_code, 204,
            f"expected status code 204, got {response.status_code}")
