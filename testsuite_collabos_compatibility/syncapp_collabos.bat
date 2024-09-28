SET device_list="Rally Bar"
SET sync_app_version="3.1.308"
SET sync_portal_env="raiden-prod"

echo %sync_app_version%
echo %device_list%
echo %sync_portal_env%

cd ..
python testsuite_collabos_compatibility\test_runner_syncapp.py -n %sync_app_version% -d %device_list% -e %sync_portal_env%