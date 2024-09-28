
# Framework configuration:

### 1. Please use Python 3.7 or above and install the libraries in requirements.txt using:

`pip install -r requirements.txt`


### 2. Install Java JDK 8 (or higher) in the host computer.

- for Windows platform set `JAVA_HOME` in environmental variables

### 3. Configure AWS credentials

- [Instruction](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
- Ensure that `region = us-west-2` is present in `C:\Users\<login_name>\.aws\credentials`. If not, add it.
- After adding the environment variable, goto `Pycharm > File > Invalidate Caches`.

### 4. Windows WinAppDriver Configuration:
- Enable `Developer Mode` in Windows settings
- Turn Off User Account Control settings: [Link](https://knowledge.autodesk.com/support/autocad/learn-explore/caas/sfdcarticles/sfdcarticles/How-to-turn-off-User-Account-Control-in-Windows.html)

- Install x86 version of [Windows Application Driver](https://github.com/microsoft/WinAppDriver/releases/download/v1.2.99/WindowsApplicationDriver-1.2.99-win-x86.exe)  (even if you use 64-bit please use x86 version)

### 5. Hosts file configuration (for Jenkins setup):

For macOS, update hosts file
- Go->Go to Folder and search for `/private/etc/hosts`
- At the end of file, add `172.28.78.218 desktop-05v8uef`

If https://desktop-05v8uef is not accessible on Windows, you need to modify hosts file there as well
- Go to `C:\Windows\System32\drivers\etc\hosts`
- At the end of file, add `172.28.78.218 desktop-05v8uef`

### 6. LOCAL config creation

- Go to `common` folder
- Create `properties.LOCAL` file
- Copy all entries from `properties.TEMPLATE` to `properties.LOCAL`. Remember to update values in `properties.LOCAL` with unique uuids from your working station.
- `properties.LOCAL` is visible only to you and ignored by `.gitignore` rules
- When adding a new device to be supported in this framework please remember to update `properties.TEMPLATE `as well
- Update values in `properties.LOCAL` for device port numbers and USB Switch serial number in `SWITCH_PORT_MASTER`.

### 7. SYNC API tests

Mark the repositories:
- vc-cloud-apps-automation-e2e
- vc-cloud-apps-automation-e2e/apis/sync_api/library
- vc-cloud-apps-automation-e2e/apis/sync_api/library/protobuf/compiled/python

folders as source root.

### 8. Email Notification Configuration
Create below environment variables and provide the email id and password that will be used to send email
- JENKINS_EMAIL
- JENKINS_PASSWORD
- To send email at the start of execution, set email id of receipent in global_variables.email_to
- To send email at the end of execution, set global_variables.email_flag = True and set email id of receipent in global_variables.email_to
- To send email to multiple people, email id's should be separated by , in global_variables.email_to

### 9. Security & Privacy settings for running AppleScript through Terminal on MacOS

Due to running AppleScript (.scpt) via osascript in Terminal, it needs to update Security & Privacy settings.
Please add `PyCharm` to `System Preferences > Security & Privacy > Privacy > Accessibility` if running test via PyCharm.
(More info could be found here: https://apple.stackexchange.com/questions/291574/osascript-is-not-allowed-assistive-access-1728)
