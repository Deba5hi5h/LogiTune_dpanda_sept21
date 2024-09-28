#!/bin/bash

# Inputted variables
appName="LogiTune"

function silent_app_quit() {
    # silently kill the application.
    appName="$1"
    if [[ $(pgrep -ix "$appName") ]]; then
    	echo "Closing $appName"
    	/usr/bin/osascript -e "quit app \"$appName\""
    	sleep 1

    	# double-check
    	countUp=0
    	while [[ $countUp -le 10 ]]; do
    		if [[ -z $(pgrep -ix "$appName") ]]; then
    			echo "$appName closed."
    			break
    		else
    			let countUp=$countUp+1
    			sleep 1
    		fi
    	done
        if [[ $(pgrep -x "$appName") ]]; then
    	    echo "$appName failed to quit - killing."
    	    /usr/bin/pkill "$appName"
        fi
    fi
}

if [[ -z "${appName}" ]]; then
    echo "No application specified!"
    exit 1
fi

# quit the app if running
silent_app_quit "$appName"

# Now remove the app
echo "Removing application: ${appName}"

# Add .app to end when providing just a name e.g. "TeamViewer"
if [[ ! $appName == *".app"* ]]; then
	appName=$appName".app"
fi

# Add standard path if none provided
if [[ ! $appName == *"/"* ]]; then
	appToDelete="/Applications/$appName"
else
	appToDelete="$appName"
fi

# Remove the application
sudo /bin/rm -rf "${appToDelete}"

# Try to Forget the packages if we can find a match
# Loop through the remaining parameters
for package in "${@:5}"; do
    if [[ ${package} ]]; then
        /usr/sbin/pkgutil --pkgs | /usr/bin/grep -i "${package}" | /usr/bin/xargs /usr/bin/sudo /usr/sbin/pkgutil --forget
    fi
done

echo "Application: ${appName} removed"
