from bs4 import BeautifulSoup
from flask import url_for
import pytest


cookie_name = 'gateway_idp'
cookie_value = 'gds-google'
department = "Government Digital Service"


def request(url, method, **kwargs):
    r = method(url, **kwargs)
    r.soup = BeautifulSoup(r.get_data(as_text=True), 'html.parser')
    return r


class WhenOnToIDPInterstitialWithSuggestedIDPSessionSet(object):

    @pytest.fixture(autouse=True)
    def setup_page(self, client):
        with client.session_transaction() as session:
            session['suggested_idp'] = cookie_value
        self.response = request(url_for('main.to_idp'),
                                client.get, follow_redirects=True)

    def it_stores_suggested_IDP_in_Gateway_IDP_cookie(self):
        cookie = self.response.headers['Set-Cookie']
        assert "{}={};".format(cookie_name, cookie_value) in cookie


class WhenNavigatingToAuthPathWithGatewayIDPCookieSet(object):

    @pytest.fixture(autouse=True)
    def setup_page(self, client):
        client.set_cookie('localhost', cookie_name, cookie_value)
        self.response = request(url_for('main.authentication_request'),
                                client.get, follow_redirects=True)

    def it_redirects_to_department_confirmation_with_department_set(self):
        assert department in self.response.soup.select_one("form legend").text

    def it_redirects_to_dept_confirm_and_does_not_show_email_given_box(self):
        assert self.response.soup.select_one(".email-given") is None
