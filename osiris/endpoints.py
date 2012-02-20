from pyramid.view import view_config
from osiris.errorhandling import OAuth2ErrorHandler
from osiris.authorization import password_authorization


@view_config(name='token',
             renderer='json',
             request_method='POST',
             http_cache=0)
def token_endpoint(request):
    """
    The token endpoint is used by the client to obtain an access token by
    presenting its authorization grant or refresh token. The token
    endpoint is used with every authorization grant except for the
    implicit grant type (since an access token is issued directly).
    """
    # import ipdb;ipdb.set_trace()
    expires_in = request.registry.settings.get('osiris.tokenexpiry', 0)

    grant_type = request.params.get('grant_type')

    # Authorization Code Grant
    if grant_type == 'authorization_code':
        return OAuth2ErrorHandler.error_unsupported_grant_type()
    # Implicit Grant
    elif grant_type == 'implicit':
        return OAuth2ErrorHandler.error_unsupported_grant_type()
    # Client Credentials
    elif grant_type == 'client_credentials':
        return OAuth2ErrorHandler.error_unsupported_grant_type()
    # Client Credentials Grant
    elif grant_type == 'password':
        scope = request.params.get('scope', '')  # Optional
        username = request.params.get('username', None)
        password = request.params.get('password', None)
        if username is None:
            return OAuth2ErrorHandler.error_invalid_request('Required paramer "username" not found in the request')
        elif password is None:
            return OAuth2ErrorHandler.error_invalid_request('Required paramer "password" not found in the request')
        else:
            return password_authorization(request, username, password, scope, expires_in)
    else:
        return OAuth2ErrorHandler.error_unsupported_grant_type()
