import pytest
from flask import url_for

supplied_email = 'some.one@digital.cabinet-office.gov.uk'


class When_on_change_email_address_page(object):

    def it_shows_the_email_address_supplied_in_the_textbox(
            self, live_server, browser):

        browser.visit(url_for(
            'main.change_email_address', email_address=supplied_email, _external=True))

        assert browser.find_by_css('#email_address').value == supplied_email

    def it_goes_to_dept_confirm_when_continue_clicked(
            self, live_server, browser):

        email_address = 'some.one@cabinetoffice.gov.uk'
        department = 'Cabinet Office'

        browser.visit(url_for(
            'main.change_email_address', email_address=supplied_email, _external=True))

        browser.fill('email_address', email_address)

        browser.find_by_css('form button').click()

        assert browser.url == url_for(
            'main.confirm_dept', _external=True)
        assert browser.find_by_css(
            '#confirm-dept > div > div').value == email_address
        assert department in browser.find_by_css(
            '#confirm-dept > h2').value
