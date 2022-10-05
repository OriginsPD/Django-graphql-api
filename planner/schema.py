import graphene
from graphene_django import DjangoObjectType
from planner.models import *


class EventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = '__all__'


class PlanType(DjangoObjectType):
    class Meta:
        model = Plan
        fields = '__all__'

# Queries


class Query(graphene.ObjectType):
    all_events = graphene.List(EventType)
    all_plans = graphene.List(PlanType)

    def resolve_all_events(root, info):
        return Event.objects.select_related('event').all()

    def resolve_all_plans(root, info):
        return Plan.objects.all()


# Schema

schema = graphene.Schema(query=Query)
