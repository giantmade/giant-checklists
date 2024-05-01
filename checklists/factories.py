import factory
from django.contrib.auth.models import User
from .models import Checklist, ChecklistItem, Category
from templates.models import TemplateType, Template, TemplateItem


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class TemplateTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TemplateType

    name = factory.Faker('word')
    slug = factory.Sequence(lambda n: f"template-type-{n}")


class TemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Template

    title = factory.Faker('sentence')
    description = factory.Faker('paragraph')
    author = factory.SubFactory(UserFactory)
    is_active = True
    type = factory.SubFactory(TemplateTypeFactory)


class TemplateItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TemplateItem

    template = factory.SubFactory(TemplateFactory)
    description = factory.Faker('sentence')
    position = factory.Sequence(lambda n: n)
    is_active = True


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('word')
    slug = factory.Sequence(lambda n: f"category-{n}")


class ChecklistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Checklist

    template = factory.SubFactory(TemplateFactory)
    title = factory.Faker('sentence')
    notes = factory.Faker('paragraph')
    author = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)


class ChecklistItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChecklistItem

    checklist = factory.SubFactory(ChecklistFactory)
    original_item = factory.SubFactory(TemplateItemFactory)
    description = factory.Faker('sentence')
    notes = factory.Faker('paragraph')
