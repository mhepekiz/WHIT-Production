from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, JobPreference
from companies.models import Function, WorkEnvironment
from companies.serializers import FunctionSerializer


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists."})
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        
        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Create associated profile and job preference
        UserProfile.objects.create(user=user)
        JobPreference.objects.create(user=user)
        
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model."""
    
    user = UserSerializer(read_only=True)
    resume_url = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user',
            'phone',
            'location',
            'bio',
            'current_title',
            'years_of_experience',
            'linkedin_url',
            'portfolio_url',
            'github_url',
            'resume',
            'resume_url',
            'resume_uploaded_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'resume_uploaded_at']
    
    def validate_phone(self, value):
        """Validate phone number format: +X (XXX) XXX-XXXX"""
        if value:
            import re
            phone_pattern = r'^\+\d{1,3}\s\(\d{3}\)\s\d{3}-\d{4}$'
            if not re.match(phone_pattern, value):
                raise serializers.ValidationError(
                    'Phone must be in format: +country code (area) xxx-xxxx (e.g., +1 (555) 123-4567)'
                )
        return value
    
    def get_resume_url(self, obj):
        if obj.resume:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.resume.url)
        return None


class JobPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for JobPreference model."""
    
    desired_functions = FunctionSerializer(many=True, read_only=True)
    desired_function_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Function.objects.all(),
        source='desired_functions',
        required=False
    )
    
    work_environment_names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = JobPreference
        fields = [
            'id',
            'desired_functions',
            'desired_function_ids',
            'work_environments',
            'work_environment_names',
            'employment_types',
            'preferred_locations',
            'willing_to_relocate',
            'remote_only',
            'minimum_salary',
            'industries',
            'company_size_preference',
            'email_notifications',
            'job_alerts',
            'actively_looking',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Convert work_environments from objects to name list
        representation['work_environments'] = [env.name for env in instance.work_environments.all()]
        return representation
    
    def update(self, instance, validated_data):
        work_env_names = validated_data.pop('work_environment_names', None)
        
        # Update other fields
        instance = super().update(instance, validated_data)
        
        # Handle work environments by name
        if work_env_names is not None:
            instance.work_environments.clear()
            for env_name in work_env_names:
                env, _ = WorkEnvironment.objects.get_or_create(name=env_name)
                instance.work_environments.add(env)
        
        return instance


class UserDashboardSerializer(serializers.Serializer):
    """Combined serializer for user dashboard."""
    
    user = UserSerializer()
    profile = UserProfileSerializer()
    job_preference = JobPreferenceSerializer()
