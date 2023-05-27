from rest_framework.validators import UniqueValidator, ValidationError
from rest_framework import serializers

from django.contrib.auth import password_validation as pw

from users.models import CustomUsers

from recipes.models import Recipe


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор списка пользователей.
    Регистрации пользователя.
    Профиля пользователя.
    Информации о текущем пользователе.
    """

    is_subscribed = serializers.SerializerMethodField()
    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(
                queryset=CustomUsers.objects.all(),
                message='Пользователь с таким Логином уже существует.'
            ),
        ]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[
            UniqueValidator(
                queryset=CustomUsers.objects.all(),
                message=f'Пользователь c таким email уже существует'
            ),
        ]
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUsers
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed',
        )


    def get_is_subscribed(self, obj):
        """
        Информации о подписке на пользователя
        """

        if self.context.get('request').path_info == '/api/users/me/':
            return False

        user = self.context.get('request').user
        if user.is_authenticated:
            try:
                return obj.is_subscribed
            except AttributeError:
                return user.subscriber.filter(user_author=obj).exists()

        return False

    def create(self, validated_data):
        """Функция регистрации пользователя"""
        password = validated_data.pop('password')
        user = CustomUsers.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user

    def validate_password(self, value):
        """
        Проверка пароля на соответствие требованиям Django.
        """
        text_help = pw.password_validators_help_texts()

        if pw.validate_password(value) is None:
            return value
        raise ValidationError(f'{text_help}')


class GetTokenSerializer(serializers.Serializer):
    """Обработка запросов на получение токена"""

    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(max_length=150)

    def validate(self, data):
        """
        Проверка email и пароля
        """

        try:
            user = CustomUsers.objects.get(email=data['email'])
        except CustomUsers.DoesNotExist:
            raise serializers.ValidationError(
                'Пользователя с таким email не существует'
            )

        if user.check_password(data['password']):
            return data
        raise serializers.ValidationError(
            'Неверный пароль'
        )


class SubscriptionSerializer(UserSerializer):
    """Обработка запроса на подписку"""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUsers
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, obj):
        """Получение списка рецептов"""
        request = self.context.get('request')
        recipes_limit = None
        if request:
            recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit and recipes_limit.isdigit():
            recipes_limit = int(recipes_limit)
        queryset = obj.recipes.all()[:recipes_limit]
        serializer = RecipeUserSerializer(queryset, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        """Колличество рецептов"""
        rec_count = obj.recipes.all().count()
        return rec_count

    def get_validators(self):
        pass


class RecipeUserSerializer(serializers.ModelSerializer):
    """Получение списка рецептов"""

    class Meta:
        model = Recipe
        fields = ('id',
                  'name',
                  'image',
                  'cooking_time')
        read_only_fields = ('name',
                            'image',
                            'cooking_time')


class ChangePasswordSerializer(serializers.Serializer):
    """Обработка запроса изменения старого пароля"""

    new_password = serializers.CharField(min_length=8,
                                         max_length=150)
    current_password = serializers.CharField(max_length=150)

    class Meta:
        model = CustomUsers

    def validate_password(self, value):
        """Проверка старого пароля"""
        user = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError('Текущий пароль указан неверно')
        return value

    def update(self, instance, validated_data):
        """J,yjdktybt cnfhjuj gfhjkz"""
        instance.set_password(validated_data['new_password'])
        instance.save()

        return instance
