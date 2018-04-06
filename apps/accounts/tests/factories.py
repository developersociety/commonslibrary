import factory

from accounts.models import User


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Sequence(lambda n: 'email{}@test.com'.format(n))
    password = 'test123'

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        if 'is_superuser' in kwargs:
            is_superuser = kwargs.pop('is_superuser')
            if is_superuser:
                return manager.create_superuser(*args, **kwargs)

        if 'is_staff' in kwargs:
            is_staff = kwargs.pop('is_staff')
            if is_staff:
                return manager.create_staff(*args, **kwargs)
        return manager.create_user(*args, **kwargs)

    @factory.post_generation
    def approved_organisations(self, created, extracted, **kwargs):
        if not created:
            return
        if extracted:
            for organisation in extracted:
                self.approved_organisations.add(organisation)
