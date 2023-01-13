from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, password2=None, first_name=None, last_name=None, phone_no=None, aadhar=None, pan=None, cheque=None, role=None, created_by=None, refer_code=None, referred_by=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_no=phone_no,
            aadhar=aadhar,
            pan=pan,
            cheque=cheque,
            role=role,
            refer_code=refer_code,
            referred_by = referred_by,
            created_by=created_by
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password,  first_name, last_name, phone_no, password2=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_no=phone_no,

        )
        user.is_admin = True
        user.is_staff = True
        user.is_verified = True
        user.save(using=self._db)
        return user

    def create_admin(self, email, password,  first_name, last_name, phone_no, password2=None, role=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_no=phone_no,
            role = role

        )
        user.save(using=self._db)
        return user