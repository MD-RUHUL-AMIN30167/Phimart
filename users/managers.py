from django.contrib.auth.base_user import BaseUserManager


class CustomUseManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_field):
        if not email:
            raise ValueError('this email field must be set')
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_field)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,password=None,**extra_field):
        extra_field.setdefault('is_staff',True)
        extra_field.setdefault('is_superuser',True)
        if not extra_field.get('is_staff'):
            raise ValueError('is staff not active')
        if not extra_field.get('is_superuser'):
            raise ValueError('is_superuser not active')
        
        return self.create_user(email,password,**extra_field)