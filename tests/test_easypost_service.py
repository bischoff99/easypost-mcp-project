from unittest.mock import MagicMock, patch

from src.services.easypost_service import EasyPostService


def test_get_shipments_list_sync_includes_before_id() -> None:
    fake_key = "EZAK" + ("0" * 20)
    with patch("src.services.easypost_service.easypost.EasyPostClient") as mock_client_cls:
        mock_client = MagicMock()
        mock_client.shipment.all.return_value = MagicMock(shipments=[])
        mock_client_cls.return_value = mock_client

        service = EasyPostService(fake_key)

        before_id = "shp_123"
        service._get_shipments_list_sync(5, True, None, None, before_id)

        mock_client.shipment.all.assert_called_once_with(
            page_size=5, purchased=True, before_id=before_id
        )
