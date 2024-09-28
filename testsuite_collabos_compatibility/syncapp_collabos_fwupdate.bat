SET device_list="Rally Bar"
SET sync_app_version="3.1.185"
SET sync_portal_env="raiden-prod"
SET update_channel="futen-prod-qa"

echo %sync_app_version%
echo %device_list%
echo %sync_portal_env%
echo %update_channel%

cd ..
python testsuite_collabos_compatibility\test_runner_syncapp_fwupdate.py -n %sync_app_version% -d %device_list% -e %sync_portal_env% -f %update_channel%