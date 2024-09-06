""" Tailscale webfinger responder

based on info here: https://www.authelia.com/integration/openid-connect/tailscale/
"""

from functools import lru_cache
import os
from typing import Any, Dict
from fastapi import FastAPI, HTTPException, Request
import uvicorn


app = FastAPI()


def uvicorn_run():
    uvicorn.run("tailscale_webfinger:app", host=os.getenv('LISTEN_HOST', '127.0.0.1'))


@lru_cache()
def get_oidc_url() -> str:
    """makes the OIDC URL"""
    return f"https://{os.getenv('KANIDM_DOMAIN')}/oauth2/openid/{os.getenv('CLIENT_ID')}/.well-known/openid-configuration"


# KANDIM_FRONTEND = os.getenv("KANIDM_DOMAIN")
# TAILSCALE_CLIENT_ID = os.getenv("CLIENT_ID")

# OIDC_URL = f"https://{KANDIM_FRONTEND}/oauth2/openid/{TAILSCALE_CLIENT_ID}/.well-known/openid-configuration"


@app.get("/.well-known/webfinger")
async def webfinger(request: Request) -> Dict[str, Any]:
    resource = request.query_params.get("resource")
    rel = request.query_params.get("rel")

    if rel is None or resource is None:
        raise HTTPException(
            status_code=400, detail="Bad Request: either rel or resource were empty"
        )
    elif resource.split(":")[0] != "acct":
        raise HTTPException(
            status_code=400, detail="Bad Request, resource must be an acct URI"
        )
    return {
        "subject": resource,
        "links": [
            {
                "rel": rel,
                "href": get_oidc_url(),
            }
        ],
    }
