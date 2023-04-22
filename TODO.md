# TODO

## General planned improvements

- [ ] add logging to file for any errors
- [ ] check if the supplied email address is valid on site creation, fail if not
- [ ] add User Authentication and Authorization, users should not be able to mess
  with or even list any other users sites. Add Admin users who can do all.
- [x] implement `read-only` mode where sites cannot be added/edited/deleted, only
  allow to catch data for existing sites. This would be helpful to lockdown a
  single-site service after setting up your site. [`Implemented as
  'lockdown'`]
- [ ] add test for empty form data, don't send email if so.
- [ ] version the API endpoints for future-proofing.
- [x] add an 'echo' form_id that will simply echo the results back to you (for
  testing)
- [ ] implement spam protection. Can use `Botpoison`, `reCAPTCHA`, `Akismet` etc
- [ ] optionally send the submitted data back to the redirect URL so it can be
  personalised.
- [ ] display a generic redirect page if one is not provided, with a link back to
  the original site. Add our branding 😁 but allow minor customisation.
- [ ] integrate with Slack, Google Sheets, Discord, Whatsapp and more
- [ ] add Webhooks
- [ ] add full testing suite

## Once User Auth is implemented

- [ ] show user stats for their form endpoint
- [ ] save the submitted data so it can be viewed online
- [ ] option to export above saved data to CSV and others
