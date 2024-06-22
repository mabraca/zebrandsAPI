from django.contrib.auth.models import Group, Permission, User
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = 'Setup groups and permissions for Admins '

    def handle(self, *args, **options):
        # Create admin group if not exists
        admin_group, created = Group.objects.get_or_create(name='Admins')

        # Define permissions
        user_permissions = Permission.objects.filter(content_type__app_label='auth',
                                                     codename__in=['add_user', 'update_user', 'delete_user'])

        # Setting permission to group
        for permission in user_permissions:
            admin_group.permissions.add(permission)

        # creating an admin user with pass = Caracas1.
        admin_user, created = User.objects.get_or_create(
            username='admin',
            first_name='Maria',
            password="pbkdf2_sha256$600000$cEPRetJTrQ1tbb9Qx7qeV7$Is2JLPLiNXCMVwg2QL3Uh3CSgdio49VguQWGwIR3jGg=",
            last_name="Bracamonte",
            email="mabraca18@gmail.com",
            is_staff=True,
            is_superuser=True
        )
        # Creating token authentication
        token, created = Token.objects.get_or_create(user=admin_user)
        print(token.key)
        # the new admin user adding in the group
        admin_user.groups.add(admin_group)

        self.stdout.write(self.style.SUCCESS('Successfully setup groups and permissions.'))
