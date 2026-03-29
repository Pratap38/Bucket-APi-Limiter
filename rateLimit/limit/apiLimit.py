import time 
import logging

logger=logging.getLogger (__name__)


class TokenBucket:

    def __init__(self,capacity,refillRate):
        self.capacity=capacity
        self.tokens=capacity
        self.refillRate=refillRate
        self.lastRefillRate=time.time()

        logger.info(f"new bucket {capacity}, Refill {refillRate}")
        
    def _refill(self):
        now=time.time()
        timePassed=time.time()-self.lastRefillRate
        newTokens=timePassed*self.refillRate

        oldTokens=self.tokens
        self.tokens=min(self.capacity,self.tokens+newTokens)
        self.lastRefillRate=now
        if newTokens>0:
            logger.info(f"refill rate {timePassed} token {oldTokens} ")
            
    def allowUser(self):
        self._refill()  # ✅ FIXED - Parentheses lagaye!
        if self.tokens>=1:
            self.tokens-=1
            logger.info(f"rquest allow remain {self.tokens: .2f}")
            return True
        else:
            logger.warning("no token left")
            return False
    
    def get_status(self):
        """Status check karne ke liye"""
        self._refill()
        return {
            'current_tokens': round(self.tokens, 2),
            'capacity': self.capacity,
            'refill_rate': self.refillRate
        }