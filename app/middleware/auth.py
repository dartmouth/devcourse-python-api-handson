from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

SECRET_TOKEN = "your-secret-token"  # This should not live in your code!


async def verify_bearer_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> bool:
    token = credentials.credentials  # Extract string token
    print(token)
    # Validate the token
    if token == SECRET_TOKEN:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
