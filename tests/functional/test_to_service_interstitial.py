from bs4 import BeautifulSoup
from flask import url_for
import pytest


def request(url, method):
    r = method(url)
    r.soup = BeautifulSoup(r.get_data(as_text=True), 'html.parser')
    return r


class When_on_to_service_interstitial(object):

    @pytest.fixture(autouse=True)
    def setup_page(self, client, app):
        self.delay = app.config['META_REFRESH_DELAY']
        self.service_page_redirect = 'to-service-page'

        with client.session_transaction() as session:
            session['auth_redirect'] = self.service_page_redirect

        self.response = request(url_for('main.to_service'), client.get)

    def it_has_continue_link_href_set_to_service_page(self, client):
        next_link = self.response.soup.select_one('.next a')

        assert self.service_page_redirect == next_link['href']

    def it_has_countdown_set_to_the_meta_refresh_config(self):
        redirect_timer_text = self.response.soup.select_one(
            ".redirect-timer").text

        assert "{} seconds".format(self.delay) in redirect_timer_text
