from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from library.models import Member


class Command(BaseCommand):
    help = 'Create test users for the library system'

    def handle(self, *args, **options):
        # Create a librarian (staff user)
        librarian, created = User.objects.get_or_create(
            username='librarian',
            defaults={
                'email': 'librarian@library.com',
                'first_name': 'John',
                'last_name': 'Librarian',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            librarian.set_password('password123')
            librarian.save()
            self.stdout.write(
                self.style.SUCCESS('Successfully created librarian user')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Librarian user already exists')
            )

        # Create a regular member
        member_user, created = User.objects.get_or_create(
            username='member',
            defaults={
                'email': 'member@library.com',
                'first_name': 'Jane',
                'last_name': 'Member',
                'is_staff': False,
                'is_superuser': False,
            }
        )
        if created:
            member_user.set_password('password123')
            member_user.save()
            self.stdout.write(
                self.style.SUCCESS('Successfully created member user')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Member user already exists')
            )

        # Create member profile
        member_profile, created = Member.objects.get_or_create(
            user=member_user,
            defaults={
                'name': 'Jane Member',
                'email': 'member@library.com',
            }
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created member profile')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Member profile already exists')
            )

        self.stdout.write(
            self.style.SUCCESS('Test users created successfully!')
        )
        self.stdout.write('Librarian: username=librarian, password=password123')
        self.stdout.write('Member: username=member, password=password123')
