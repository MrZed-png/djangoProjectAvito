import pytest
from rest_framework import status
from ads.serializers import AdsListSerializer
from tests.factories import AdFactory


@pytest.mark.django_db
def test_ad_list(client):
    ad_list = AdFactory.create_batch(4)

    response = client.get(f"/ads/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "count": 4,
        "next": None,
        "previous": None,
        "results": AdsListSerializer(ad_list, many=True).data
    }