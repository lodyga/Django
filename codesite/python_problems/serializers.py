from rest_framework import serializers
from .models import Tag, Difficulty, Complexity, Language, Problem, Solution


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class DifficultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Difficulty
        fields = '__all__'


class ComplexitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Complexity
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'


class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = '__all__'
