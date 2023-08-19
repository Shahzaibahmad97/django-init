from django.core.management.base import BaseCommand
from django.core.management import call_command

from api.users.models import User
from api.categories.models import Category
from api.product_types.models import ProductType
from api.vendors.models import Vendor


class Command(BaseCommand):
    help = 'Load initial data'

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('Admin data already exists. No action required.'))
        else:
            call_command('loaddata', 'fixtures/users.json')
            call_command('loaddata', 'fixtures/admin_profile.json')
            self.stdout.write(self.style.SUCCESS('Admin data loaded successfully.'))

        if Category.objects.exists():
            self.stdout.write(self.style.SUCCESS('Category data already exists. No action required.'))
        else:
            call_command('loaddata', 'fixtures/categories.json')
            self.stdout.write(self.style.SUCCESS('Category data loaded successfully.'))

        if ProductType.objects.exists():
            self.stdout.write(self.style.SUCCESS('ProductType data already exists. No action required.'))
        else:
            call_command('loaddata', 'fixtures/product_types.json')
            self.stdout.write(self.style.SUCCESS('ProductType data loaded successfully.'))

        if Vendor.objects.exists():
            self.stdout.write(self.style.SUCCESS('Vendor data already exists. No action required.'))
        else:
            call_command('loaddata', 'fixtures/vendors.json')
            self.stdout.write(self.style.SUCCESS('Vendor data loaded successfully.'))


