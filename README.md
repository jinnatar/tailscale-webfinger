# tailscale-webfinger

Responds with the OIDC endpoint based on a few config things.

## Startup

You'll need poetry, or make a virtualenv and pip install the repo.

```shell
git clone <repo url> && cd <repo name>
poetry install
poetry run tailscale-webfinger
```

## Environment vars

- KANIDM_DOMAIN - the hostname of your Kanidm server
- CLIENT_ID - the client ID of the Tailscale config on your Kanidm server
- LISTEN_HOST - the host to listen to, defaults to `127.0.0.1`

It'll respond with this if you have `idp.example.com`and `tailscale` respectively:

```json
{"subject":"acct:user@example.com`","links":[{"rel":"http://openid.net/specs/connect/1.0/issuer","href":"https://idp.example.com/oauth2/openid/tailscale/.well-known/openid-configuration"}]}
```
