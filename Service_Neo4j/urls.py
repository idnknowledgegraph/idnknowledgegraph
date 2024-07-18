from . import views
from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from Service_Neo4j.views import CompositeNarrativeView
from Service_Neo4j import views

router = DefaultRouter()
router.register(r'characters', views.CharacterViewSet, basename='characters')
router.register(r'events', views.EventViewSet, basename='event')
router.register(r'actions', views.ActionViewSet, basename='action')
router.register(r'choices', views.ChoiceViewSet, basename='choice')
router.register(r'outcomes', views.OutcomeViewSet, basename='outcome')
router.register(r'story-arcs', views.StoryArcViewSet, basename='story-arc')
router.register(r'character-relationships', views.CharacterRelationshipViewSet, basename='character-relationship')
router.register(r'character-plots', views.CharacterPlotViewSet, basename='character-plot')
router.register(r'decision-points', views.DecisionPointViewSet, basename='decision-point')
router.register(r'narrative-changes', views.NarrativeChangeViewSet, basename='narrative-change')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/composite-narrative/', CompositeNarrativeView.as_view(), name='composite-narrative'),
]   