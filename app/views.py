"""
Flask Module Docs:  http://flask.pocoo.org/docs/api/#flask.Module

This file is used for both the routing and logic of your
application.
"""

from flask import (Module, render_template, redirect, request,
                   url_for, jsonify, flash)

import mapq
from epa.pcs import PCS

from epa_utils import address_details, nearest_facility, pcs_set_to_list
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
    elif q == 'radinfo' and location:
        return redirect(url_for('epa_radinfo', address=location))
    return redirect(url_for('epa'))


@views.route('/epa/radinfo')
def epa_radinfo():
    """
    Find facilities in a zipcode that have EPA permits to pollute public
    water sources.
    """
    if 'format' in request.args:
        return views.send_static_file('js/all_facilities.json')
    elif 'address' not in request.args:
        return redirect(url_for('epa'))
    address = request.args['address']
    try:
        mapq.key("Fmjtd|luua2lu2ll,80=o5-hy82u")
        geo_data = mapq.geocode(address)
    except:
        return redirect(url_for('epa'))
    else:
        # Find the address state.
        state, coords = address_details(geo_data)
        # Search against the dict of radiation location states.
        closest, mileage = nearest_facility(state, coords)
        # Return miles and address of nearest location.
    latitude, longitude = closest
    latitude, longitude = round(latitude, 2), round(longitude, 2)
    mileage = int(round(mileage))
    return render_template('epa_data/radinfo.html', mileage=mileage,
                           latitude=latitude, longitude=longitude)


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


# The following should be applicable to all web applications.

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
