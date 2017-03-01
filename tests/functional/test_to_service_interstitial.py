import re

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
        self.config_countdown = app.config['META_REFRESH_DELAY']

        self.service_page_redirect = 'to-service-page'

        with client.session_transaction() as session:
            session['auth_redirect'] = self.service_page_redirect

        self.response = request(url_for('main.to_service'), client.get)

    def it_has_continue_link_href_set_to_service_page(
            self, client):
        next_li = self.response.soup.find("li", class_="next")

        assert self.service_page_redirect == next_li.find('a')['href']

    def it_has_countdown_set_to_the_meta_refresh_config(self, config):
        countdown_text = self.response.soup.select_one(
            "#content span.pagination-text span").text

        countdown_int = int(re.match(r'\d+', countdown_text).group())

        assert countdown_int == self.config_countdown
