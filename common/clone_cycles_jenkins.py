from common.JiraLibrary import JiraAPI
from requests.packages import urllib3
from argparse import ArgumentParser


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


parser = ArgumentParser()
parser.add_argument("--sourceFolder", help="Source folder name")
parser.add_argument("--sourceCycle", help="Source Cycle Name")
parser.add_argument("--destFolder", help="Destination folder name")
parser.add_argument("--destCycle", help="Destination Cycle Name")

args = parser.parse_args()


if __name__ == "__main__":
    jira = JiraAPI()
    try:
        jira.clone_cycle_tune(source_release_folder_name=args.sourceFolder,
                              source_cycle_name=args.sourceCycle,
                              destination_release_folder_name=args.destFolder,
                              destination_cycle_name=args.destCycle)
    except Exception as e:
        print(f"Exception: {repr(e)}")

