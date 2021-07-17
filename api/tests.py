from rest_framework.test import APITestCase
from django.shortcuts import reverse
from .models import Show, Role, Quote
from django.contrib.auth.models import User
import json
from rest_framework_simplejwt.tokens import RefreshToken

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


class AdminCreateListQuoteTestCase(APITestCase):
    url = reverse("api:admin_create_list_quote")

    def setUp(self):
        self.show_name = "test show creation"
        self.role_name = "test role creation"
        self.data = json.dumps(
            {
                "show": self.show_name,
                "role": self.role_name,
                "quote": "some quote",
                "contain_adult_lang": True
            }
        )
        self.invalid_data = json.dumps(
            {
                "show": self.show_name,
                "role": self.role_name,
            }
        )
        self.username = "test"
        self.email = "test@test.com"
        self.password = "sometestpassword"
        self.create()
        self.header = {
            "HTTP_AUTHORIZATION":
            "Bearer " + str(RefreshToken.for_user(self.user).access_token)}

    def create(self):
        show = Show.objects.create(name=self.show_name)
        role = Role.objects.create(name=self.role_name)
        Quote.objects.create(
            show=show,
            role=role,
            quote=test_quote_text
        )
        self.user = User.objects.create(
            username=self.username,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            email=self.email,
            password=self.password
        )

    def test_quote_creation_invalid_authentication(self):
        response = self.client.post(
            self.url,
            data=self.data
        )
        self.assertEqual(
            response.status_code, 401,
            f"expected status code 401, got {response.status_code}")

    def test_quote_creation_valid_authentication(self):
        response = self.client.post(
            self.url,
            self.data, content_type="application/json", **self.header
        )
        self.assertEqual(
            response.status_code, 201,
            f"expected status code 201, got {response.status_code}")

    def test_quote_creation_ivalid_data(self):
        response = self.client.post(
            self.url, data=self.invalid_data, **self.header)

        self.assertEqual(
            response.status_code, 400,
            f"expected status code 400, got {response.status_code}")

    def test_quote_list(self):
        response = self.client.get(self.url, **self.header)
        self.assertEqual(
            response.status_code, 200,
            f"expected status code 200, got {response.status_code}"
        )
        self.assertEqual(
            len(response.json()), 1,
            f"expected 1 object, got {len(response.json())}"
        )


class EditAndDeleteQuoteTestCase(APITestCase):
    def setUp(self):
        self.show_name1 = "test show creation1"
        self.role_name1 = "test role creation1"
        self.show_name2 = "test show creation2".title()
        self.role_name2 = "test role creation2".title()
        self.username = "test"
        self.email = "test@test.com"
        self.password = "sometestpassword"
        self.create()
        self.url = reverse(
            "api:admin_edit_delete_quote", kwargs={"key": self.quote.key})

        self.header = {
            "HTTP_AUTHORIZATION":
            "Bearer " + str(RefreshToken.for_user(self.user).access_token)}

    def create(self):
        show1 = Show.objects.create(name=self.show_name1)
        role1 = Role.objects.create(name=self.role_name1)
        self.show2 = Show.objects.create(name=self.show_name2)
        self.role2 = Role.objects.create(name=self.role_name2)
        self.quote = Quote.objects.create(
            show=show1,
            role=role1,
            quote=test_quote_text,
            contain_adult_lang=True
        )
        self.user = User.objects.create(
            username=self.username,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            email=self.email,
            password=self.password
        )

    def test_edit_quote_valid(self):
        data = {
            "show": self.show_name2,
            "contain_adult_lang": False
        }
        response = self.client.put(
            self.url, data, **self.header)
        self.assertEqual(
            response.status_code, 200,
            f"expected status code 200, got {response.status_code}")
        self.assertEqual(response.json()["detail"], "updated")

    def test_edit_quote_invalid(self):
        data = {
            "show": "test valid show name",
            "role": "test valid role name",
            "contain_adult_lang": False
        }
        response = self.client.put(
            self.url, data, **self.header)
        self.assertEqual(
            response.status_code, 404,
            f"expected status code 404, got {response.status_code}")
        self.assertEqual(response.json()["detail"], "Not found.")
