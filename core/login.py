import requests
from bs4 import BeautifulSoup

LOGIN_URL = "https://warframe.market/signin"

def login(session=requests.Session(), email, password):
    """ Attempts to log-in based off the given credentials

    Args:
        session: (Optional) Allows for future GET's using the same session
            to be authenticated. Defaults to arbitrary session if not given.
        email: E-mail to be used to log-in
        password: Password to use when logging-in (plaintext)

    Returns:
        Returns "None" if unable to log-in, otherwise, return
        the CSRF_TOKEN used for the session.
    """

    # go the the base URL
    login_page = session.get(LOGIN_URL)

    # try and get the CSRF_TOKEN
    soup = BeautifulSoup(login_page.text, 'html.parser')
    CSRF_TOKEN = soup.find(id="csrf_token")['value']

    # build the payload
    login_payload = {
        "csrf_token": CSRF_TOKEN,
        "LoginEmail": email,
        "LoginPassword": password
    }

    print("[LOGIN] EMAIL: %s | CSRF: %s" % (login_payload['LoginEmail'],
                                            login_payload['csrf_token']));

    # lets try and post the payload
    login_post = s.post(
                        LOGIN_URL,
                        data=login_payload,
                        headers={ "Referer": LOGIN_URL }
                        )

    # check to see if we're logged in
    soup = BeautifulSoup(login_post.text, 'html.parser')

    # something went wrong (it cannot find the "Account" dropdown)
    if (soup.find( "a", class_="dropdown-toggle" ) == None):
        print "[ERR] Uh oh! Check your credentials."
        return

    # if we've reached here, SUCCESS!
    return CSRF_TOKEN
