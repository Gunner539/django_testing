import pytest
import pytest_django
from model_bakery import baker
from rest_framework.test import APIClient

@pytest.fixture
def API_client():
    return APIClient()

@pytest.fixture()
def courses_factory():
    def factory(*args, **kwargs):
        return baker.make('students.Course', *args, **kwargs)

    return factory

@pytest.fixture
def students_factory():
    def factory(*args, **kwargs):
        return baker.make('students.Student', *args, **kwargs)

    return factory