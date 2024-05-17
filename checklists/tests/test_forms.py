import pytest

from ..factories import CategoryFactory, ChecklistFactory, TemplateTypeFactory, TemplateFactory
from ..forms import ChecklistFilterForm


@pytest.mark.django_db
class TestChecklistFilterForm:
    @pytest.fixture
    def category_a(self):
        return CategoryFactory(name='alpha')

    @pytest.fixture
    def category_b(self):
        return CategoryFactory(name='bravo')

    @pytest.fixture
    def template_type_a(self):
        return TemplateTypeFactory(name='alpha')

    @pytest.fixture
    def template_type_b(self):
        return TemplateTypeFactory(name='bravo')

    @pytest.fixture
    def template_a(self, template_type_a):
        return TemplateFactory(type=template_type_a)

    @pytest.fixture
    def template_b(self, template_type_b):
        return TemplateFactory(type=template_type_b)

    @pytest.fixture
    def checklist_a(self, category_a, template_a):
        return ChecklistFactory(category=category_a, template=template_a)

    @pytest.fixture
    def checklist_b(self, category_b, template_b):
        return ChecklistFactory(category=category_b, template=template_b)

    def test_filter_by_category(self, checklist_a, checklist_b, category_a):
        form = ChecklistFilterForm(data={"category": category_a.id})
        form.is_valid()
        result = form.filter_checklists()

        assert checklist_a in result and checklist_b not in result

    def test_filter_by_template_type(self, template_type_b, checklist_a, checklist_b):
        form = ChecklistFilterForm(data={"template_type": template_type_b.id})
        form.is_valid()
        result = form.filter_checklists()

        assert checklist_a not in result and checklist_b in result

    def test_filter_checklists(self, template_type_b, category_a, checklist_a, checklist_b):
        form = ChecklistFilterForm(data={
            "template_type": template_type_b.id,
            "category": category_a.id,
        })
        form.is_valid()
        result = form.filter_checklists()

        assert result.count() == 0
