from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from website.apps.staff_member_manager.models import StaffMember


@receiver(pre_save, sender=User)
def user_pre_save_handler(sender, instance, *args, **kwargs):
    if instance.pk is None:
        # If being created for the first time
        if User.objects.filter(email__iexact=instance.email).exists():
            # If a user with this email already exists
            raise RuntimeError("Email already in use")


@receiver(post_save, sender=StaffMember)
def staff_member_post_save_handler(sender, instance, created, **kwargs):
    staff_member = instance

    if created:
        user = staff_member.user

        if not user.has_usable_password():
            user.set_password(staff_member.generated_password)
            user.save()
            # Note that middleware will force user to change password on their first login
        else:
            # There is a password already, silently disable generated_password
            staff_member.generated_password = ""
            staff_member.save()
