import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIClient
from students.models import Course, Student
from students.serializers import CourseSerializer



@pytest.fixture
def API_client():
    return APIClient()

@pytest.fixture()
def courses_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory

@pytest.fixture
def students_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory

# def test_example():
#     assert True, "Just test example"

# Проверка получения 1го курса
@pytest.mark.django_db
def test_get_one_course(client, courses_factory):
    test_courses_create = courses_factory(_quantity=1)
    first_course = test_courses_create[0]
    response = client.get(f'/api/v1/courses/{first_course.id}/')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == first_course.name

# Проверка получения списка курсов
@pytest.mark.django_db
def test_get_courses_list(client, courses_factory):
    test_courses_create = courses_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    data = response.json()
    for i, course in enumerate(data):
        assert course['name'] == test_courses_create[i].name

# проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_get_courses_filter_on_id(client, courses_factory):
    test_courses_create = courses_factory(_quantity=1)
    response = client.get('/api/v1/courses/', {'id': test_courses_create[0].id})
    assert response.status_code == 200
    data = response.json()
    assert test_courses_create[0].id == data[0]['id']

# Проверка фильтрации курсов по name
@pytest.mark.django_db
def test_get_course_filter_on_name(client, courses_factory):
    test_courses_create = courses_factory(_quantity=1)
    response = client.get('/api/v1/courses/', {'name': test_courses_create[0].name})
    assert response.status_code == 200
    data = response.json()
    assert test_courses_create[0].name == data[0]['name']



# Тест успешного создания курса
@pytest.mark.django_db
def test_course_creation(client):
    response = client.post(reverse('courses-list'), data={
        'name': 'test_course_name'
    }, format='json')
    assert response.status_code == 201
    data = response.json()
    assert Course.objects.get(id=data['id']).name == 'test_course_name'


# Тест успешного обновления курса
@pytest.mark.django_db
def test_course_update(client, courses_factory):
    test_courses_create = courses_factory(_quantity=10)
    response = client.patch(reverse('courses-detail', args=[test_courses_create[0].id]), data={
        'name': 'new_name'
    }, format='json')
    print(reverse('courses-detail', args=[test_courses_create[0].id]))
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'new_name'

# Тест успешного удаления курса
@pytest.mark.django_db
def test_course_delete(client, courses_factory):
    test_courses_create = courses_factory(_quantity=1)
    response = client.delete(reverse('courses-detail', args=[test_courses_create[0].id]))
    assert response.status_code == 204