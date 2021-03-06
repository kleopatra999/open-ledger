import pytest

from openledger import licenses
from openledger.handlers import handler_500px, handler_flickr

def test_license_match_simple():
    """The license_match() function should match an array of license names
    to a comma-separated string of values from a partner mapping"""
    mapping = handler_500px.LICENSES
    assert '4' == licenses.license_match(["BY"], mapping)
    assert '1,4' == licenses.license_match(["BY", "BY-NC"], mapping)

    mapping = handler_flickr.LICENSES
    assert '4' == licenses.license_match(["BY"], mapping)
    assert '2,7' == licenses.license_match(["BY-NC", "PDM"], mapping)

def test_license_match_unknown_license():
    """The license match function should ignore unknown licenses"""
    mapping = handler_flickr.LICENSES
    assert None == licenses.license_match(["UNKNOWN"], mapping)

def test_license_match_partial_unknown_license():
    """The license match function should ignore unknown licenses
    but still include known ones"""
    mapping = handler_flickr.LICENSES
    assert '4' == licenses.license_match(["UNKNOWN", "BY"], mapping)

def test_license_match_groups():
    """The license match function should expand out logical groups of licenses"""
    mapping = handler_flickr.LICENSES
    assert '1,2,3,4,5,6,7,9' == licenses.license_match(["ALL"], mapping)
    assert '1,2,3,4,5,6' == licenses.license_match(["ALL-CC"], mapping)
    assert '4,5,6,7,9' == licenses.license_match(["ALL-$"], mapping)
    assert '1,2,4,5,7,9' == licenses.license_match(["ALL-MOD"], mapping)

def test_license_match_groups_intersection():
    """The license match function should return the intersection of multiple groups, not the union"""
    mapping = handler_flickr.LICENSES
    assert '4,5,7,9' == licenses.license_match(["ALL-$", "ALL-MOD"], mapping)

def test_license_map_version():
    """The license match function should return a special `version` key that includes
    the correct static license version associated with each provider"""
    license_map = licenses.license_map_from_partners()
    assert "1.0" == license_map['rijks']['version']
    assert "1.0" == license_map['wikimedia']['version']
    assert "3.0" == license_map['fpx']['version']
    assert "2.0" == license_map['flickr']['version']

def test_license_map_lookup():
    """The license map function should return a known key for a license value by provider"""
    license_map = licenses.license_map_from_partners()
    assert "CC0" == license_map['fpx'][8]
    assert "CC0" == license_map['flickr'][9]

def test_license_map_pd_sources():
    """The license map function should return a value of CC0 for a default lookup of 0"""
    license_map = licenses.license_map_from_partners()
    assert "CC0" == license_map['wikimedia'][0]
    assert "CC0" == license_map['rijks'][0]

def test_get_license_url_license():
    """The license URL method should return the expected URL for a license type"""
    assert "https://creativecommons.org/licenses/by/4.0" == licenses.get_license_url("by", "4.0")
    assert "https://creativecommons.org/licenses/by-sa/4.0" == licenses.get_license_url("by-sa", "4.0")
    assert "https://creativecommons.org/licenses/by-nc/4.0" == licenses.get_license_url("by-nc", "4.0")
    assert "https://creativecommons.org/licenses/by-nc-nd/4.0" == licenses.get_license_url("by-nc-nd", "4.0")
    assert "https://creativecommons.org/licenses/by-nc-sa/4.0" == licenses.get_license_url("by-nc-sa", "4.0")

def test_get_license_url_version():
    """The license URL method should return the expected URL for a license version"""
    assert "https://creativecommons.org/licenses/by/3.0" == licenses.get_license_url("by", "3.0")
    assert "https://creativecommons.org/licenses/by-sa/3.0" == licenses.get_license_url("by-sa", "3.0")
    assert "https://creativecommons.org/licenses/by-nc/3.0" == licenses.get_license_url("by-nc", "3.0")
    assert "https://creativecommons.org/licenses/by-nc-nd/3.0" == licenses.get_license_url("by-nc-nd", "3.0")
    assert "https://creativecommons.org/licenses/by-nc-sa/3.0" == licenses.get_license_url("by-nc-sa", "3.0")

def test_get_license_url_no_version():
    """The license URL method should return an exception if not passed a version"""
    with pytest.raises(Exception) as exc:
        licenses.get_license_url("by", None)
    assert 'No version' in str(exc.value)

def test_get_license_url_no_license():
    """The license URL method should return an exception if not passed a license"""
    with pytest.raises(Exception) as exc:
        licenses.get_license_url(None, "3.0")
    assert 'No license' in str(exc.value)

def test_get_license_url_unknown_license():
    """The license URL method should return None if passed an unknown license"""
    assert licenses.get_license_url("FAKE", "3.0") is None

def test_get_license_url_pd_licenses():
    """The license URL method should return the correct public domain licenses regardless of version"""
    assert "https://creativecommons.org/publicdomain/zero/1.0" == licenses.get_license_url("cc0", "10.0")
    assert "https://creativecommons.org/publicdomain/mark/1.0" == licenses.get_license_url("pdm", "10.0")
