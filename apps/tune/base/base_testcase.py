from apps.tune.TuneElectron import TuneElectron
from base.base_ui import UIBase


class TuneBaseTestCase(UIBase):

    tune_app = None
    calendar_methods = None
    desk_booking = None
    scenario_class = None
    scenario = None

    @classmethod
    def setUpClass(cls, *args, **kwargs) -> None:
        cls.tune_app = TuneElectron()
        cls.tune_app.connect_tune_app()
        cls.tune_app.driver.implicitly_wait(0)
        for kwarg, value in kwargs.items():
            if kwarg == 'scenario_class':
                cls.scenario = value(cls.tune_app.driver)
                kwargs.pop(kwarg)
                break
        super().setUpClass(*args, **kwargs)
        cls.tune_app.driver.implicitly_wait(0)
        if cls.scenario is None:
            raise AttributeError('scenario_class not defined!')
