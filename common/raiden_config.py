# Raiden End Points
ORG_ENDPNT = '/api/org/'
PUBLICAPI_V1_ORG_ENDPNT = '/v1/org/'
SIGNIN_ENDPNT = '/api/session/sign-in'
VERSION_ENDPNT = '/api/version'
SESSION_ENDPNT = '/api/session/context'
USER_ENDPNT = '/api/user'

# Errors
FORBIDDEN_ERROR = (int('403'), 'Forbidden', 'ForbiddenError')
CONFLICT_ERROR = (int('409'), 'Conflict', 'ConflictError')
AUTHORIZE_ERROR = (int('401'), 'Bad Token')
NOTFOUND_ERROR = (int('404'), 'NotFoundError', 'room not found')

ORGS_GET_ERROR = {
    'OrgViewer': FORBIDDEN_ERROR,
    'OrgAdmin': FORBIDDEN_ERROR,
    'Readonly': FORBIDDEN_ERROR
}

ORG_EXISTING_ERROR = {
    'OrgViewer': FORBIDDEN_ERROR,
    'OrgAdmin': FORBIDDEN_ERROR,
    'SysAdmin': CONFLICT_ERROR,
    'Viewer': FORBIDDEN_ERROR,
    'Readonly': FORBIDDEN_ERROR
}

ORG_UPDATE_ERROR = {
    'OrgViewer': FORBIDDEN_ERROR,
    'OrgAdmin': FORBIDDEN_ERROR,
    'SysAdmin': CONFLICT_ERROR,
    'Viewer': FORBIDDEN_ERROR,
    'Readonly': FORBIDDEN_ERROR
}

USER_EXISTING_ERROR = {
    'OrgViewer': FORBIDDEN_ERROR,
    'OrgAdmin': CONFLICT_ERROR,
    'SysAdmin': CONFLICT_ERROR,
}

DEPROVISION_ERROR = {
    'OrgViewer': FORBIDDEN_ERROR,
    'OrgAdmin': NOTFOUND_ERROR,
    'SysAdmin': NOTFOUND_ERROR,
}
