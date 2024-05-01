import pytest
from django.contrib.auth.models import AnonymousUser

from django.test import RequestFactory
from django.urls import reverse
from django.utils import timezone
from checklists import views
from checklists.factories import UserFactory, ChecklistFactory, ChecklistItemFactory


def setup_index_view(sort_string, client):
    factory = RequestFactory()

    # Create a GET request with the desired query parameters
    url = reverse("checklists:index") + sort_string
    request = factory.get(url)
    # user = User.objects.create_user(username="testuser", password="testpassword")
    client.force_login(UserFactory())

    return client.get(url)


@pytest.mark.django_db
class TestChecklistIndexView:

    @pytest.fixture
    def author_a(self):
        return UserFactory(first_name="Simon")

    @pytest.fixture
    def author_b(self):
        return UserFactory(first_name="Theodore")

    @pytest.fixture
    def checklist_a(self, author_a):
        return ChecklistFactory(
            author=author_a,
            created_on=(timezone.now() - timezone.timedelta(days=2)),
        )

    @pytest.fixture
    def checklist_b(self, author_b):
        return ChecklistFactory(
            author=author_b,
            created_on=(timezone.now() - timezone.timedelta(days=1)),
        )

    @pytest.fixture
    def checklist_item_a(self, checklist_a):
        return ChecklistItemFactory(checklist=checklist_a, completed=True)

    def test_index_returns_sorted_by_author_asc(self, client, checklist_a, checklist_b):
        response = setup_index_view(sort_string="?sort-by-author=asc", client=client)
        sorted_checklists = response.context["checklists"]
        assert checklist_a == sorted_checklists[0]

    def test_index_returns_sorted_by_progress_asc(self, client, checklist_a, checklist_b, checklist_item_a):
        response = setup_index_view(sort_string="?sort-by-progress=asc", client=client)
        sorted_checklists = response.context["checklists"]
        assert checklist_b == sorted_checklists[0]

    def test_index_returns_sorted_by_created_on_desc(self, client, checklist_a, checklist_b):
        response = setup_index_view(sort_string="?sort-by-created_on=desc", client=client)
        sorted_checklists = response.context["checklists"]
        assert checklist_b == sorted_checklists[0]
