from rest_framework import serializers
from .models import Character, Event, Action, Choice, Outcome, StoryArc, CharacterRelationship, CharacterPlot, DecisionPoint, NarrativeChange

class BaseNeoModelSerializer(serializers.Serializer):
    uid = serializers.UUIDField(read_only=True)

    def create(self, validated_data):
        return self.Meta.model(**validated_data).save()

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

class CharacterSerializer(BaseNeoModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Character

class EventSerializer(BaseNeoModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Event

class ActionSerializer(BaseNeoModelSerializer):
    description = serializers.CharField()

    class Meta:
        model = Action

class ChoiceSerializer(BaseNeoModelSerializer):
    description = serializers.CharField()

    class Meta:
        model = Choice

class OutcomeSerializer(BaseNeoModelSerializer):
    result_description = serializers.CharField()

    class Meta:
        model = Outcome

class StoryArcSerializer(BaseNeoModelSerializer):
    title = serializers.CharField()

    class Meta:
        model = StoryArc

class CharacterRelationshipSerializer(BaseNeoModelSerializer):
    type = serializers.CharField()

    class Meta:
        model = CharacterRelationship

class CharacterPlotSerializer(BaseNeoModelSerializer):
    plot_description = serializers.CharField()

    class Meta:
        model = CharacterPlot

class DecisionPointSerializer(BaseNeoModelSerializer):
    description = serializers.CharField()

    class Meta:
        model = DecisionPoint

class NarrativeChangeSerializer(BaseNeoModelSerializer):
    change_description = serializers.CharField()

    class Meta:
        model = NarrativeChange
