import pytest
from flask import url_for

q_email = 'some.one@digital.cabinet-office.gov.uk'

email_depts = [('some.one@cabinetoffice.gov.uk',
                'Cabinet Office')]


class When_on_change_email(object):

    def it_shows_the_email_address_query_string_in_the_textbox(
            self, live_server, browser):

        browser.visit(url_for('main.change_email_address',
                              email_address=q_email, _external=True))

        assert browser.find_by_css('#email_address').value == q_email

    @pytest.mark.parametrize("email_address,department", email_depts)
    def it_goes_to_department_confirm_when_continue_clicked_after_email_changed(
            self, live_server, browser, email_address, department):

        browser.visit(url_for('main.change_email_address',
                              email_address=q_email, _external=True))

        browser.fill('email_address', email_address)

        browser.find_by_css('form button').click()

        assert browser.url == url_for(
            'main.confirm_dept', _external=True)
        assert browser.find_by_css(
            '#confirm-dept > div > div').value == email_address
        assert department in browser.find_by_css(
            '#confirm-dept > h2').value
