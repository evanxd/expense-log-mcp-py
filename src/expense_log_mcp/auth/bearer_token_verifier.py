from fastmcp.server.auth import TokenVerifier
from fastmcp.server.auth.auth import AccessToken

class BearerTokenVerifier(TokenVerifier):
    def __init__(self, client_id: str, token: str, **kwargs):
        super().__init__(**kwargs)
        self.client_id = client_id
        self.token = token

    async def verify_token(self, token: str) -> AccessToken | None:
        if token == self.token:
            return AccessToken(
                client_id=self.client_id,
                expires_at=None,
                scopes=["read", "write"],
                token=token,
            )
        return None
