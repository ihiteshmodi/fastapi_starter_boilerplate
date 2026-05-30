from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

app = FastAPI()
bearer = HTTPBearer(auto_error=False)


def decode_token(token: str) -> dict:
    # Replace with real JWT verification.
    if token != "valid-token":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"sub": "user-123", "role": "admin"}


def require_current_user(
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
) -> dict:
    if creds is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return decode_token(creds.credentials)


@app.get("/users/me")
async def get_me(current_user: Annotated[dict, Depends(require_current_user)]):
    return {"user_id": current_user["sub"], "role": current_user["role"]}
