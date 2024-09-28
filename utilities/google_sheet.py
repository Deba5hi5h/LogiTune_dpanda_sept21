# for python 3.8 workaround
# Once we upgrade to 3.11, we can replace this with 'from typing import Self'
from __future__ import annotations

import argparse
import bz2
import codecs
import datetime
import difflib
import json
import pathlib
import pickle
import platform
import re
import sys
import base64
import io
import time
from dataclasses import dataclass, field
from itertools import accumulate, groupby
from typing import Any, Literal

import pandas as pd
import pygsheets
import pypdfium2
import requests
from selenium.webdriver.common.by import By
from PIL import Image, ImageChops

from testsuite_firmware_api_tests.api_tests.device_api_names import DeviceName
from apps.browser_methods import BrowserClass

STATUS_STYLE: dict[AllureReport.Testcase.Status, dict] = {
    'passed': { 'symbol': '🟢', 'backgroundColor': (0.8, 1, 0.8, 1)},
    'failed': { 'symbol': '🔴', 'backgroundColor': (1, 0.8, 0.8, 1)},
    'skipped': { 'symbol': '⚪️', 'backgroundColor': (0.9, 0.9, 0.9, 1)},
    'broken': { 'symbol': '🟡', 'backgroundColor': (1, 1, 0.8, 1)},
    'info': { 'symbol': '🔵', 'backgroundColor': (0.8, 0.8, 1, 1)},
}

@dataclass
class AllureReport:
    """
    This class reads the test results generated from Jenkins plugin `https://plugins.jenkins.io/allure-jenkins-plugin/`
    """
    environment: dict[str, str]
    testcase: dict[str, Testcase]
    executor: dict[str, str]

    CONNECTION_TYPES = ['BT', 'USB']

    class Testcase(dict):
        """
        This class stores the test results of each test case.
        """
        Status = Literal['passed', 'failed', 'skipped', 'broken', 'info']

        @property
        def full_name(self) -> str:
            full_name = ' '.join(re.sub('((tc|test)_(.*?_)|vc_\d+_?|bt|dongle)\s*', '', self['name'], flags=re.IGNORECASE).split('_'))
            return full_name

        @property
        def device_or_ui_name(self) -> str:
            device_or_ui_name = next(filter(lambda x: re.match(f'.*{x}.*', self.full_name, re.IGNORECASE), AllureReport.get_all_possible_device()), None)
            if device_or_ui_name is None:
                device_or_ui_name = "UI"

            return device_or_ui_name

        @property
        def connection_type(self) -> str:
            if not self.is_device_test:
                connection_type = ''
                return connection_type

            connection_type = 'BT' if re.match(".*BT.*", '.'.join(self['parent']), re.IGNORECASE)  else 'USB'
            return connection_type

        @property
        def testcase_name(self) -> str:
            if not self.is_device_test:
                testcase_name = self.full_name.title()
                return testcase_name

            connection_type = self.connection_type
            testcase_name = re.sub(f'\s*({self.device_or_ui_name}|{connection_type})\s*', '', self.full_name, flags=re.IGNORECASE).title()
            testcase_name = re.sub(f'\s*(^headset|headset$)\s*', '', testcase_name, flags=re.IGNORECASE).title()
            return testcase_name

        @property
        def is_device_test(self) -> bool:
            return self.device_or_ui_name != 'UI'

    def _read_date_from_jenkins(self) -> datetime.datetime:
        """
        This method reads the test results from Jenkins and stores them in the report object.
        """

        try:
            pipeline = requests.get(self.executor['buildUrl']).text
            upstream_path = re.findall('build number.*href="(.*?)"', pipeline)[0]
            upstream = requests.get(self.executor['url'] + upstream_path[1:]).text
            date_str = re.findall('Build #.* \((.*)\)', upstream)[0]
            date = datetime.datetime.strptime(date_str, "%b %d, %Y, %I:%M:%S %p")
            return date
        except Exception as e:
            print(f'Failed to read date from Jenkins: {e}')

        return datetime.datetime.now()

    def download_history_trend(self, fp) -> None:
        base_url = self.executor.get('reportUrl', '')
        url = '{}/graph'.format(base_url)
        res = requests.get(url=url)
        res.raise_for_status()

        with open(fp, 'wb') as f:
            f.write(res.content)

    def get_firmware_version(self, device_or_ui_name: str) -> str:
        firmware_version = ''
        if device_or_ui_name is not None and '_'.join(device_or_ui_name.split()) in self.environment:
            firmware_version = self.environment['_'.join(device_or_ui_name.split())]

        return firmware_version

    def get_rate(self, state: Testcase.Status) -> float:
        return sum(1 for x in self.testcase.values() if x['status'] == state) / len(self.testcase)

    @property
    def tune_version(self) -> str:
        return '.'.join(self.environment['Tune_version'].split('.')[:3])

    @classmethod
    def get_all_possible_device(cls) -> list[str]:
        all_member = DeviceName.__dict__.items()
        all_devices = [y for x, y in all_member if type(y) == str and not x.startswith('__')]
        return list(sorted(all_devices, reverse=True))

    @classmethod
    def _read_environment(cls, json_file: str) -> dict:
        try:
            with open(json_file, 'r') as f:
                environment = dict((record['name'], record['values'][0]) for record in json.load(f))

            if 'platform' in environment:
                os_name = environment['platform']
            else:
                os_name = ' '.join(platform.platform(terse=True).split('-'))
                if os_name == "Windows 10" and sys.getwindowsversion().build > 22000:
                    os_name = "Windows 11"

            os_type, os_version = re.findall('(Windows|macOS).*?(\d+\.?\d*).*', os_name, flags=re.IGNORECASE)[0]
            environment['platform'] = f'{os_type} {os_version}'
            environment['os_type'] = os_type
            environment['os_version'] = os_version

            return environment
        except Exception as e:
            raise Exception(f'{json_file} not found: {e}')

    @classmethod
    def _read_testcase(cls, json_file: str, environment: dict) -> dict:
        try:
            with open(json_file, 'r') as f:
                nested_suite = json.load(f)

            testcase = dict()
            def flatten(nested_suites, parent=[environment['platform']]):
                for nested_suite in nested_suites:
                    if 'children' in nested_suite:
                        flatten(nested_suite['children'], parent + [nested_suite['name']])
                    else:
                        nested_suite['parent'] = parent
                        nested_suite['duration'] = nested_suite['time']['duration'] // 1000

                        testcase[nested_suite['uid']] = AllureReport.Testcase({
                            "name": nested_suite['name'],
                            "uid": nested_suite['uid'],
                            "parentUid": nested_suite['parentUid'],
                            "status": nested_suite['status'],
                            "parent": nested_suite['parent'],
                            "duration": nested_suite['duration'],
                        })
            flatten([nested_suite])

            return testcase
        except Exception as e:
            raise Exception(f'{json_file} not found: {e}')

    @classmethod
    def _read_executor(cls, json_file: str) -> dict:
        try:
            with open(json_file, 'r') as f:
                executor = json.load(f)[0]

            return executor
        except Exception as e:
            raise Exception(f'{json_file} not found: {e}')

    @classmethod
    def from_path(cls, report_folder='./report') -> AllureReport:
        report_folder = pathlib.Path(report_folder)

        environment = cls._read_environment(report_folder / 'widgets/environment.json')
        testcase = cls._read_testcase(report_folder / 'data/suites.json', environment)
        executor = cls._read_executor(report_folder / 'widgets/executors.json')
        self = AllureReport(environment, testcase, executor)
        self.environment['date'] = self._read_date_from_jenkins()

        return self

# for compatibility
Report = AllureReport

@dataclass
class Board:
    reports: dict[Any, AllureReport] = field(default_factory=dict)

    def add_report(self, report: AllureReport):
        self.reports[report.environment['platform']] = report

    def get_all_os(self) -> list:
        os = set()
        for report in self.reports.values():
            os.add(report.environment['platform'])

        return list(os)

    def get_all_device_name_with_conn_type_or_ui(self) -> list:
        device_name_or_ui = set()
        for report in self.reports.values():
            for testcase in report.testcase.values():
                device_name_or_ui.add(' '.join((testcase.device_or_ui_name, testcase.connection_type)).strip())

        return list(sorted(device_name_or_ui, reverse=True))

    def to_dataframe(self) -> pd.DataFrame:
        raise NotImplementedError

    def dump_to_google_sheet(self, wks: pygsheets.Worksheet) -> None:
        raise NotImplementedError

    def serialize(self) -> str:
        return codecs.encode(bz2.compress(pickle.dumps(self.reports)), "base64").decode()

    @classmethod
    def deserialize(cls, data: str) -> Summary:
        unverified_data = pickle.loads(bz2.decompress(codecs.decode(data.encode(), 'base64')))
        if type(unverified_data) != dict:
            raise Exception(TypeError('deserialize(data) is not dict'))

        board = cls(unverified_data)

        # for compatibility
        for report in board.reports.values():
            for uid, testcase in report.testcase.items():
                if type(testcase) != dict:
                    continue

                report.testcase[uid] = AllureReport.Testcase(
                    name=testcase['name'],
                    uid=testcase['uid'],
                    parentUid=testcase['parentUid'],
                    status=testcase['status'],
                    parent=testcase['parent'],
                    duration=testcase['duration'],
                )

        return board

class Summary(Board):
    def group_by_environment(self) -> dict:
        testcase_group_by_environment = dict()
        for report in self.reports.values():
            for _, testcase in report.testcase.items():
                firmware_version = report.get_firmware_version(testcase.device_or_ui_name)

                os_type = re.sub('Windows', '=IMAGE("https://img.icons8.com/ios-filled/50/windows-10.png")', report.environment['os_type'], flags=re.IGNORECASE)
                os_type = re.sub('macOS', '=IMAGE("https://img.icons8.com/ios-filled/50/mac-os.png")', report.environment['os_type'], flags=re.IGNORECASE)

                # the header rows. If need to add more header rows, add here
                key = (testcase.device_or_ui_name, os_type, report.environment['os_version'], testcase.connection_type)

                testcase_group_by_environment.setdefault(key, {})
                testcase_group_by_environment[key][testcase.testcase_name] = testcase
                testcase_group_by_environment[key]['Firmware Version'] = {'info': firmware_version, 'status': 'info'}

        # align all testcase name of environment
        all_testcase = {xx: None for x in testcase_group_by_environment.values() for xx in x}
        for key in testcase_group_by_environment:
            testcases = all_testcase.copy()
            for test_name, testcase in testcase_group_by_environment[key].items():
                testcase_name = difflib.get_close_matches(test_name, testcases, n=1)[0]
                testcases[testcase_name] = testcase

            testcase_group_by_environment[key] = testcases

        testcase_group_by_environment = dict(sorted(testcase_group_by_environment.items(), reverse=True))
        return testcase_group_by_environment

    def to_dataframe(self) -> pd.DataFrame:
        testcase_group_by_environment = self.group_by_environment()
        table = pd.DataFrame(testcase_group_by_environment)

        left_top_cell = ('',) * table.columns.nlevels
        table[left_top_cell] = table.index

        # count each row number of non nan value
        table['_cnt'] = table.apply(lambda x: x.map(lambda xx: 1 if xx and 'duration' in xx else 0)).sum(axis=1)
        # index of left most non nan value
        table['_lmv'] = table.transpose().apply(lambda x: table.columns.get_loc(x.first_valid_index()))

        table.sort_values(by=['_cnt', '_lmv', left_top_cell], ascending=[False, True, True], inplace=True)
        table.drop(columns=['_cnt', '_lmv'], inplace=True, axis=1, level=0)

        return table

    def dump_to_google_sheet(self, wks: pygsheets.Worksheet) -> None:
        table = self.to_dataframe()
        wks.adjust_column_width(start=1, end=1, pixel_size=215)
        wks.adjust_column_width(start=2, end=100, pixel_size=35)
        wks.merge_cells(start=(1, 1), end=(table.columns.nlevels, table.index.nlevels))
        wks.set_dataframe(pd.DataFrame('', columns=table.columns, index=table.index), (1, 1), copy_index=True)

        def merge_cells(level, start, end):
            if level >= table.columns.nlevels:
                return

            tail = list(accumulate([len(list(y)) for _, y in groupby(table.columns.codes[level][start:end+1])]))
            intervals = list((x + start, y + start - 1) for x, y in zip([0] + tail[:-1], tail))

            for left, right in intervals:
                if level < table.columns.nlevels:
                    merge_cells(level + 1, left, right)

                cell = pygsheets.Cell((level + 1, left + table.index.nlevels + 1))
                cell.set_vertical_alignment(pygsheets.custom_types.VerticalAlignment.MIDDLE)
                cell.set_horizontal_alignment(pygsheets.custom_types.HorizontalAlignment.CENTER)
                cell.set_text_format('bold', True)
                cell.format = (pygsheets.FormatType.TEXT, '')
                cell.set_value(table.columns[left][level])
                wks.update_cells([cell])

                if left >= right:
                    continue

                wks.merge_cells(start=(level + 1, left + table.index.nlevels + 1), end=(level + 1, right + table.index.nlevels + 1))

        merge_cells(0, 0, len(table.columns) - 1)

        table[table.isna()] = ''
        for i, row in enumerate(table.iterrows()):
            for j, col in enumerate(row[1]):
                cell = pygsheets.Cell((i + table.columns.nlevels + 1, j + table.index.nlevels + 1))
                cell.format = (pygsheets.FormatType.TEXT, '')

                if 'info' in col:
                    cell.set_value(col['info'])
                    cell.set_text_format('fontSize', 7)

                if 'duration' in col:
                    cell_val = '{:.0f}s'.format(datetime.timedelta(seconds=col['duration']).total_seconds())

                    if 'uid' in col and 'parentUid' in col:
                        allure_base_link = self.reports.get(col['parent'][0]).executor.get('reportUrl', '')
                        cell_val = '=HYPERLINK("{}/#suites/{}/{}", "{}")'.format(
                            allure_base_link,
                            col['parentUid'],
                            col['uid'],
                            cell_val
                        )

                    cell.set_value(cell_val)
                    cell.set_text_format('fontSize', 7)
                    cell.set_text_format('foregroundColor', (0, 0, 0, 0))
                    cell.set_text_format('underline', False)

                if 'status' in col:
                    cell.color = STATUS_STYLE.get(col['status'], {'backgroundColor': (1, 1, 1, 1)})['backgroundColor']
                    cell.set_text_format('bold', True)

                wks.update_cells([cell])

        left_top_cell = pygsheets.Cell((1, 1))
        left_top_cell.set_vertical_alignment(pygsheets.custom_types.VerticalAlignment.MIDDLE)
        left_top_cell.set_horizontal_alignment(pygsheets.custom_types.HorizontalAlignment.CENTER)
        left_top_cell.set_text_format('bold', True)
        left_top_cell.set_text_format('fontSize', 8)
        left_top_cell.format = (pygsheets.FormatType.TEXT, '')
        left_top_cell.set_value(
            'Tune Version:\n'
            + '\n'.join(['{}: {} | Pass Rate: {:.2f}'.format(
                    os,
                    report.tune_version,
                    report.get_rate("passed")
                ) for os, report in self.reports.items()]))
        wks.update_cells([left_top_cell])

        wks.frozen_rows = table.columns.nlevels
        wks.frozen_cols = table.index.nlevels

class TuneTrend(Board):
    def overwrite_better_test_result(self, report: AllureReport) -> None:
        os = report.environment['platform']
        tune_version = report.tune_version
        if (os, tune_version) not in self.reports:
            self.reports[(os, tune_version)] = report
            return

        new_passed_rate = report.get_rate('passed')
        old_passed_rate = self.reports[(os, tune_version)].get_rate('passed')
        if old_passed_rate > new_passed_rate:
            return

        self.reports[(os, tune_version)] = report

    def group_by_tune_version(self) -> dict:
        testcase_group_by_tune_version = dict()
        for (os, tune_version), report in self.reports.items():
            testcase_group_by_tune_version.setdefault(tune_version, {})
            for _, testcase in report.testcase.items():
                if not testcase.is_device_test:
                    key = (os, testcase.device_or_ui_name)
                else:
                    key = (os, testcase.device_or_ui_name, testcase.connection_type)

                testcase_group_by_tune_version[tune_version].setdefault(testcase.testcase_name, {})
                testcase_group_by_tune_version[tune_version][testcase.testcase_name].setdefault(key, {})
                testcase_group_by_tune_version[tune_version][testcase.testcase_name][key] = testcase

        return testcase_group_by_tune_version

    def to_dataframe(self) -> pd.DataFrame:
        testcase_group_by_environment = self.group_by_tune_version()
        table = pd.DataFrame(testcase_group_by_environment)

        # count each row number of non nan value
        table['_cnt'] = table.apply(lambda x: x.map(lambda xx: len(xx) if type(xx) == dict else 0)).sum(axis=1)

        table.sort_values(by=['_cnt'], ascending=[False], inplace=True)
        table.drop(columns=['_cnt'], inplace=True)

        return table

    def dump_to_google_sheet(self, wks: pygsheets.Worksheet) -> None:
        table = self.to_dataframe()
        wks.adjust_column_width(start=1, end=1, pixel_size=215)
        wks.adjust_column_width(start=2, end=100, pixel_size=50)

        for addr, width, dropdown_menu in [
            ((1, 2), 3, self.get_all_os()),
            ((1, 6), 3, self.get_all_device_name_with_conn_type_or_ui()),
        ]:
            wks.cell(addr).set_text_format('fontSize', 12)
            wks.cell(addr).set_text_format('bold', True)
            wks.merge_cells(start=addr, end=(addr[0], addr[1] + width))
            wks.set_data_validation(addr, addr, condition_type='ONE_OF_LIST', condition_values=dropdown_menu, showCustomUi=True, strict=True)

        wks.set_dataframe(pd.DataFrame('', columns=table.columns, index=table.index), (2, 1), copy_index=True)
        wks.apply_format('B2:$2', {'textFormat': {'bold': True}})
        table[table.isna()] = ''
        for state, style in STATUS_STYLE.items():
            wks.add_conditional_formatting(
                start=(2, 1), end=(table.shape[0] + 2, table.shape[1] + 1),
                condition_type='TEXT_CONTAINS',
                condition_values=[style['symbol']],
                format={'backgroundColor': dict(zip(('red', 'green', 'blue', 'alpha'), STATUS_STYLE.get(state, {'backgroundColor': (0, 0, 0, 0)})['backgroundColor']))}
            )

        for i, row in enumerate(table.iterrows()):
            for j, col in enumerate(row[1]):
                if type(col) != dict:
                    continue

                cell = pygsheets.Cell((i + table.columns.nlevels + 2, j + table.index.nlevels + 1))
                cell.format = (pygsheets.FormatType.TEXT, '')
                cell.set_text_format('fontSize', 7)
                cell.set_text_format('bold', True)
                cell.set_text_format('foregroundColor', (0, 0, 0, 0))
                cell.set_text_format('underline', False)

                cell_val = '=IFNA(SWITCH(B1&" "&F1'
                for key, testcase in col.items():
                    if 'duration' not in testcase:
                        continue

                    cell_val += ',"' + ' '.join(key) + '",'
                    allure_base_link = self.reports.get((testcase['parent'][0], table.columns[j])).executor.get('reportUrl', '')
                    cell_val += 'HYPERLINK("{}/#suites/{}/{}", "{} {:.0f}s")'.format(
                        allure_base_link,
                        testcase['parentUid'],
                        testcase['uid'],
                        STATUS_STYLE.get(testcase["status"])['symbol'],
                        datetime.timedelta(seconds=testcase['duration']).total_seconds()
                    )
                cell_val += '), "")'

                cell.set_value(cell_val)
                wks.update_cells([cell])

        wks.frozen_rows = table.columns.nlevels + 1
        wks.frozen_cols = table.index.nlevels

class GoogleSheet:
    gc: pygsheets.Client
    sh: pygsheets.Spreadsheet

    MAX_METADATA_SIZE = 29000

    def __init__(self, gc: pygsheets.Client, url: str) -> None:
        self.gc = gc
        self.sh = self.gc.open_by_url(url)

    def get_worksheet(self, title: str) -> pygsheets.Worksheet:
        return next(filter(lambda x: x.title == title, self.sh.worksheets()), None)

    def get_metadata(self, wks: pygsheets.Worksheet) -> str | None:
        if wks is None:
            return None

        all_metadata = wks.get_developer_metadata()
        if all_metadata and hasattr(all_metadata[0], 'value'):
            return ''.join([metadata.value for metadata in all_metadata])

        return None

    def set_metadata(self, wks: pygsheets.Worksheet, metadata: str) -> None:
        if wks is None:
            return None

        all_metadata = wks.get_developer_metadata()
        if all_metadata:
            for metadata in all_metadata:
                metadata.delete()

        # avoid exceeding the limit of 30000 characters
        for n in range(0, len(metadata), GoogleSheet.MAX_METADATA_SIZE):
            wks.create_developer_metadata(f"{wks.title}-{n}-{n+GoogleSheet.MAX_METADATA_SIZE}",
                                          metadata[n:n+GoogleSheet.MAX_METADATA_SIZE])

    def batch_mode(self, title: str):
        class BatchMode:
            def __init__(_, title: str):
                self.wks = self.get_worksheet(title)
                self.title = title

            def __enter__(_) -> pygsheets.Worksheet:
                self.gc.batch_mode = True

                self.old_wks_title = f"{self.title} [Processing]"
                if next(filter(lambda x: x.title == self.old_wks_title, self.sh.worksheets()), False):
                    self.sh.del_worksheet(self.sh.worksheet_by_title(self.old_wks_title))

                try:
                    if self.wks is not None:
                        self.wks.title = self.old_wks_title

                    self.wks = self.sh.add_worksheet(self.title, index=0)
                except Exception as e:
                    print('Error: {}'.format(e))

                self.gc.set_batch_mode(True)

                return self.wks

            def __exit__(_, exc_type, exc_val, exc_tb):
                if exc_type is None:
                    try:
                        self.gc.run_batch()
                        self.gc.set_batch_mode(False)

                        old_wks = next(filter(lambda x: x.title == self.old_wks_title, self.sh.worksheets()), None)
                        if old_wks:
                            self.sh.del_worksheet(old_wks)
                    except Exception as e:
                        print('Error: {}'.format(e))

                # restore previous state
                if next(filter(lambda x: x.title == self.old_wks_title, self.sh.worksheets()), False):
                    self.sh.del_worksheet(self.sh.worksheet_by_title(self.title))
                    self.sh.worksheet_by_title(self.old_wks_title).title = self.title

        return BatchMode(title)

    def save_png(self, wks: pygsheets.Worksheet, fp) -> Image.Image:
        # reference: https://spreadsheet.dev/comprehensive-guide-export-google-sheets-to-pdf-excel-csv-apps-script
        #            https://gist.github.com/Spencer-Easton/78f9867a691e549c9c70
        header = {'Authorization': 'Bearer ' + self.gc.oauth.token}
        url = f'https://docs.google.com/spreadsheets/export'
        res = requests.get(url=url, headers=header, params={
            'gid': wks.id, 'id': self.gc.spreadsheetId,
            'size': 'b2', 'fitw': 'true',
            'printtitle': 'true',
            'header': 'true',
            'format': 'pdf',
            'portrait': 'false',
        })
        res.raise_for_status()
        pdf = pypdfium2.PdfDocument(res.content).get_page(0)
        image = pdf.render(scale=5).to_pil()

        # crop white space
        diff = ImageChops.difference(image, Image.new(image.mode, image.size, image.getpixel((0,0))))
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if not bbox:
            return image

        # add padding
        bbox = (bbox[0] - 80, bbox[1] - 80, bbox[2] + 200, bbox[3] + 200)
        resized_image = image.crop(bbox)
        resized_image.save(fp)
        return resized_image

def generate_summary_board(gs: GoogleSheet):
    report = AllureReport.from_path('./report')

    title = report.environment['date'].strftime('%Y/%m/%d')

    summary = Summary()

    wks = gs.get_worksheet(title)
    if wks:
        metadata = gs.get_metadata(wks)
        if metadata:
            summary = Summary.deserialize(metadata)

    summary.add_report(report)

    with gs.batch_mode(title) as wks:
        gs.set_metadata(wks, summary.serialize())
        summary.dump_to_google_sheet(wks)

    report.download_history_trend('./report/export/history_trend.png')
    gs.save_png(wks, './report/export/summary.png')

def generate_tune_trend_board(gs: GoogleSheet):
    tune_trend = TuneTrend()

    all_wks = gs.sh.worksheets()
    for wks in all_wks:
        try:
            if not re.match('\d{4}/\d{2}/\d{2}', wks.title):
                continue

            metadata = gs.get_metadata(wks)
            if not metadata:
                continue

            summary = tune_trend.deserialize(metadata)
            for report in summary.reports.values():
                tune_trend.overwrite_better_test_result(report)
        except Exception as e:
            print(f'Failed to import {wks.title} from Google Sheet: {e}')

    with gs.batch_mode('Tune Trend') as wks:
        tune_trend.dump_to_google_sheet(wks)

def download_eazybi_report_png(url, authorization, device_name, os_name):
    username, password = base64.b64decode(authorization).decode('utf-8').split(':')

    browser = BrowserClass()
    browser.open_browser(url)
    browser.driver.set_window_size(1000, 800)

    browser.driver.find_element(By.LINK_TEXT, 'Continue with username and password').click()
    browser.driver.find_element(By.ID, 'login-form-username').send_keys(username)
    browser.driver.find_element(By.ID, 'login-form-password').send_keys(password)
    browser.driver.find_element(By.ID, 'login-form-submit').click()

    browser.driver.execute_script("document.body.style.zoom='50%'")
    time.sleep(3)

    try:
        browser.driver.execute_script("arguments[0].click();", browser.driver.find_element(By.CSS_SELECTOR, 'button[data-dimension="Device Name"]'))
        browser.driver.execute_script("arguments[0].click();", browser.driver.find_element(By.CSS_SELECTOR, f'li[data-fullname="[Device Name].[{device_name}]"] a'))
        time.sleep(3)

        browser.driver.execute_script("arguments[0].click();", browser.driver.find_element(By.CSS_SELECTOR, 'button[data-dimension="Operating System"]'))
        browser.driver.execute_script("arguments[0].click();", browser.driver.find_element(By.CSS_SELECTOR, f'li[data-fullname="[Operating System].[{os_name}]"] a'))
        time.sleep(3)
    except Exception as e:
        print('Failed to select device name and operating system: ', e)

    element = browser.driver.find_element(By.CLASS_NAME, 'aui-page-panel-content')

    im = Image.open(io.BytesIO(browser.driver.get_screenshot_as_png()))

    left = element.location['x']
    top = element.location['y']
    right = element.location['x'] + element.size['width']
    bottom = element.location['y'] + element.size['height']

    im = im.crop((left, top, right, bottom))
    im.save('./report/export/history_trend.png')

    browser.close_browser()

def main(args):
    gc = pygsheets.authorize(service_account_file='./service-account.json')
    gs = GoogleSheet(gc, args.url_of_google_sheet)

    generate_summary_board(gs)
    generate_tune_trend_board(gs)
    download_eazybi_report_png(args.url_of_eazybi, args.authorization_of_eazybi, args.device_of_eazybi, args.os_name_of_eazybi)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url-of-google-sheet", help="URL of Google Sheet")
    parser.add_argument("-e", "--url-of-eazybi", help="URL of eazyBI")
    parser.add_argument("-a", "--authorization-of-eazybi", help="Authorization of eazyBI")
    parser.add_argument("-d", "--device-of-eazybi", help="Device of eazyBI")
    parser.add_argument("-o", "--os-name-of-eazybi", help="Operating System of eazyBI")
    args = parser.parse_args()

    main(args)
