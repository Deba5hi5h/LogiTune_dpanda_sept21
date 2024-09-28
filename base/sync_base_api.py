"""
:Module Name: **SyncBaseAPI**

===============================

SyncBaseAPI class.
"""
import logging
from base.base import Base
from base import global_variables

from apis.sync_api.productrequest import ProductRequest
from apis.sync_api.websocketconnection import WebsocketConnection
from apis.sync_helper import SyncHelper
import asyncio
import apis.process_helper as process_helper

log = logging.getLogger(__name__)


class SyncBaseAPI(Base):
    product_uuid = {}

    @classmethod
    def setUpClass(cls):
        """
        Setup Class for Sync Base.
        """
        try:
            if global_variables.setupFlag:
                super(SyncBaseAPI, cls).setUpClass()

            cls.sync = SyncHelper()
            cls.loop = asyncio.get_event_loop()
            if not process_helper.check_sync_service_status():
                log.error('Please start the sync service to execute test-suite')
                raise AssertionError('Sync Service not running')

            product_request = ProductRequest()
            # Generate the request message
            websocket_dict = {'type': 'LogiSync', 'timeout': 30.0}
            websocket_dict['msg_buffer'] = product_request.create_product_request()
            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(websocket_dict)
            # Get the response
            product_data = cls.loop.run_until_complete(websocket_con.request_response_listener())
            # Update UUID for all devices
            products = product_data['response']['productResponse']['getAllProductsResponse']
            if len(products):
                for item in products['products']:
                    cls.product_uuid.update({item['model']: item['uuid']})

        except Exception as e:
            logging.error('Error: {}'.format(e))
            raise e

    @classmethod
    def tearDownClass(cls) -> None:
        super(SyncBaseAPI, cls).tearDownClass()

    def setUp(self) -> None:
        Base.setUp(self)

    def tearDown(self) -> None:
        Base.tearDown(self)
