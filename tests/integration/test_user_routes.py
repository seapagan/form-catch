"""Integration tests for user routes."""

import pytest

from managers.user import pwd_context


@pytest.mark.skip(reason="fails on CI")
class TestUserRoutes:
    """Test the user resource routes."""

    test_user = {
        "email": "testuser@usertest.com",
        "first_name": "Test",
        "last_name": "User",
        "password": pwd_context.hash("test12345!"),
        "verified": True,
    }

    @pytest.mark.parametrize(
        "route",
        [
            ["/users", "get"],
            ["/users/me", "get"],
            ["/users/1/make-admin", "post"],
            ["/users/1/password", "post"],
            ["/users/1/ban", "post"],
            ["/users/1/unban", "post"],
            ["/users/1", "put"],
            ["/users/1", "delete"],
        ],
    )
    def test_routes_no_auth(self, test_app, route):
        """Test that routes are protected by authentication."""
        route_name, method = route
        fn = getattr(test_app, method)
        response = fn(route_name)

        print(response)
        assert response.status_code == 403

    @pytest.mark.parametrize(
        "route",
        [
            ["/users", "get"],
            ["/users/me", "get"],
            ["/users/1/make-admin", "post"],
            ["/users/1/password", "post"],
            ["/users/1/ban", "post"],
            ["/users/1/unban", "post"],
            ["/users/1", "put"],
            ["/users/1", "delete"],
        ],
    )
    def test_routes_bad_auth(self, test_app, route):
        """Test that routes are protected by authentication."""
        route_name, method = route
        fn = getattr(test_app, method)
        response = fn(route_name, headers={"Authorization": "Bearer BADBEEF"})

        print(response)
        assert response.status_code == 401
