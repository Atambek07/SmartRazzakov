from rest_framework import serializers
from ...infrastructure.models import UserProfileModel, UserRole
from ..serializers.content_serializers import CourseSerializer

class UserRoleField(serializers.Field):
    def to_representation(self, value):
        return UserRole(value).name.lower()

    def to_internal_value(self, data):
        try:
            return UserRole[data.upper()].value
        except KeyError:
            raise serializers.ValidationError("Invalid user role")

class UserProfileSerializer(serializers.ModelSerializer):
    role = UserRoleField()
    enrolled_courses = CourseSerializer(many=True, read_only=True)
    authored_content = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        pk_field=serializers.UUIDField()
    )

    class Meta:
        model = UserProfileModel
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'grade_level',
            'subjects',
            'achievements',
            'enrolled_courses',
            'authored_content',
            'created_at'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'grade_level': {
                'min_value': 1,
                'max_value': 11,
                'required': False
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileModel
        fields = [
            'id',
            'first_name',
            'last_name',
            'role',
            'grade_level',
            'subjects'
        ]
        read_only_fields = fields