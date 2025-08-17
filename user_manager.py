from typing import Dict, List, Optional
from config import ROLES, DEFAULT_ROLE

class UserManager:
    def __init__(self):
        self.users: Dict[int, Dict] = {}
    
    def get_user(self, user_id: int) -> Dict:
        """Get or create a user session"""
        if user_id not in self.users:
            self.users[user_id] = {
                "role": DEFAULT_ROLE,
                "conversation": [],
                "name": None,
                "partner_name": None  # Store partner name for partner roles
            }
        return self.users[user_id]
    
    def set_user_role(self, user_id: int, role: str) -> bool:
        """Set user's selected role"""
        try:
            if role in ROLES:
                user = self.get_user(user_id)
                user["role"] = role
                print(f"✅ User {user_id} role changed to: {role}")
                return True
            else:
                print(f"❌ Invalid role '{role}' for user {user_id}")
                return False
        except Exception as e:
            print(f"❌ Error setting role for user {user_id}: {e}")
            return False
    
    def get_user_role(self, user_id: int) -> str:
        """Get user's current role"""
        user = self.get_user(user_id)
        return user["role"]
    
    def add_message(self, user_id: int, role: str, content: str):
        """Add a message to user's conversation history"""
        user = self.get_user(user_id)
        user["conversation"].append({
            "role": role,
            "content": content,
            "timestamp": None  # Could add timestamp if needed
        })
        
        # Keep only last 20 messages to prevent memory issues
        if len(user["conversation"]) > 20:
            user["conversation"] = user["conversation"][-20:]
    
    def get_conversation(self, user_id: int) -> List[Dict]:
        """Get user's conversation history"""
        user = self.get_user(user_id)
        return user["conversation"]
    
    def clear_conversation(self, user_id: int):
        """Clear user's conversation history"""
        user = self.get_user(user_id)
        user["conversation"] = []
    
    def set_user_name(self, user_id: int, name: str):
        """Set user's name"""
        user = self.get_user(user_id)
        user["name"] = name
    
    def get_user_name(self, user_id: int) -> Optional[str]:
        """Get user's name"""
        user = self.get_user(user_id)
        return user["name"]
    
    def set_partner_name(self, user_id: int, partner_name: str):
        """Set partner name for partner roles"""
        user = self.get_user(user_id)
        user["partner_name"] = partner_name
        print(f"✅ User {user_id} partner name set to: {partner_name}")
    
    def get_partner_name(self, user_id: int) -> Optional[str]:
        """Get partner name for partner roles"""
        user = self.get_user(user_id)
        return user.get("partner_name")
    
    def clear_partner_name(self, user_id: int):
        """Clear partner name when switching away from partner roles"""
        user = self.get_user(user_id)
        user["partner_name"] = None
        print(f"✅ User {user_id} partner name cleared")
    
    def get_available_roles(self) -> Dict[str, Dict]:
        """Get all available roles"""
        return ROLES 