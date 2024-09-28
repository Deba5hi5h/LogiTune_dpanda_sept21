option explicit

Dim arguments
arguments = Wscript.Arguments.Item(0)

Dim arguments_list, arguments_count, i, rule_name, ip_addresses, start
arguments_list = Split(arguments, ",")

arguments_count = UBound(arguments_list)
'Wscript.Echo arguments_count
ip_addresses = ""
rule_name = "Allow_Hosts"
If arguments_count > 0 Then
    if InStr(1, arguments_list(0), ".") Then
        start = 0
    Else
        start = 1
        rule_name = arguments_list(0)
    End If
    For i = start to arguments_count
        if i = start Then
            ip_addresses = arguments_list(i)
        Else
            ip_addresses = ip_addresses + "," + arguments_list(i)
        End If
    Next
Else
    ip_addresses = arguments
End if

Dim CurrentProfiles

' Protocol numbers for future use
Const NET_FW_IP_PROTOCOL_TCP = 6
Const NET_FW_IP_PROTOCOL_UDP = 17

'Direction
Const NET_FW_RULE_DIR_IN = 1
Const NET_FW_RULE_DIR_OUT = 2

'Action
Const NET_FW_ACTION_ALLOW = 1

' Create the FwPolicy2 object.
Dim fwPolicy2
Set fwPolicy2 = CreateObject("HNetCfg.FwPolicy2")

' Get the Rules object
Dim RulesObject
Set RulesObject = fwPolicy2.Rules

CurrentProfiles = fwPolicy2.CurrentProfileTypes

'Create a Rule Object.
Dim NewRule
Set NewRule = CreateObject("HNetCfg.FWRule")
    
NewRule.Name = rule_name
NewRule.Description = "Allow Remote Computers"
NewRule.RemoteAddresses = ip_addresses
NewRule.Direction = NET_FW_RULE_DIR_OUT
NewRule.Enabled = TRUE  
'NewRule.Profiles = CurrentProfiles
NewRule.Action = NET_FW_ACTION_ALLOW

'Remove the rule with same name if it exists
RulesObject.Remove NewRule.Name
        
'Add a new rule
RulesObject.Add NewRule