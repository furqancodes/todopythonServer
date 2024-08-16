import unittest
import requests

BASE_URL = "http://localhost:8000/todoapp"

class TestTodoAPI(unittest.TestCase):

    def setUp(self):
        self.clear_todos()

    def clear_todos(self):
        response = requests.get(f"{BASE_URL}/todos/")
        if response.status_code == 200:
            todos = response.json()
            for todo in todos:
                requests.delete(f"{BASE_URL}/todos/{todo['id']}")

    def test_create_todo(self):
        payload = {
            "heading": "Test Todo",
            "description": "Test Description",
            "status": 1
        }
        response = requests.post(f"{BASE_URL}/todos/", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['heading'], payload['heading'])
        self.assertEqual(data['description'], payload['description'])
        self.assertEqual(data['status'], payload['status'])

    def test_get_todos(self):
        payload = {
            "heading": "Test Todo",
            "description": "Test Description",
            "status": 1
        }
        requests.post(f"{BASE_URL}/todos/", json=payload)
        response = requests.get(f"{BASE_URL}/todos/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_get_todo_by_id(self):
        payload = {
            "heading": "Test Todo",
            "description": "Test Description",
            "status": 1
        }
        create_response = requests.post(f"{BASE_URL}/todos/", json=payload)
        self.assertEqual(create_response.status_code, 201)
        todo_id = create_response.json()['id']
        response = requests.get(f"{BASE_URL}/todos/{todo_id}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['heading'], payload['heading'])
        self.assertEqual(data['description'], payload['description'])
        self.assertEqual(data['status'], payload['status'])

    def test_update_todo(self):
        payload = {
            "heading": "Test Todo",
            "description": "Test Description",
            "status": 1
        }
        create_response = requests.post(f"{BASE_URL}/todos/", json=payload)
        self.assertEqual(create_response.status_code, 201)
        todo_id = create_response.json()['id']
        update_payload = {
            "heading": "Updated Todo",
            "description": "Updated Description",
            "status": 3
        }
        response = requests.put(f"{BASE_URL}/todos/{todo_id}/", json=update_payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['heading'], update_payload['heading'])
        self.assertEqual(data['description'], update_payload['description'])
        self.assertEqual(data['status'], update_payload['status'])

    def test_delete_todo(self):
        payload = {
            "heading": "Test Todo",
            "description": "Test Description",
            "status": 1
        }
        create_response = requests.post(f"{BASE_URL}/todos/", json=payload)
        self.assertEqual(create_response.status_code, 201)
        todo_id = create_response.json()['id']
        delete_response = requests.delete(f"{BASE_URL}/todos/{todo_id}/")
        self.assertEqual(delete_response.status_code, 204)
        get_response = requests.get(f"{BASE_URL}/todos/{todo_id}/")
        self.assertEqual(get_response.status_code, 404)

    def test_set_reminder(self):
        payload = {
            "heading": "Test Todo",
            "description": "Test Description",
            "status": 1
        }
        create_response = requests.post(f"{BASE_URL}/todos/", json=payload)
        self.assertEqual(create_response.status_code, 201)
        todo_id = create_response.json()['id']
        reminder_payload = {
            "reminder_minutes": 2
        }
        reminder_response = requests.post(f"{BASE_URL}/todos/{todo_id}/set-reminder/", json=reminder_payload)
        self.assertEqual(reminder_response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
