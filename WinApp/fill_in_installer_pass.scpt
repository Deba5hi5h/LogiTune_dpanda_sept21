on run argv
    return installPassword(item 1 of argv)
end run

on installPassword(pass)
    tell application "System Events"
        with timeout of 120 seconds
            repeat until (exists application process "SecurityAgent")
                delay 1
            end repeat

            tell process "SecurityAgent"
                if exists (text field 2 of window 1) then
                    set value of text field 2 of window 1 to pass
                end if
                click button "OK" of window 1
            end tell
        end timeout
    end tell
end installPassword