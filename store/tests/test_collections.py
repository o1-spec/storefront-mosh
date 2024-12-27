from rest_framework.test import APIClient
from rest_framework import status
import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from store.models import Collection, Product

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection

@pytest.mark.django_db
class TestCreateCollection:
    # @pytest.mark.skip
    def test_if_user_is_anonymous_returns_401(self, api_client, create_collection):
        #AAA(Arrange,Act,Assert)
        #Arrange
        
        #Act
        # client = APIClient()
        response = create_collection( {'title': 'a'})
        #Assert, here we check to see if the behaviour we expect happens or not
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_if_user_is_not_admin_returns_403(self,api_client, create_collection, authenticate):
        # client = APIClient()
        authenticate(is_staff=False)
        response = create_collection({'title': 'a'})
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_if_data_is_invalid_returns_400(self, api_client, create_collection, authenticate):
        # client = APIClient()
        authenticate(is_staff=True)
        response =  create_collection({'title': ''})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
        
    def test_if_data_is_valid_return_201(self, api_client, create_collection, authenticate):
        #client = APIClient()
        authenticate(is_staff=True)
        response = create_collection({'title': 'a'})
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
        
#This test should not be dependent of the other collection test unless it will fail if there is no collection in the database
#Two option is to use the api client, the only error is if there is a bug the line will fail
#Other option is to use the collection model
@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_returns_200(self,api_client):
        #Arrange
        # Collection.objects.create(title='a')
        # baker.make(Product, _quantity=10)
        collection = baker.make(Collection)
        
        response = api_client.get(f'/store/collections/{collection.id}')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'products_count' : 0
        }