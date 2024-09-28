from common.JiraLibrary import JiraAPI
from requests.packages import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logi_tune_version = '3.5.249'
release_version = '3.5.x'
coily_version = "1.12.130"

OS_PLATFORMS = ["Mac11-Apple M1",
                "Mac13-Apple M1",
                "Mac14-Apple M2",
                "Win10-AMD",
                "Win11-Intel 12th",
                "Win11-Intel 13th"]


class LogiTuneGeneralRegressionTestsData:
    source_release_folder_name = "Tune-Desktop-Automation-Template"
    source_cycle_name = "LogiTune-RegressionUI-Automation-Template"
    destination_release_folder_name = f"Tune-{release_version}-Automated-Regular"
    destination_cycles = [f"LogiTune-{logi_tune_version}-{platform}-Automation" for platform in OS_PLATFORMS]


class LogiTuneFWUStressTestsData:
    source_release_folder_name = "Tune-Desktop-Template"
    source_cycle_name = "LogiTune-FWUpdateStress-Automation-Template"
    destination_release_folder_name = f"Tune-{release_version}-Automated-Stress"
    destination_cycles = [f"{logi_tune_version}-FWUpdateStress-{platform}-Auto" for platform in OS_PLATFORMS]


class LogiTuneCoilyTestsData:
    source_release_folder_name = "Tune-Desktop-Automation-Template"
    source_cycle_name = "LogiTune-CoilyAuthentication-Automation-Template"
    destination_release_folder_name = f"Tune-{release_version}-Coily-1.12.x-Automated"
    destination_cycles = [f"LogiTune-{logi_tune_version}-Coily-{coily_version}-{platform}-Automation" for platform in OS_PLATFORMS]


def clone_tune_cycles(logi_tune_cycles):
    jira = JiraAPI()
    for cycle_name in logi_tune_cycles.destination_cycles:
        try:
            jira.clone_cycle_tune(source_release_folder_name=logi_tune_cycles.source_release_folder_name,
                                  source_cycle_name=logi_tune_cycles.source_cycle_name,
                                  destination_release_folder_name=logi_tune_cycles.destination_release_folder_name,
                                  destination_cycle_name=cycle_name)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    clone_tune_cycles(LogiTuneCoilyTestsData)
