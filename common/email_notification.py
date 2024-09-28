import os
import smtplib

from email.message import EmailMessage
from typing import Optional

from base import global_variables
from common.framework_params import PROJECT, INSTALLER
from common.platform_helper import get_custom_platform, get_current_system_version, get_cpu_vendor, \
    get_installer_version


class EmailNotification:
    @staticmethod
    def send_report_email(url, passed, failed, blocked, skipped):
        """
        Method to send email with pass/fail details and link to report on completion of test execution
        This is used in Dashboard.py when gloabl_varibales.email_flag is set to True
        Set email id (to whom email will be sent) in gloabl_varibales.email_to
        :param url, passed, failed, blocked, skipped
        :return none
        """
        try:

            project = PROJECT
            platform = get_custom_platform()
            system_version = get_current_system_version()
            msg = EmailMessage()
            installer_version = get_installer_version() if project == 'LogiTune' else INSTALLER
            msg['Subject'] = f"Automation Results for {project} {installer_version} {global_variables.test_category} on {platform}-{system_version}"

            msg['From'] = os.environ.get('JENKINS_EMAIL')
            msg['To'] = global_variables.email_to
            msg.set_content(f"Test Results for {project} on {platform}-{system_version} - {url}")
            msg.add_alternative(f"""\
                <div>Hello,</div>
                <div>Automated tests execution for {project} {installer_version} {global_variables.test_category} completed on {platform}-{system_version}. Below are the results</div>
                <div> {global_variables.email_details} </div>
                <h1 style="color: #3366ff;">Automation Test Results</h1>
                <table style="border-collapse: collapse; width: 100%; height: 36px;" border="1">
                <tbody>
                <tr style="height: 18px;">
                <td style="width: 25%; height: 18px; background-color: silver; text-align: center;"><strong>Pass</strong></td>
                <td style="width: 25%; height: 18px; background-color: silver; text-align: center;"><strong>Fail</strong></td>
                <td style="width: 25%; height: 18px; background-color: silver; text-align: center;"><strong>Blocked</strong></td>
                <td style="width: 25%; height: 18px; background-color: silver; text-align: center;"><strong>Skipped</strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 25%; height: 18px; text-align: center;">{passed}</td>
                <td style="width: 25%; height: 18px; text-align: center;">{failed}</td>
                <td style="width: 25%; height: 18px; text-align: center;">{blocked}</td>
                <td style="width: 25%; height: 18px; text-align: center;">{skipped}</td>
                </tr>
                </tbody>
                </table>
                <div>&nbsp;</div>
                <div>For detailed test report, click&nbsp;<a href="{url}">here</a></div>
                <div>&nbsp;</div>
                <div>Regards,</div>
                <div>Automation Team</div>
            """, subtype='html')

            send_email(msg)
        except Exception as e:
            print(e)

    @staticmethod
    def send_job_email(project_name: Optional[str] = None):
        """
        Method to send email on start of test execution
        Set email id (to whom email will be sent) in global_varibales.email_to
        :param project_name
        :return none
        """
        try:
            if project_name:
                project = project_name
            else:
                project = PROJECT
            platform = get_custom_platform()
            system_version = get_current_system_version()
            msg = EmailMessage()

            installer_version = get_installer_version() if project == 'LogiTune' else INSTALLER

            msg['Subject'] = f"Jenkins job started for {project} {installer_version} {global_variables.test_category} on '{platform}-{system_version} {get_cpu_vendor()}'"

            print(f"msg['Subject']: {msg['Subject']}")
            msg['From'] = os.environ.get('JENKINS_EMAIL')
            msg['To'] = global_variables.email_to
            msg.set_content(f"Automated tests execution for {project} {installer_version} {global_variables.test_category} started on {platform}-{system_version}")
            msg.add_alternative(f"""\
                <div>Hello,</div>
                <div>Automated tests execution for {project} {installer_version} started on {platform}-{system_version}.&nbsp;</div>
                <div>&nbsp;</div>
                <div>Regards,</div>
                <div>Automation Team</div>
            """, subtype='html')

            send_email(msg)
        except Exception as e:
            print(e)

    @staticmethod
    def send_missing_devices(missing_devices: list) -> None:
        """
        Method to send email of missing device before test execution start
        :param missing_devices - list of strings (names of missing devices)
        :return none
        """
        try:
            html_parsed_missing_devices = '\n'.join(
                [f'<div>- {device}</div>' for device in missing_devices])
            project = PROJECT
            platform = get_custom_platform()
            system_version = get_current_system_version()
            installer_version = get_installer_version()
            s_or_not = 's' if len(missing_devices) > 1 else ''
            subject = f"{project} {installer_version} {global_variables.test_category} on {platform}-" \
                      f"{system_version} {get_cpu_vendor()} - {len(missing_devices)} device{s_or_not} not detected"
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = os.environ.get('JENKINS_EMAIL')
            msg['To'] = global_variables.email_to
            msg.set_content(subject)
            msg.add_alternative(f"""
                <div>Hello,</div>
                <div>There are missing devices on {platform} - {system_version} for {project} {installer_version}:</div>
                {html_parsed_missing_devices}
                <div>&nbsp;</div>
                <div>Regards,</div>
                <div>Automation Team</div>
            """, subtype='html')

            send_email(msg)
        except Exception as e:
            print(e)


def send_email(message: EmailMessage) -> None:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.environ.get('JENKINS_EMAIL'), os.environ.get('JENKINS_PASSWORD'))
        smtp.send_message(message)
