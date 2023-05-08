from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.exceptions import ValidationError

# https://docs.djangoproject.com/ko/4.1/topics/auth/customizing/
# 에 있는 User, UserManager 모델 입니다.


class UserManager(BaseUserManager):
    def create_user(self, account, nickname, category, email, password=None):
        # if not email:
        #     raise ValueError('Users must have an email address')
        if email:
            email = validate_email(email)
        else:
            raise ValueError('Users must have an email address')

        user = self.model(
            account=account,
            nickname=nickname,
            category=category,
            email=self.normalize_email(email),  # 소문자로 바꾼 후 정규화 체크
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, account, email, password=None):
        user = self.create_user(
            account,
            password,
            email,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser):
    account = models.CharField("계정", max_length=50, unique=True)
    nickname = models.CharField("별명", max_length=15, blank=True)
    email = models.EmailField(
        "이메일 주소",
        max_length=255,
        unique=True,
    )
    profile_img = models.ImageField(
        "프로필 이미지",
        upload_to=None,
        height_field=None,
        width_field=None,
        max_length=None,
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
        "self", symmetrical=False, related_name='followers')  # symmetrical=False 대칭여부

    '''
    self,
        to: Union[Type[_T], str],
        related_name: Optional[str] = ...,
        related_query_name: Optional[str] = ...,
        limit_choices_to: Optional[Union[Dict[str, Any], Callable[[], Any], Q]] = ...,
        symmetrical: Optional[bool] = ...,
        through: Optional[Union[str, Type[Model]]] = ...,
        through_fields: Optional[Tuple[str, str]] = ...,
        db_constraint: bool = ...,
        db_table: Optional[str] = ...,
        swappable: bool = ...,
        verbose_name: Optional[Union[str, bytes]] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        max_length: Optional[int] = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        default: Any = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: Optional[str] = ...,
        unique_for_month: Optional[str] = ...,
        unique_for_year: Optional[str] = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ) -> None: ...
    '''
    category = models.CharField(
        "반려동물 종류", choices=categories, max_length=10, blank=True
    )
    is_active = models.BooleanField("활성화 여부", default=True)
    is_staff = models.BooleanField("스태프 여부", default=False)
    is_admin = models.BooleanField("관리자 여부", default=False)

    objects = UserManager()

    USERNAME_FIELD = 'account'
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.email

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
