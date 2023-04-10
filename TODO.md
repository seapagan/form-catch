# TODO

- add logging to file for any errors
- check if the supplied email address is valid on site creation, fail if not
- add User Authentication and Authorization, users should not be able to mess
  with or even list any other users sites. Add Admin users who can do all.
- implement `read-only` mode where sites cannot be added/edited/deleted, only
  allow to catch data for existing sites. This would be helpful to lockdown a
  single-site service after setting up your site.
- add test for empty form data, don't send email if so.
