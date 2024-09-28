"""
:Module Name: **RaidenBaseAPI**

===============================

RaidenBaseAPI class.
"""
import logging
from common.aws_wrappers import SSMParameterStore
from base import global_variables
from base.base import Base
from config.aws_helper import AWSHelper

log = logging.getLogger(__name__)


class RaidenBaseAPI(Base):
    """
    Raiden Base Class
    """
    @classmethod
    def setUpClass(cls):
        """
        Initializing the raiden base
        """
        try:
            if global_variables.setupFlag:
                super(RaidenBaseAPI, cls).setUpClass()
            cls.env = global_variables.SYNC_ENV
            # variable - org_id & token is overridden by the roles classes
            cls.config = cls.org_id = cls.token = cls.email_id = None
            cls.config = AWSHelper.get_config(global_variables.SYNC_ENV)
            if cls.config is None:
                try:
                    aws_config_file = None
                    prefix = '/seam/raiden/' + cls.env + '/'
                    logging.info(f'Prefix is {prefix}')
                    cls.ssm_ps_wrapper = SSMParameterStore(
                        prefix=prefix, aws_config_file=aws_config_file)
                except Exception as e:
                    log.error(
                        'Unable to fetch SSM Credentials. Make sure AWS credentials are set properly')
                    raise e

                try:
                    cls.config = cls.ssm_ps_wrapper.get_parameter_value_as_struct(
                        'config')
                except Exception as e:
                    log.error('Exception while reading config: {}'.format(e))
                    raise e

        except Exception as e:
            logging.error('Error: {}'.format(e))
            raise e

    @classmethod
    def tearDownClass(cls) -> None:
        super(RaidenBaseAPI, cls).tearDownClass()

    def setUp(self) -> None:
        Base.setUp(self)

    def tearDown(self) -> None:
        Base.tearDown(self)
