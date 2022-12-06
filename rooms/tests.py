from rest_framework.test import APITestCase

from rooms import models
from users.models import User


class TestAmenities(APITestCase):
    NAME = "Amenity Test"
    DESC = "Amenity Desc"

    URL = "/api/v1/rooms/amenities/"
    Page = 1

    #
    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_all_amenities(self):
        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(response.status_code, 200, "Status code is not 200")
        # print(data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], self.NAME)
        self.assertEqual(data[0]['description'], self.DESC, )

    def test_create_amenity(self):
        new_amenity_name = "New Amenity"
        new_amenity_description = "New Amenity Des."

        response = self.client.post(
            self.URL,
            data={"name": new_amenity_name,
                  "description": new_amenity_description,
                  },
        )
        data = response.json()
        self.assertEqual(response.status_code, 200, "Not 200 status code")
        self.assertEqual(data['name'], new_amenity_name)
        self.assertEqual(data['description'], new_amenity_description)

        response = self.client.post(self.URL)
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)


class TestAmenity(APITestCase):
    NAME = 'test_amenity'
    DESC = 'test_description'

    URL = "/api/v1/rooms/amenities/"
    Page = "1"
    PUT_URL = URL + Page

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_amenity_not_found(self):
        response = self.client.get("/api/v1/rooms/amenities/2/")
        self.assertEqual(response.status_code, 404)

    def test_get_amenity(self):
        response = self.client.get("/api/v1/rooms/amenities/2/")
        self.assertEqual(response.status_code, 404)
        response = self.client.get("/api/v1/rooms/amenities/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['name'], self.NAME)
        self.assertEqual(data['description'], self.DESC)

    def test_put_amenity(self):
        put_amenity_name = "Put Amenity"
        put_amenity_description = "Put Amenity Desc"

        response = self.client.put(
            self.PUT_URL, data={
                "name": put_amenity_name,
                "description": put_amenity_description,
            },
        )

        data = response.json()
        print("data:", data)
        self.assertEqual(response.status_code, 200, "Not 200 status code")
        self.assertEqual(data['name'], put_amenity_name)
        self.assertEqual(data['description'], put_amenity_description)
        response = self.client.put(self.PUT_URL)
        data = response.json()
        self.assertIn("name", data)

    def test_delete_amenity(self):
        response = self.client.delete("/api/v1/rooms/amenities/1")
        self.assertEqual(response.status_code, 204)


class TestRooms(APITestCase):

    def setUp(self):
        user = User.objects.create(username="test")
        user.set_password("1234")
        user.save()
        self.user = user

    def test_create_room(self):
        response = self.client.post("/api/v1/rooms/")
        self.assertEqual(response.status_code, 403, "Not 403")

        self.client.force_login(self.user)
        # self.client.login(
        #     username="test", password="1234", )
        response = self.client.post("/api/v1/rooms/")
        print(response.json())
