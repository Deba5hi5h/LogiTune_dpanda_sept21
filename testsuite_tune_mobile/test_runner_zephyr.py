import argparse
from apps.tune_mobile.config import tune_mobile_config
from common.JiraLibrary import JiraAPI

parser = argparse.ArgumentParser()
parser.add_argument("-qv", "--qa_version", help="QA version of App to be tested")
parser.add_argument("-up", "--user_phone", help="User phone for running tests")
args = parser.parse_args()

qa_version = args.qa_version
tune_mobile_config.phone = args.user_phone

from base.base_mobile import MobileBase
platform_version = MobileBase.get_platform_version()
platform_name = MobileBase.get_platform_name()
folder = qa_version.split("-")[0]
destination_folder = f"Tune-Mobile-{folder}x"
destination_cycle = f"TuneMobile {qa_version} {platform_name} {platform_version} Auto"
jiraApi = JiraAPI()
try:
    jiraApi.clone_cycle_tune(source_release_folder_name="Tune-Mobile-Auto-Template",
                             source_cycle_name="TuneMobile Auto Template",
                             destination_release_folder_name=destination_folder,
                             destination_cycle_name=destination_cycle)
except Exception as e:
    print(e)