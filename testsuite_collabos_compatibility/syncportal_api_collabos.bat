SET sync_app_version="3.1.185"
SET sync_portal_env="raiden-prod"
SET hostedkong_ip="172.23.154.136"
SET diddy_ip="172.23.154.207"

echo %sync_app_version%
echo %sync_portal_env%
echo %hostedkong_ip%
echo %diddy_ip%

cd ..
python testsuite_collabos_compatibility\test_runner_syncportal_api.py -n %sync_app_version% -e %sync_portal_env% -k %hostedkong_ip% -d %diddy_ip%