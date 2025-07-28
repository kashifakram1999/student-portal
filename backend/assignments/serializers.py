from rest_framework import serializers
from .models import Assignment, Submission

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'
        read_only_fields = ['created_by']

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ['student', 'submitted_at']
