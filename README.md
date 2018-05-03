# Example OpenID Connect Application using Okta and Flask
This sample application uses okta together with flask for authentication purposes.

I am publishing this because, as of now, any examples or tutorials on the subject are either non-existent or impossible to find.

First, you must register an okta application. Through the setup to create a new application, select 'Web', and use 'Authorization Code' for the 'Grant type allowed' section. Next, set 'Base URI' to `http://localhost:5000/` and 'Login redirect URI' to `http://localhost:5000/authn-callback`.

Then, set the `CLIENT_ID`, `CLIENT_SECRET`, and `OKTA_BASE_URL` environment variables to their respective values from Okta.

Example base url: `https://example.okta.com`
