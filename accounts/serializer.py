# serializers.py

from rest_framework import serializers

class CreateCollectionSerializer(serializers.Serializer):
    workspaceId = serializers.CharField(required=True)
    collectionName = serializers.CharField(required=True)


class CheckDatabaseStatusSerializer(serializers.Serializer):
    workspaceId = serializers.CharField(required=True)
