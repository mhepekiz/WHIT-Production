from rest_framework import serializers
from .models import Company, Function, WorkEnvironment, HowItWorksSection, HowItWorksStep, RecruiterSection


class FunctionSerializer(serializers.ModelSerializer):
    """Serializer for Function model."""
    
    class Meta:
        model = Function
        fields = ['id', 'name', 'color', 'text_color']


class CompanySerializer(serializers.ModelSerializer):
    """Serializer for Company model."""
    
    functions_list = serializers.SerializerMethodField()
    work_environment_list = serializers.SerializerMethodField()
    functions = FunctionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Company
        fields = [
            'id',
            'name',
            'logo',
            'jobs_page_url',
            'company_reviews',
            'country',
            'state',
            'city',
            'work_environment',
            'work_environment_list',
            'functions',
            'functions_list',
            'engineering_positions',
            'status',
            'is_sponsored',
            'sponsor_order',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'status', 'is_sponsored', 'sponsor_order', 'created_at', 'updated_at']
    
    def get_functions_list(self, obj):
        return obj.get_functions_list()
    
    def get_work_environment_list(self, obj):
        return obj.get_work_environment_list()


class CompanyListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for company lists."""
    
    functions = FunctionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Company
        fields = [
            'id',
            'name',
            'logo',
            'jobs_page_url',
            'company_reviews',
            'country',
            'city',
            'state',
            'work_environment',
            'functions',
            'engineering_positions',
            'status',
            'is_sponsored',
            'sponsor_order',
        ]


class WorkEnvironmentSerializer(serializers.ModelSerializer):
    """Serializer for WorkEnvironment model."""
    
    class Meta:
        model = WorkEnvironment
        fields = ['id', 'name']


class HowItWorksStepSerializer(serializers.ModelSerializer):
    """Serializer for HowItWorksStep model."""
    
    class Meta:
        model = HowItWorksStep
        fields = ['id', 'step_number', 'icon', 'title', 'description', 'is_active', 'order']


class HowItWorksSectionSerializer(serializers.ModelSerializer):
    """Serializer for HowItWorksSection model."""
    
    steps = HowItWorksStepSerializer(many=True, read_only=True)
    
    class Meta:
        model = HowItWorksSection
        fields = [
            'id', 'title', 'subtitle', 'section_header', 'description',
            'is_active', 'order', 'steps'
        ]


class RecruiterSectionSerializer(serializers.ModelSerializer):
    """Serializer for RecruiterSection model."""
    
    class Meta:
        model = RecruiterSection
        fields = [
            'id', 'title', 'description', 'button_text', 'button_link',
            'is_active', 'order', 'background_color', 'text_color', 'button_color'
        ]
