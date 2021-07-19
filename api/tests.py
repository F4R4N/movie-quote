from rest_framework.test import APITestCase
from django.shortcuts import reverse
from .models import Show, Role, Quote
from django.contrib.auth.models import User
import json
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.text import slugify

random_quote = "api:random_quote"
test_quote_text = "test quote"
AUTH_TOKEN_PREFIX = "Bearer "
EMAIL = "test@test.com"


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
        self.password = "sometestpassword"
        self.create()
        self.header = {
            "HTTP_AUTHORIZATION":
            AUTH_TOKEN_PREFIX + str(
                RefreshToken.for_user(self.user).access_token)
        }

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
            email=EMAIL,
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
        self.show_name1 = "test show creation1".title()
        self.role_name1 = "test role creation1".title()
        self.show_name2 = "test show creation2".title()
        self.role_name2 = "test role creation2".title()
        self.username = "test"
        self.password = "sometestpassword"
        self.create()
        self.url = reverse(
            "api:admin_edit_delete_quote", kwargs={"key": self.quote.key})

        self.header = {
            "HTTP_AUTHORIZATION":
            AUTH_TOKEN_PREFIX + str(
                RefreshToken.for_user(self.user).access_token)
        }

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
            email=EMAIL,
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

    def test_delete_quote_valid(self):
        response = self.client.delete(
            self.url,
            **self.header
        )
        self.assertEqual(
            response.status_code, 200,
            f"expected status code 200, got {response.status_code}")
        self.assertEqual(response.json()["detail"], "deleted")


class EditShowTestCase(APITestCase):
    def setUp(self):
        self.show_name1 = "test show creation1"
        self.show_name2 = "test show creation2".title()
        self.username = "test"
        self.password = "sometestpassword"
        self.create()
        self.url = reverse(
            "api:admin_edit_show", kwargs={"slug": slugify(self.show_name1)})

        self.header = {
            "HTTP_AUTHORIZATION":
            AUTH_TOKEN_PREFIX + str(
                RefreshToken.for_user(self.user).access_token)
        }

    def create(self):
        Show.objects.create(name=self.show_name1)
        self.user = User.objects.create(
            username=self.username,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            email=EMAIL,
            password=self.password
        )

    def test_edit_show_valid(self):
        response = self.client.put(
            self.url,
            {"name": self.show_name2},
            **self.header
        )
        self.assertEqual(
            response.status_code, 200,
            f"expected status code 200, got {response.status_code}")
        self.assertEqual(response.json()["detail"], "show updated")
        all_shows = Show.objects.all()
        self.assertEqual(len(all_shows), 1)
        self.assertEqual(all_shows[0].name, self.show_name2)

    def test_edit_show_invalid_data(self):
        response = self.client.put(
            self.url,
            {"hello": self.show_name1},
            **self.header
        )
        self.assertEqual(
            response.status_code, 400,
            f"expected status code 400, got {response.status_code}")
        self.assertEqual(response.json()["detail"], "no new data provided.")

    def test_edit_show_no_token(self):
        response = self.client.put(
            self.url,
            {"name": self.show_name1}
        )
        self.assertEqual(
            response.status_code, 401,
            f"expected status code 401, got {response.status_code}")

    def test_invalid_http_method(self):
        response = self.client.post(
            self.url,
            {"name": self.show_name1},
            **self.header
        )
        self.assertEqual(
            response.status_code,
            405,
            f"expected status code 405, got {response.status_code}"
        )

    def test_edit_show_not_exist_show(self):
        url = reverse(
            "api:admin_edit_show",
            kwargs={"slug": "its_test"})
        response = self.client.put(
            url,
            {"name", "its_not_test"},
            **self.header
        )
        self.assertEqual(
            response.status_code, 404,
            f"expected status code 404, got {response.status_code}"
        )


class AllShowsTestCase(APITestCase):
    def setUp(self):
        self.show_name1 = "test show creation1".title()
        self.show_name2 = "test show creation2".title()
        self.create()
        self.url = reverse(
            "api:all_shows")

    def create(self):
        Show.objects.create(name=self.show_name1)
        Show.objects.create(name=self.show_name2)

    def test_show_availability(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code, 200,
            f"expected status code 200, got {response.status_code}")
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["name"], self.show_name1)

    def test_invalid_methods(self):
        post = self.client.post(self.url)
        put = self.client.put(self.url)
        delete = self.client.delete(self.url)
        self.assertEqual(post.status_code, 405)
        self.assertEqual(put.status_code, 405)
        self.assertEqual(delete.status_code, 405)


class EditRoleTestCase(APITestCase):
    def setUp(self):
        self.role_name1 = "test role creation1"
        self.role_name2 = "test role creation2".title()
        self.username = "test"
        self.password = "sometestpassword"
        self.create()
        self.url = reverse(
            "api:admin_edit_role", kwargs={"slug": slugify(self.role_name1)})

        self.header = {
            "HTTP_AUTHORIZATION":
            AUTH_TOKEN_PREFIX + str(
                RefreshToken.for_user(self.user).access_token)
        }

    def create(self):
        Role.objects.create(name=self.role_name1)
        self.user = User.objects.create(
            username=self.username,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            email=EMAIL,
            password=self.password
        )

    def test_edit_role_valid(self):
        response = self.client.put(
            self.url,
            {"name": self.role_name2},
            **self.header,
        )
        self.assertEqual(
            response.status_code, 200,
            f"expected status code 200, got {response.status_code}"
        )
        self.assertEqual(
            response.json()["detail"],
            "role updated."
        )

    def test_edit_role_invalid_data(self):
        response = self.client.put(
            self.url,
            {"hello": self.role_name2},
            **self.header
        )
        self.assertEqual(
            response.status_code, 400
        )
        self.assertEqual(
            response.json()["detail"],
            "no new data provided.",
        )

    def test_not_exist_role(self):
        url = reverse(
            "api:admin_edit_role", kwargs={"slug": "not_exists_test_role"})
        response = self.client.put(
            url, {"name": "test role name"},
            **self.header
        )
        self.assertEqual(
            response.status_code, 404,
            f"expected status code 404, got {response.status_code}"
        )

    def test_invalid_methods(self):
        post = self.client.post(self.url, {"name": "test"}, **self.header)
        get = self.client.get(self.url, **self.header)
        delete = self.client.delete(self.url, **self.header)
        self.assertEqual(post.status_code, 405, post.content)
        self.assertEqual(get.status_code, 405, get.content)
        self.assertEqual(delete.status_code, 405, delete.content)


class AdminListAllRolesTestCase(APITestCase):
    def setUp(self):
        self.role_name1 = "test role creation1".title()
        self.role_name2 = "test role creation2".title()
        self.role_name3 = "test role creation3".title()
        self.username = "test"
        self.password = "sometestpassword"
        self.create()
        self.url = reverse(
            "api:admin_all_roles")
        self.header = {
            "HTTP_AUTHORIZATION":
            AUTH_TOKEN_PREFIX + str(
                RefreshToken.for_user(self.user).access_token)
        }

    def create(self):
        Role.objects.create(name=self.role_name1)
        Role.objects.create(name=self.role_name2)
        Role.objects.create(name=self.role_name3)
        self.user = User.objects.create(
            username=self.username,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            email=EMAIL,
            password=self.password
        )

    def test_role_availability(self):
        response = self.client.get(
            self.url,
            **self.header
        )
        self.assertEqual(
            response.status_code, 200,
            f"expected status code 200, got {response.status_code}"
        )
        self.assertEqual(
            len(response.json()), 3,
            f"expected 3 object, got {len(response.json())}"
        )

    def test_invalid_methods(self):
        post = self.client.post(self.url, {"name": "test"}, **self.header)
        put = self.client.put(self.url, **self.header)
        delete = self.client.delete(self.url, **self.header)
        self.assertEqual(post.status_code, 405, post.content)
        self.assertEqual(put.status_code, 405, put.content)
        self.assertEqual(delete.status_code, 405, delete.content)


class AdminAddListUserTestCase(APITestCase):
    def setUp(self):
        self.admin_username = "admin"
        self.admin_password = "password"
        self.username1 = "test1"
        self.password1 = "sometestpassword"
        self.username2 = "test2"
        self.password2 = "sometestpassword"
        self.data = {
            "username": "test",
            "email": "test1@test.com",
            "first_name": "test",
            "last_name": "test",
            "is_active": True,
            "is_superuser": True,
            "password1": "this is a password",
            "password2": "this is a password"
        }
        self.create()
        self.url = reverse(
            "api:admin_create_list_user")
        self.header = {
            "HTTP_AUTHORIZATION":
            AUTH_TOKEN_PREFIX + str(
                RefreshToken.for_user(self.user).access_token)
        }

    def create(self):
        self.user = User.objects.create(
            username=self.admin_username,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            email=EMAIL,
            password=self.admin_password
        )
        User.objects.create(
            username=self.username1,
            password=self.password1,
            email="1" + EMAIL
        )
        User.objects.create(
            username=self.username2,
            password=self.password2,
            email="2" + EMAIL
        )

    def test_list_all_users(self):
        response = self.client.get(
            self.url,
            **self.header
        )
        self.assertEqual(
            response.status_code, 200,
            f"expected status code 200, got {response.status_code}"
        )
        self.assertEqual(
            len(response.json()), 3,
            f"expected 3 object, got {len(response.json())}"
        )

    def test_create_user_valid(self):
        response = self.client.post(
            self.url,
            self.data,
            **self.header
        )
        self.assertEqual(
            response.status_code, 201,
            f"expected status code 201, got {response.status_code}"
        )
