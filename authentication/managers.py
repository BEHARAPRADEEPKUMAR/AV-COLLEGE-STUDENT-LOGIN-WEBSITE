from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, rollno, email, dateofbirth, password=None, **extra_fields):
        if not rollno:
            raise ValueError("The Roll Number field must be set")
        if not email:
            raise ValueError("The Email field must be set")
        if not dateofbirth:
            raise ValueError("The Date of Birth field must be set")

        email = self.normalize_email(email)
        user = self.model(rollno=rollno, email=email, dateofbirth=dateofbirth, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, rollno, email, dateofbirth, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not password:
            raise ValueError("Superusers must have a password.")

        return self.create_user(rollno=rollno, email=email, dateofbirth=dateofbirth, password=password, **extra_fields)