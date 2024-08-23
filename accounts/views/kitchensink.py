from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from  .datacube_services import DatacubeServices
# from .utils import PayloadValidationServices, createCollectionSchema
from accounts.serializer import CreateCollectionSerializer, CheckDatabaseStatusSerializer


class CreateCollectionView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CreateCollectionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Invalid payload',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        workspace_id = validated_data['workspaceId']
        collection_name = validated_data['collectionName']
        api_key = request.headers.get('Authorization')

        if not api_key or not api_key.startswith('Bearer '):
            return Response({
                'success': False,
                'message': 'You are not authorized to access this resource'
            }, status=status.HTTP_401_UNAUTHORIZED)

        api_key = api_key.split(' ')[1]
        datacube = DatacubeServices(api_key)
        response = datacube.create_collection(f'{workspace_id}_dowell_survey_database', collection_name)

        if not response['success']:
            return Response({
                'success': False,
                'message': 'Failed to create collection, kindly contact the administrator',
                'response': response['data']
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'success': True,
            'message': 'Collection created successfully'
        }, status=status.HTTP_201_CREATED)


class CheckDatabaseStatusView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = CheckDatabaseStatusSerializer(data=request.query_params)

        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Invalid payload',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        workspace_id = validated_data['workspaceId']
        api_key = request.headers.get('Authorization')

        if not api_key or not api_key.startswith('Bearer '):
            return Response({
                'success': False,
                'message': 'You are not authorized to access this resource'
            }, status=status.HTTP_401_UNAUTHORIZED)

        api_key = api_key.split(' ')[1]
        datacube = DatacubeServices(api_key)

        try:
            response = datacube.collection_retrieval(f'{workspace_id}_dowell_survey_database')

            if not response['success']:
                return Response({
                    'success': False,
                    'message': 'Database is not yet ready, kindly contact the administrator',
                    'response': {
                        'databaseName': f'{workspace_id}_dowell_survey_database',
                        'collectionNames': [
                            f'{workspace_id}_dowell_survey_collection',
                        ]
                    }
                }, status=status.HTTP_501_NOT_IMPLEMENTED)

            list_of_meta_data_collections = [
                f'{workspace_id}_dowell_survey_list_collection',
            ]

            missing_collections = [col for col in list_of_meta_data_collections if col not in response['data'][0]]

            if missing_collections:
                missing_collections_str = ', '.join(missing_collections)
                return Response({
                    'success': False,
                    'message': f'The following collections are missing: {missing_collections_str}',
                    'response': missing_collections
                }, status=status.HTTP_404_NOT_FOUND)

            return Response({
                'success': True,
                'message': 'Excel the power of DoWell QR Code Generator'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'An error occurred: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)