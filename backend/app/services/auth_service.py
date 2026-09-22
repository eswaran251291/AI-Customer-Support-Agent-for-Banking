"""Authentication and security services."""

import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import jwt
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class AuthService:
    """Service for authentication and MFA."""
    
    @staticmethod
    async def verify_mfa_token(mfa_token: str, user_id: str) -> bool:
        """
        Verify MFA token for user.
        
        Args:
            mfa_token: MFA verification token (SMS/Email code or authenticator token)
            user_id: User identifier
            
        Returns:
            True if valid, False otherwise
        """
        logger.info(f"Verifying MFA token for user: {user_id}")
        
        # Mock MFA verification
        # In production, this would verify against:
        # - SMS codes sent to registered phone
        # - Email verification links
        # - TOTP authenticator tokens
        # - Biometric verification
        
        if not mfa_token or len(mfa_token) < 4:
            logger.warning(f"Invalid MFA token format for user: {user_id}")
            return False
        
        # Mock: Accept tokens starting with "mfa_" for demo
        # In production, validate against stored MFA credentials
        is_valid = mfa_token.startswith("mfa_") or mfa_token == "123456"
        
        if is_valid:
            logger.info(f"MFA verification successful for user: {user_id}")
        else:
            logger.warning(f"MFA verification failed for user: {user_id}")
        
        return is_valid
    
    @staticmethod
    async def generate_jwt_token(user_id: str, expires_in_minutes: int = 30) -> str:
        """
        Generate JWT authentication token.
        
        Args:
            user_id: User identifier
            expires_in_minutes: Token expiration time
            
        Returns:
            JWT token string
        """
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(minutes=expires_in_minutes),
            "iat": datetime.utcnow(),
            "type": "access"
        }
        
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        logger.info(f"Generated JWT token for user: {user_id}")
        return token
    
    @staticmethod
    async def verify_jwt_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Verify JWT token and extract claims.
        
        Args:
            token: JWT token to verify
            
        Returns:
            Token claims dict or None if invalid
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            logger.info(f"JWT token verified for user: {payload.get('user_id')}")
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JWT token: {str(e)}")
            return None
    
    @staticmethod
    async def create_session(user_id: str, session_duration_minutes: int = 60) -> Dict[str, Any]:
        """
        Create new session for user.
        
        Args:
            user_id: User identifier
            session_duration_minutes: Session duration
            
        Returns:
            Session info dict
        """
        session_token = await AuthService.generate_jwt_token(
            user_id, 
            expires_in_minutes=session_duration_minutes
        )
        
        logger.info(f"Session created for user: {user_id}")
        
        return {
            "session_id": f"session_{user_id}_{datetime.utcnow().timestamp()}",
            "user_id": user_id,
            "token": session_token,
            "expires_at": (datetime.utcnow() + timedelta(minutes=session_duration_minutes)).isoformat(),
            "created_at": datetime.utcnow().isoformat()
        }
