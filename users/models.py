from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.exceptions import ValidationError
# https://docs.djangoproject.com/ko/4.1/topics/auth/customizing/
# 에 있는 User, UserManager 모델 입니다.


class UserManager(BaseUserManager):

    def create_user(self, account, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have a email")

        user = self.model(
            account=account,
            email=self.normalize_email(email),  # 소문자로 바꾼 후 정규화 체크
            # profile_img='default/die1_1.png',   # 기본 이미지
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(
            email=email,
            password=password,

            **extra_fields
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser):
    class Meta:
        db_table = "User"

    account = models.CharField("계정", max_length=50, unique=True)
    nickname = models.CharField("별명", max_length=15)
    email = models.EmailField(
        "이메일 주소",
        max_length=255,
        unique=True,
    )
    profile_img = models.ImageField(
        "프로필 이미지",
        upload_to='users/%Y%m%d',
        # height_field=None,
        # width_field=None,
        # max_length=None,
        # default='static/img/die1_1.png',  # default 이미지
        # default='default/die1_1.png',  # default 이미지
        blank=True,
    )
    # default(line)

    categories = (
        ('cat', '고양이'),
        ('dog', '개'),
        ('bird', '새'),
        ('fish', '물고기'),
        ('snail', '달팽이'),
        ('stone', '돌'),
        ('turtle', '거북이'),
    )
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name='followers', blank=True)  # symmetrical=False 대칭여부

    category = models.CharField(
        "반려동물 종류", choices=categories, max_length=10, blank=True
    )
    is_active = models.BooleanField("활성화 여부", default=True)
    is_staff = models.BooleanField("스태프 여부", default=False)
    is_admin = models.BooleanField("관리자 여부", default=False)

    objects = UserManager()

    USERNAME_FIELD = 'account'
    REQUIRED_FIELDS = ["email",]

    class Meta:
        db_table = "User"

    def __str__(self):
        return self.account

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

# is_staff와 is_admin 분류 해야함.
