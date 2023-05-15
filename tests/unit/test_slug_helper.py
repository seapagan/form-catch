"""Tests for slug helper functions."""


from helpers.slug import create_slug


def test_create_slug_default_length():
    """Test create_slug function."""
    slug = create_slug()
    assert isinstance(slug, str)
    assert len(slug) == 8


def test_create_slug_providing_length():
    """Test create_slug function while providing a length parameter."""
    slug_length = 10
    slug = create_slug(length=slug_length)
    assert isinstance(slug, str)
    assert len(slug) == slug_length
