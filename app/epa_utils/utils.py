"""Utility functions for the EPA views."""

from math import sin, cos, atan2, sqrt, radians
from radiation_facilities import RADIATION_FACILITIES


def address_details(geo_data):
    """
    Based on geocoded data from Google's API, find both the coordinates and
    state for an address.
    """
    place = geo_data['Placemark'][0]
    coords = tuple(reversed(place['Point']['coordinates'][:-1]))
    try:
        address_dict = place['AddressDetails']['Country']['AdministrativeArea']
        state = address_dict['AdministrativeAreaName']
    except:
        # No state found in the Google Maps search.
        state = None
    return state, coords


def haversine(origin, destination):
    """
    Find the distance between locations in miles.
    Stack Overflow:  http://stackoverflow.com/questions/4913349/

    >>> haversine((32, 90), (33, 127))
    2148.31523223
    """
    equatorial_radius = 3963
    if not hasattr(origin, 'index') or not hasattr(destination, 'index'):
        raise ValueError('You did not pass in two iterables.')
    lat, lng = map(radians, origin)
    dest_lat, dest_lng = map(radians, destination)
    # Now for the Haversine formula...
    d_lng = dest_lng - lng
    d_lat = dest_lat - lat
    # One letter variables for the lose.
    a = sin(d_lat/2)**2 + cos(lat) * cos(dest_lat) * sin(d_lng/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = equatorial_radius * c
    return distance


def nearest_facility(state, coords):
    """Find the closest radiation facility given a state and coordinates."""
    radiation_facilities = RADIATION_FACILITIES
    if state in radiation_facilities:
        # Make sure template states closest radiation facility in your state.
        nearby = radiation_facilities[state]
    else:
        nearby = radiation_facilities['all']
    closest, mileage = None, None
    for facility in nearby:
        # Haversine formula against origin and destination.
        miles_apart = haversine(coords, facility)
        if not closest or mileage > miles_apart:
            closest = facility
            mileage = miles_apart
    return closest, mileage


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
