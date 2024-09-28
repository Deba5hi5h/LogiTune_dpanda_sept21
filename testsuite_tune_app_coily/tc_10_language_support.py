import shutil
import unittest
from functools import wraps

from apps.collabos.coily.tune_coily_config import GOOGLE, MICROSOFT
from base import global_variables

from base.base_coily import CoilyBase

languages = {'English': 'en_US',
             'French': 'fr_FR',
             'German': 'de_DE',
             'Italian': 'it_IT',
             'Portuguese': 'pt_BR',
             'Spanish': 'es_ES'}


def iterate_languages(test_method):
    @wraps(test_method)
    def wrapper(self):
        for lang_name, lang_value in languages.items():
            test_method(self, lang_name, lang_value)

    return wrapper


class LanguageSupport(CoilyBase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        shutil.copyfile(f"{CoilyBase.rootPath}/apps/collabos/coily/CoilyScreenshots.html",
                        f"{global_variables.reportPath}/CoilyScreenshots.html")

    @iterate_languages
    def test_10001_VC_XXXXXX_localization_main_page_idle(self, lang_name, lang_value):
        self.coily_test_methods.tc_localization_main_idle_page(lang_name=lang_name,
                                                               lang_value=lang_value)

    @iterate_languages
    def test_10002_VC_XXXXXX_localization_anonymous_walk_in_session(self, lang_name, lang_value):
        self.coily_test_methods.tc_localization_anonymous_walk_in_session(lang_name=lang_name,
                                                                          lang_value=lang_value)

    @iterate_languages
    def test_10003_VC_XXXXXX_localization_identified_walk_in_session(self, lang_name, lang_value):
        self.coily_test_methods.tc_localization_identified_walk_in_session(lang_name=lang_name,
                                                                           lang_value=lang_value,
                                                                           account_type=GOOGLE)

    @iterate_languages
    def test_10004_VC_XXXXXX_localization_booked_session(self, lang_name, lang_value):
        self.coily_test_methods.tc_localization_booked_session(lang_name=lang_name,
                                                               lang_value=lang_value,
                                                               account_type=GOOGLE,
                                                               wrong_account_type=MICROSOFT)

    @iterate_languages
    def test_10005_VC_XXXXXX_localization_early_check_in(self, lang_name, lang_value):
        self.coily_test_methods.tc_localization_early_check_in(lang_name=lang_name,
                                                               lang_value=lang_value,
                                                               correct_user_account_type=GOOGLE,
                                                               correct_user=self.google_credentials,
                                                               wrong_user_account_type=None,
                                                               wrong_user='anonymous',
                                                               reservation_delay=3)

    @iterate_languages
    def test_10006_VC_XXXXXX_localization_different_kind_of_booked_sessions(self, lang_name, lang_value):
        self.coily_test_methods.tc_localization_different_kind_of_booked_sessions(lang_name=lang_name,
                                                                                  lang_value=lang_value,
                                                                                  account_type=GOOGLE)

    @iterate_languages
    def test_10007_VC_XXXXXX_localization_desk_conflict(self, lang_name, lang_value):
        self.coily_test_methods.tc_localization_desk_conflict(lang_name=lang_name,
                                                              lang_value=lang_value,
                                                              account_type=GOOGLE,
                                                              desk_id="dWnRfZ7SYwyF3wbICDcc2JsX8rcoEn0X-hmnvxop0d99wzrwdiEbIFFkvQuBU6NN8")

    @iterate_languages
    def test_10008_VC_XXXXXX_localization_initialisation_screen(self, lang_name, lang_value):
        self.coily_test_methods.tc_localization_initialisation_screen(lang_name=lang_name,
                                                                      lang_value=lang_value)

if __name__ == "__main__":
    unittest.main()
