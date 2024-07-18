from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, StructuredRel

class Character(StructuredNode):
    name = StringProperty(required=True)
    participates_in = RelationshipTo('Event', 'PARTICIPATES_IN')
    performs_action = RelationshipTo('Action', 'PERFORMS_ACTION')
    has_relationship_with = RelationshipTo('CharacterRelationship', 'HAS_RELATIONSHIP_WITH')

class Event(StructuredNode):
    name = StringProperty(required=True)
    characters = RelationshipFrom(Character, 'PARTICIPATES_IN')
    part_of_story_arc = RelationshipTo('StoryArc', 'PART_OF_STORY_ARC')

class DecisionPoint(StructuredNode):
    description = StringProperty(required=True)
    part_of_plot = RelationshipTo('CharacterPlot', 'PART_OF_PLOT')

class Action(StructuredNode):
    description = StringProperty(required=True)
    leads_to_narrative_change = RelationshipTo('NarrativeChange', 'LEADS_TO_NARRATIVE_CHANGE')
    performed_by = RelationshipFrom(Character, 'PERFORMS_ACTION')

class Choice(StructuredNode):
    description = StringProperty(required=True)
    leads_to_outcome = RelationshipTo('Outcome', 'LEADS_TO_OUTCOME')

class Outcome(StructuredNode):
    result_description = StringProperty(required=True)
    from_choice = RelationshipFrom(Choice, 'LEADS_TO_OUTCOME')

class StoryArc(StructuredNode):
    title = StringProperty(required=True)
    events = RelationshipFrom(Event, 'PART_OF_STORY_ARC')

class CharacterRelationship(StructuredNode):
    type = StringProperty(required=True)
    between_characters = RelationshipFrom(Character, 'HAS_RELATIONSHIP_WITH')

class CharacterPlot(StructuredNode):
    plot_description = StringProperty(required=True)
    involves_decision_points = RelationshipFrom(DecisionPoint, 'PART_OF_PLOT')

class NarrativeChange(StructuredNode):
    change_description = StringProperty(required=True)
    initiated_by_action = RelationshipFrom(Action, 'LEADS_TO_NARRATIVE_CHANGE')

