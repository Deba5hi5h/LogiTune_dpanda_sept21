
# Framework configuration:

### 0. Download and install Python 3.12.2 (https://www.python.org/downloads/release/python-3122/)

### 1. Please use Python 3.12 or above and install the libraries in requirements_312.txt using:

`pip install -r requirements_312.txt`


### 2. Install Java JDK 8 (or higher) in the host computer.

- for Windows platform set `JAVA_HOME` in environmental variables
- for MacOS with Python 3.12 (if there is an issue with old Java):
  - delete previous java with: `sudo rm -rf /Library/Java/JavaVirtualMachines/jdk1.8.0_281.jdk`
  - install with brew: `brew install java` and run commands:
    - `sudo ln -sfn /opt/homebrew/opt/openjdk/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk.jdk`
    - `echo 'export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"' >> ~/.zshrc`
    - For Jenkins machines run: `brew unlink python`
  

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

### 6. For .pkg installation and services loading/unloading on macOS please do:

- open Terminal
- type: `sudo visudo` and enter root password
  - go to the very end of edited file at type: 
    - `macos_user_name ALL = NOPASSWD: /usr/sbin/installer` 
    - `macos_user_name ALL = NOPASSWD: /bin/launchctl`
    - `macos_user_name ALL = NOPASSWD: /bin/rm`
    - `macos_user_name ALL = NOPASSWD: /Library/LogiSyncPersonalCollab/uninstall.sh`

  - i.e.: 
    - `pawellesniak ALL = NOPASSWD: /usr/sbin/installer`
    - `pawellesniak ALL = NOPASSWD: /bin/launchctl`
    - `pawellesniak ALL = NOPASSWD: /bin/rm`
    - `pawellesniak ALL = NOPASSWD: /Library/LogiSyncPersonalCollab/uninstall.sh`

- save changes and close file


### 7. LOCAL config creation

- Go to `common` folder
- Create `properties.LOCAL` file
- Copy all entries from `properties.TEMPLATE` to `properties.LOCAL`. Remember to update values in `properties.LOCAL` with unique uuids from your working station.
- `properties.LOCAL` is visible only to you and ignored by `.gitignore` rules
- When adding a new device to be supported in this framework please remember to update `properties.TEMPLATE `as well
- Update values in `properties.LOCAL` for device port numbers and USB Switch serial number in `SWITCH_PORT_MASTER`.


### 8. Creation of device_parameters.py file for stress firmware update tests

- Go to `testsuite_tune_app -> update_easteregg` folder
- Copy `device_parameters.TEMPLATE` file
- Paste it to the same folder with changed extension (`device_parameters.TEMPLATE -> device_parameters.py`)
- Complete each device with base and target FW version

### 9. Security & Privacy settings for Screen Recording on MacOS

Due to automated Logi Tune recordings (for debugging reasons) there is a need for update Security & Privacy settings
of Screen Recording. Just allow your IDE to be able to record contents of the screen in your Macbook settings (e.g. PyCharm as it's shown on below image)

<img width="783" alt="image" src="https://user-images.githubusercontent.com/97097750/181743614-d5049d83-486c-424d-a083-804b1225f6b3.png">

### 10. Creation of api_parameters.py file for Firmware API tests (needed only for those tests)

- Go to `testsuite_firmware_api_tests \ api_tests` folder
- Copy `api_parameters.TEMPLATE` file
- Paste it to the same folder with changed extension (`api_parameters.TEMPLATE -> api_parameters.py`)
- Complete `local_api_pc_configuration` and necessary data for tested device
- How to get COMPort numbers?
  * Windows 10 -> Get COM Port from Bluetooth properites for Zone True Wireless 'GAIA'
  * on MacOS -> search for GAIA port by printing available ports `ls /dev/tty.*`

### 11. LogiTune Calendar

# Add to existing project

Credentials for below admin account for adding new emails: [Click here](https://drive.google.com/file/d/1I3ieX-yFmxx_jaMiSsGdNq-MCOM_0oe4/view?usp=drive_link)
- Login to Google Cloud Console (https://console.cloud.google.com/getting-started)
- On the left pane, click APIs and services -> OAuth consent screen
- Click `+ ADD USERS` button in Test users section, add new google emails and hit `SAVE` button
- Download `credentials.json` [(Click here)](https://drive.google.com/file/d/1ZfBYywSLgK6gJc4-vPJZWi9eHDNHaW7S/view?usp=sharing) file and paste it to `vc-cloud-apps-automation-e2e\apps\tune`

# Create new project 

Create google test account. Provide email and password in properties.LOCAL
- GOOGLE_ACCOUNT (email id)
- GOOGLE_PASSWORD

After account creation, change its language to english - https://support.google.com/accounts/answer/32047?hl=en&co=GENIE.Platform%3DDesktop 

On Test Machine, login to created Google account using Chrome browser. Make chrome as default browser.

Tutorial with images: https://drive.google.com/file/d/1nyeNaHQFGgqpyDeWN75XpbOnvlaaMoPm/view

Create Google cloud project using the above email and password
- Open the Google Cloud Console - https://console.cloud.google.com/getting-started
- At the top-left, click Menu menu > IAM & Admin > Create a Project.
- In the Project Name field, enter a descriptive name for your project.
- In the Location field, click Browse to display potential locations for your project. Then, click Select. If no location, leave blank
- Click Create.

Enable Calendar API
- Open the Google Cloud Console - https://console.cloud.google.com/getting-started
- At the top-left, click Menu menu > APIs & Services > Library.
- Search for Calendar API and enable

Create oAuth client
- Open the Google Cloud Console - https://console.cloud.google.com/getting-started
- At the top-left, click Menu menu > APIs & Services > OAuth consent screen.
- Enter app name, email and continue
- Click Add scope and search for https://www.googleapis.com/auth/calendar, then add to table and update. Save and continue.
- Add test users by their emails.
- Click Credentials > Create Credentials > OAuth client ID.
- Click Application type > Desktop app. Enter name and click Create.
- Download the JSON and save the file as credentials.json under `vc-cloud-apps-automation-e2e\apps\tune` folder

### 12. LogiTune Easter Egg firmware update

To be able to run Easter Egg update, create tune-feature.cfg file
- Create tune-feature.cfg file with following content:
  ```
  local_update_enabled=true
  detailed_logging_enabled=true
  ```
- Place it
  - for Windows in `C:\Program Files` and `C:\Program Files (x86)`
  - for MacOS in `/Aplications`
  
### 13. Bluetooth and audio tests - Configuration

Install Bluetooth tools
- For Windows, install Bluetooth Command Line Tools - https://bluetoothinstaller.com/bluetooth-command-line-tools
- For MacOS, install blueutil - https://github.com/toy/blueutil
- Both tools are a suite of command line utilities that can be used to configure your bluetooth adapter and discover remote bluetooth devices and services.

Install switchaudio-osx tools
- For MacOS, install switchaudio-osx to switch audio input/output devices through command line. - https://github.com/deweller/switchaudio-osx
- The command line tool is used to run tests which may need to switch/select audio input/output to specific resource
- For example, "test_1404_VC_74126_mic_level_zone_900" will have to get system input level. Thus, it requires to select audio input as DUT to avoid getting wrong system input level (like the built-in one).

### 14. Email Notification Configuration

Create below environment variables and provide the email id and password that will be used to send email
- JENKINS_EMAIL
- JENKINS_PASSWORD
- To send email at the start of execution, set email id of receipent in global_variables.email_to
- To send email at the end of execution, set global_variables.email_flag = True and set email id of receipent in global_variables.email_to
- To send email to multiple people, email id's should be separated by , in global_variables.email_to

### 15. Security & Privacy settings for running AppleScript through Terminal on MacOS

Due to running AppleScript (.scpt) via osascript in Terminal, it needs to update Security & Privacy settings.
Please add `PyCharm` to `System Preferences > Security & Privacy > Privacy > Accessibility` if running test via PyCharm.
(More info could be found here: https://apple.stackexchange.com/questions/291574/osascript-is-not-allowed-assistive-access-1728)

### 16. Export Test Result Report to Google Sheet

#### Requirement
- Jenkins has installed [Allure Report Plugin](https://plugins.jenkins.io/allure-jenkins-plugin/).
- `pip install pandas pygsheets pypdfium2 Pillow requests`
- Run `pytest utilities/get_env_version.py` to save the environment versions in Allure report folder
- Google API OAuth Credential in the `vc-cloud-apps-automation-e2e` folder. Please see [pygsheets authorization](https://pygsheets.readthedocs.io/en/stable/authorization.html) for further information.
- Allure report in `vc-cloud-apps-automation-e2e` folder. The structure:
  ```
  vc-qa-test/
  ├─ vc-cloud-apps-automation-e2e/
  │  ├─ ...
  │  ├─ report/   # <--- Allure report folder
  │  │  ├─ data/
  │  │  ├─ export/
  │  │  ├─ widgets/
  │  ├─ ...
  │  ├─ sheets.googleapis.com-python.json
  │  ├─ client_secret.json
  ```

#### How to run in Jenkins pipeline

```groovy
stage('Allure report generate') {
    dir('vc-cloud-apps-automation-e2e') {
        catchError(buildResult:'SUCCESS',stageResult:'FAILURE')
        {
            if(params.node_name == 'Windows'){
                bat 'pytest utilities\\get_env_version.py'
            }
            else if(params.node_name == 'macOS'){
                sh 'pytest utilities/get_env_version.py'
            }
        }
        script{
            allure includeProperties: false, jdk: '', report: 'report', results: [[path: 'result']]
        }
    }
}

stage('Google Sheet report generate') {
    dir('vc-cloud-apps-automation-e2e') {
        catchError(buildResult:'SUCCESS',stageResult:'FAILURE')
        {
            if(params.node_name == 'Windows'){
                bat 'set PYTHONPATH=%PYTHONPATH%;%cd% & python utilities\\google_sheet.py -u [google sheet url]'
            }
            else if(params.node_name == 'macOS'){
                sh 'export PYTHONPATH="${PYTHONPATH}:pwd" && python utilities/google_sheet.py -u [google sheet url]'
            }
        }
        stash includes: 'result\\*', name: 'allure_stash'
    }
}
```

### 17. Prepare environment for Coily (Logi Dock Flex) testing
Before testing Coily, some additional apps are needed:

For MacOS (might need updating):
- XCode (no dev account needed) - https://xcodereleases.com/
- Brew (https://brew.sh/) - `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- Java JDK - `brew install java`, after installation run commands:
  - `sudo ln -sfn /opt/homebrew/opt/openjdk/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk.jdk`
  - `echo 'export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"' >> ~/.zshrc`
  - For Jenkins machines run: `brew unlink python`
- Android Studio - https://developer.android.com/studio
  - Open it after installing - another required programs/libraries will be installed
  - Create new project (can be blank - it won't be used in the future at all)
  - Go to `Tools -> SDK Menager`, then open `SDK Tools` tab, untick `Hide Obsolete Packages` in the right bottom corner, 
  tick on the list: `Android SDK Command-line Tools` and `Android SDK Tools (Obsolete)` then hit Apply to install missing tools
- scrcpy (https://github.com/Genymobile/scrcpy/blob/master/doc/macos.md) - `brew install scrcpy`
then add to PATH (if it's needed after installing with brew)
- Node.js - https://nodejs.org/en/download
- appium - `npm i -g appium`
  - install `appium driver install uiautomator2`
- appium doctor - `npm install appium-doctor -g`
- add `JAVA_HOME` and `ANDROID_HOME` to `~/.zshrc`
  - `echo export ANDROID_HOME=/Users/<macos_user_name>/Library/Android/sdk >> ~/.zshrc`
  - `echo export JAVA_HOME=/Library/Java/JavaVirtualMachines/openjdk.jdk/Contents/Home >> ~/.zshrc`
- run `appium-doctor` in Terminal, validate if any required item is missing

For Windows:
- Java JDK - https://drive.google.com/drive/folders/18fDztuDntSdY_UP8W01SoV0IOlu8TH1U?usp=sharing
- Android Studio - https://developer.android.com/studio
  - Open it after installing - another required programs/libraries will be installed
  - Create new project (can be blank - it won't be used in the future at all)
  - Go to `Tools -> SDK Menager`, then open `SDK Tools` tab, untick `Hide Obsolete Packages` in the right bottom corner, 
  tick on the list: `Android SDK Command-line Tools` and `Android SDK Tools (Obsolete)` then hit Apply to install missing tools
  - Add new Environment Variable `ANDROID_HOME` with the path to Android folder (Default: `C:\Users\{CURRENT_USER}\AppData\Local\Android\Sdk`)
- scrcpy (https://github.com/Genymobile/scrcpy/blob/master/doc/windows.md)
then unpack it and add to PATH the main folder
- Node.js - https://nodejs.org/en/download
- appium - `npm i -g appium`
  - install `appium driver install uiautomator2`
- appium doctor - `npm install appium-doctor -g`
- run `appium-doctor` in Terminal, validate if any required item is missing
- After installation Invalidate Caches in PyCharm and restart the computer

### 18. Fastboot USB Driver for Windows - issue while trying to update FW via script on Windows
If after running `adb reboot bootloader` on Windows machine the device is not visible after calling 
`fastboot devices`, you need to install USB driver from: https://drive.google.com/file/d/1oJItHEU3zxOHobKWB5DPQpOy8v4QY20r/view?usp=drive_link

1. Open `Device Manager`
2. Find `Other devices -> Android`, right click on it and choose `Update Drivers`
3. Click `Browse my computer for drivers -> Let me pick from a list of available drivers on my computer`
4. Click `Show All Devices` on the top of the list, then click `Next`
5. Click `Have Disk... -> Browse...` button, then go to folder where you unzipped downloaded file
6. Choose `android_winusb.inf` file in the `usb_driver` folder from downloaded file, hit `Open -> OK` button
7. From the list, choose `Android Bootloader Interface`, then hit `Next`
8. Click `Yes` on the warning prompt, then `Install` (Name: Google, Inc., Publisher: Google LLC)
9. After installing, run `fastboot devices` in command prompt - it should print device Serial Number connected to PC

### 19. LogiSync Personal Collab testing (macOS)

`Please repeat below steps for Terminal and Pycharm applications:`

1. Grant Full Disk Access to Application 
   - Open System Settings:
     - Click on the Apple menu () and select "System Settings."-
   - Go to Privacy & Security:
     - In the sidebar, click on "Privacy & Security."
   - Select Full Disk Access:
          Scroll down to find "Full Disk Access" and click on it. 
   - Add Application:
     - Click the "+" button at the bottom of the list. 
     - Navigate to the Applications folder, select "Utilities," and then select "Application."
     - Click "Open" to add Terminal to the list. 
   - Enable Application:
     - Ensure that the checkbox next to Terminal is checked.

2. Grant Accessibility Permissions to Application
   - Open System Settings:
     - Click on the Apple menu () and select "System Settings."
   - Go to Privacy & Security:
     - In the sidebar, click on "Privacy & Security."
   - Select Accessibility:
     - Scroll down to find "Accessibility" and click on it.
   - Add Application:
     - Click the "+" button at the bottom of the list.
     - Navigate to the Applications folder, select "Utilities," and then select "Application."
     - Click "Open" to add Terminal to the list.
   - Enable Application:
     - Ensure that the checkbox next to Terminal is checked.

