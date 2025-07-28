from rest_framework import serializers
from .models import Assignment, Submission
import os

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

    def validate_file(self, value):
        # 1. Check file extension
        ext = os.path.splitext(value.name)[1].lower()
        valid_extensions = ['.pdf', '.docx', '.zip']
        if ext not in valid_extensions:
            raise serializers.ValidationError('Unsupported file type.')

        # 2. Check file size (e.g., max 5 MB)
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError('File size exceeds 5MB.')

        return value
