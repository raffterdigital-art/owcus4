from rest_framework import serializers
from .models import School, StudentProfile, SchoolPost, StudentChat

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'

class SchoolPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolPost
        fields = '__all__'

class StudentChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentChat
        fields = '__all__'