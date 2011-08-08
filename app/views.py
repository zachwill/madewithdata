"""
Flask Module Docs:  http://flask.pocoo.org/docs/api/#flask.Module

This file is used for both the routing and logic of your
application.
"""

from flask import (Module, render_template, redirect, request,
                   url_for, jsonify)

from epa.pcs import PCS

from .forms import EpaForm

views = Module(__name__, 'views')


@views.route('/')
def index():
    """Render website's index page."""
    # For now, we'll redirect to the EPA data.
    return redirect(url_for('epa'))


@views.route('/epa/')
def epa():
    """Render the EPA page with a form to query EPA APIs."""
    form = EpaForm()
    return render_template('epa.html', form=form)


@views.route('/epa/data')
def epa_data():
    q = request.args['q']
    location = request.args['location']
    if q == 'pcs' and location:
        return redirect(url_for('epa_pcs', zipcode=location))
    return redirect(url_for('epa'))


@views.route('/epa/pcs')
def epa_pcs():
    """
    Find facilities in a zipcode that have EPA permits to pollute public
    water sources.
    """
    if 'zipcode' not in request.args:
        return redirect(url_for('epa'))
    zipcode = request.args['zipcode']
    data = PCS().facility('location_zip_code', zipcode)
    if 'format' in request.args and request.args['format'] == 'json':
        return jsonify(data)
    return render_epa_pcs_data(data, zipcode)


def render_epa_pcs_data(data, zipcode):
    """Separate rendering logic from `epa_pcs` function."""
    if 'Count' in data:
        count = int(data['Count'])
    else:
        # Yay! No polluters.
        return render_template('epa_data/pcs_zero.html')
    pcs_data = data['PCS_PERMIT_FACILITY']
    names, waters = set(), set()
    if not count > 1:
        # Then it's only one facility -- needs to be in a list.
        pcs_data = [pcs_data]
    for d in pcs_data:
        name = d['LOCATION_NAME']
        names.update([name])
        water = d['RECEIVING_WATERS']
        if water:
            waters.update([water])
    names, waters, empty_waters = pcs_set_to_list(names, waters)
    return render_template('epa_data/pcs_zipcode.html', count=count,
                           names=names, waters=waters, zipcode=zipcode,
                           empty_waters=empty_waters)


def pcs_set_to_list(names, waters):
    """
    Turn sets to lists and make sure that they have a length of 5
    elements.
    """
    names, waters = list(names), list(waters)
    if not waters:
        # It was an empty set.
        empty_waters = True
    else:
        empty_waters = False
    names = append_blank_elements(names, 5)
    waters = append_blank_elements(waters, 5)
    return names, waters, empty_waters


def append_blank_elements(some_list, desired_length):
    """
    Append blank elements to a list if it's length is less than a
    designated number.
    """
    if len(some_list) < desired_length:
        number = desired_length - len(some_list)
        blank = [''] * number
        some_list.extend(blank)
    return some_list


@views.route('/qunit/')
def qunit():
    """Render a QUnit page for JavaScript tests."""
    return render_template('test_js.html')


@views.after_request
def add_header(response):
    """Add header to force latest IE rendering engine and Chrome Frame."""
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    return response


@views.app_errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
