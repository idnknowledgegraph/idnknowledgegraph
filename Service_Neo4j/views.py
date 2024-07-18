from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Character, Event, Action, Choice, Outcome, StoryArc, CharacterRelationship, CharacterPlot, DecisionPoint, NarrativeChange
from .serializers import CharacterSerializer, EventSerializer, ActionSerializer, ChoiceSerializer, OutcomeSerializer, StoryArcSerializer, CharacterRelationshipSerializer, CharacterPlotSerializer, DecisionPointSerializer, NarrativeChangeSerializer
from rest_framework.views import APIView

class GenericNodeViewSet(viewsets.ViewSet):
    """
    Generic ViewSet for CRUD operations on neomodel entities.
    """
    def list(self, request):
        nodes = self.model.nodes.all()
        serializer = self.serializer_class(nodes, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            node = self.model.nodes.get(id=pk)
            serializer = self.serializer_class(node)
            return Response(serializer.data)
        except self.model.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            node = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            node = self.model.nodes.get(id=pk)
            serializer = self.serializer_class(node, data=request.data, partial=True)
            if serializer.is_valid():
                node = serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except self.model.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            node = self.model.nodes.get(id=pk)
            node.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except self.model.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class CharacterViewSet(GenericNodeViewSet):
    model = Character
    serializer_class = CharacterSerializer

class EventViewSet(GenericNodeViewSet):
    model = Event
    serializer_class = EventSerializer

class ActionViewSet(GenericNodeViewSet):
    model = Action
    serializer_class = ActionSerializer

class ChoiceViewSet(GenericNodeViewSet):
    model = Choice
    serializer_class = ChoiceSerializer

class OutcomeViewSet(GenericNodeViewSet):
    model = Outcome
    serializer_class = OutcomeSerializer

class StoryArcViewSet(GenericNodeViewSet):
    model = StoryArc
    serializer_class = StoryArcSerializer

class CharacterRelationshipViewSet(GenericNodeViewSet):
    model = CharacterRelationship
    serializer_class = Character

class CharacterPlotViewSet(GenericNodeViewSet):
    model = CharacterPlot
    serializer_class = CharacterPlotSerializer

class DecisionPointViewSet(GenericNodeViewSet):
    model = DecisionPoint
    serializer_class = DecisionPointSerializer

class NarrativeChangeViewSet(GenericNodeViewSet):
    model = NarrativeChange
    serializer_class = NarrativeChangeSerializer

""" class CompositeNarrativeView(APIView):
    def post(self, request):
        data = request.data
        characters = data.get('characters', [])
        events = data.get('events', [])
        participations = data.get('participations', [])

        # Create characters
        character_objects = []
        for char_data in characters:
            serializer = CharacterSerializer(data=char_data)
            if serializer.is_valid():
                char_obj = serializer.save()
                character_objects.append(char_obj)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create events
        event_objects = []
        for event_data in events:
            serializer = EventSerializer(data=event_data)
            if serializer.is_valid():
                event_obj = serializer.save()
                event_objects.append(event_obj)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Handle participations
        for participation in participations:
            character = character_objects[participation['character_index']]
            event = event_objects[participation['event_index']]
            character.participates_in.connect(event)

        return Response({"status": "Composite narrative created"}, status=status.HTTP_201_CREATED) """

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (CharacterSerializer, EventSerializer, StoryArcSerializer,
                          ActionSerializer, CharacterRelationshipSerializer,
                          NarrativeChangeSerializer, DecisionPointSerializer,
                          ChoiceSerializer, OutcomeSerializer, CharacterPlotSerializer)

class CompositeNarrativeView(APIView):
    def post(self, request):
        data = request.data

        # Create entities and store references in dictionaries
        story_arcs, _ = self.create_entities(StoryArcSerializer, data.get('story_arcs', []))
        characters, _ = self.create_entities(CharacterSerializer, data.get('characters', []))
        events, _ = self.create_entities(EventSerializer, data.get('events', []))
        decision_points, _ = self.create_entities(DecisionPointSerializer, data.get('decision_points', []))
        choices, _ = self.create_entities(ChoiceSerializer, data.get('choices', []))
        outcomes, _ = self.create_entities(OutcomeSerializer, data.get('outcomes', []))
        actions, _ = self.create_entities(ActionSerializer, data.get('actions', []))
        narrative_changes, _ = self.create_entities(NarrativeChangeSerializer, data.get('narrative_changes', []))
        character_plots, _ = self.create_entities(CharacterPlotSerializer, data.get('character_plots', []))

        # Establish relationships between characters and events
        for participation in data.get('participations', []):
            character = characters.get(participation['character_name'])
            event = events.get(participation['event_name'])
            if character and event:
                character.participates_in.connect(event)

        #Establish relationships between characters
        for relationship in data.get('character_relationships', []):
            # Assuming you're receiving character names and relationship type in the request
            character1 = characters.get(relationship['character1'])
            character2 = characters.get(relationship['character2'])
            relationship_type = relationship['type']
            if character1 and character2:
                        # Retrieve or create the CharacterRelationship node
                    relationship = CharacterRelationship.get_or_create({'type': relationship_type})
                    character_relationship = CharacterRelationship.get(character1, relationship)
                    character1.has_relationship_with.connect(character_relationship, character2)

        return Response({"status": "Narrative created successfully"}, status=status.HTTP_201_CREATED)

    def create_entities(self, serializer_class, entities_data):
        objects = {}
        errors = []
        for entity_data in entities_data:
            serializer = serializer_class(data=entity_data)
            if serializer.is_valid():
                obj = serializer.save()
                objects[entity_data['name']] = obj  # Storing objects by name for linking
            else:
                errors.append(serializer.errors)
        return objects, errors
    
    def connect_characters_with_relationship(character1, character2, relationship_type):
        # Retrieve or create the CharacterRelationship node
        relationship, _ = CharacterRelationship.get_or_create({'type': relationship_type})
        character1.has_relationship_with.connect(character2, {'relationship': relationship})
        character2.has_relationship_with.connect(character1, {'relationship': relationship})
