from django.core.exceptions import ValidationError

from django.core.management.base import BaseCommand
from api.users.models import AdminProfile


class Command(BaseCommand):
    help = 'Create a superuser with additional unique fields'

    def get_input_data(self, field, message, default=None):
        value = input(message)
        if value == '':
            return default
        return value

    def handle(self, *args, **options):
        options['is_staff'] = True
        options['is_superuser'] = True

        # Prompt for unique fields
        while True:
            email = self.get_input_data('email', 'Email: ')
            password = self.get_input_data('password', 'Password: ')
            phone = self.get_input_data('phone', 'Phone: ')
            fullname = self.get_input_data('fullname', 'Fullname: ')

            try:
                superuser = self.UserModel._default_manager.db_manager().create_superuser(
                    email=email, password=password, phone=phone
                )
                break  # Exit the loop if the user creation is successful
            except ValidationError as e:
                self.stderr.write('\n'.join(e.messages))
                self.stderr.write('Please correct the errors.\n')

        # Create the related admin model instance
        AdminProfile.objects.create(user=superuser, fullname=fullname)

        self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))

