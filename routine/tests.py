from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import CustomUser as User
from .models import Routine, RoutineResult, RoutineDay


class APIViewTestCase(APITestCase):
    def authenticate(self):
        credentials = {"email": "testuser@abc.com", "password": "password3^"}
        User.objects.create_user(**credentials)
        self.client.login(**credentials)

    def get_new_routine_id(self):
        routine = self.get_new_routine()
        return routine.routine_id

    def get_new_routine(self):
        routine = Routine.objects.latest("routine_id")
        return routine


class TestRoutineCreateView(APIViewTestCase):
    def setUp(self):
        self.create_data = {
            "title": "test title",
            "category": "HOMEWORK",
            "goal": "test goal",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"],
        }
        self.routine_count = Routine.objects.all().count()

    def test_create_routine(self):
        self.authenticate()
        response = self.client.post("/routine/", self.create_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        routine_id = self.get_new_routine_id()
        response_data = {"routine_id": routine_id}
        self.assertEqual(response_data, response.data["data"])

        response_message = {"msg": "  .", "status": "ROUTINE_CREATE_OK"}
        self.assertEqual(response_message, response.data["message"])

        new_routine = self.get_new_routine()
        self.assertEqual(new_routine.title, self.create_data["title"])
        self.assertEqual(new_routine.is_alarm, self.create_data["is_alarm"])
        self.assertEqual(Routine.objects.all().count(), self.routine_count + 1)

    def test_create_routine_day_if_create_routine(self):
        self.authenticate()
        response = self.client.post("/routine/", self.create_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(RoutineDay.objects.all().count(), 3)


class TestRoutineListView(APITestCase):
    def setUp(self):
        self.credentials = {"email": "testuser2@abc.com", "password": "password7^"}
        self.user = User.objects.create_user(**self.credentials)
        self.routine = Routine.objects.create(
            account_id=self.user,
            title="test title",
            category="MIRACLE",
            goal="test goal",
            is_alarm=True,
        )

        self.current_date_time = timezone.now()
        RoutineDay.objects.create(day=self.current_date_time, routine_id=self.routine)
        self.routine_result = RoutineResult.objects.create(
            routine_id=self.routine, result="TRY"
        )

    def test_get_routine_list(self):
        date = self.current_date_time.strftime("%Y/%m/%d")

        self.client.login(**self.credentials)
        response = self.client.get(f"/routine/{date}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = {
            "goal": "test goal",
            "id": self.user.id,
            "result": "TRY",
            "title": "test title",
        }
        self.assertIn(response_data, response.data["data"])

        response_message = {"msg": "  .", "status": "ROUTINE_LIST_OK"}
        self.assertEqual(response_message, response.data["message"])


class TestRoutineDetailUpdateDeleteView(APIViewTestCase):
    def setUp(self):
        self.data = {
            "title": "test title",
            "category": "HOMEWORK",
            "goal": "test goal",
            "is_alarm": True,
            "days": ["MON", "WED", "SUN"],
        }

    def test_get_routine_detail(self):
        self.authenticate()
        response = self.client.post("/routine/", self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        routine = self.get_new_routine()
        routine_id = self.get_new_routine_id()
        self.routine_result = RoutineResult.objects.create(
            result="TRY", routine_id=routine
        )

        response = self.client.get(f"/routine/{routine_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data["data"]
        self.assertEqual("test title", response_data["title"])
        self.assertEqual("TRY", response_data["result"])

        response_message = {"msg": "  .", "status": "ROUTINE_DETAIL_OK"}
        self.assertEqual(response_message, response.data["message"])

    def test_update_routine(self):
        self.authenticate()
        response = self.client.post("/routine/", self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        routine = self.get_new_routine()
        self.assertFalse(routine.is_deleted)
        routine_id = self.get_new_routine_id()

        update_date = {
            "routine_id": routine_id,
            "title": "test update title",
            "category": "MIRACLE",
            "goal": "goal update goal",
            "days": ["WED", "FRI"],
        }

        response = self.client.put(
            f"/routine/{routine_id}/", update_date, format="json"
        )

        response_data = {"routine_id": routine_id}
        self.assertEqual(response_data, response.data["data"])

        response_message = {"msg": "  .", "status": "ROUTINE_UPDATE_OK"}
        self.assertEqual(response_message, response.data["message"])

        routine.refresh_from_db()
        self.assertEqual(routine.title, "test update title")
        self.assertEqual(routine.category, "MIRACLE")

    def test_delete_routine(self):
        self.authenticate()
        response = self.client.post("/routine/", self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        routine = self.get_new_routine()
        self.assertFalse(routine.is_deleted)

        routine_id = self.get_new_routine_id()
        response = self.client.delete(f"/routine/{routine_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = {"routine_id": routine_id}
        self.assertEqual(response.data["data"], response_data)

        response_message = {"msg": "  .", "status": "ROUTINE_DELETE_OK"}
        self.assertEqual(response.data["message"], response_message)

        routine.refresh_from_db()
        self.assertTrue(routine.is_deleted)


class TestRoutineResultCreateView(APIViewTestCase):
    def setUp(self):
        self.credentials = {"email": "testuser3@abc.com", "password": "password7^"}
        self.user = User.objects.create_user(**self.credentials)
        self.routine = Routine.objects.create(
            account_id=self.user,
            title="test title",
            category="MIRACLE",
            goal="test goal",
            is_alarm=True,
        )

    def test_create_routine_result(self):
        self.client.login(**self.credentials)
        response = self.client.post(
            f"/routine/result/{self.routine.routine_id}/",
            {"result": "DONE"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(RoutineResult.objects.all().count(), 1)

        new_routine_result = RoutineResult.objects.latest("routine_result_id")
        self.assertEqual(new_routine_result.result, "DONE")
