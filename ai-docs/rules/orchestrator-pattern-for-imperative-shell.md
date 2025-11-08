## Purpose
Define the Orchestrator pattern as the primary coordination mechanism for the Imperative Shell layer, ensuring strict separation between workflow coordination and business logic.

## Guidelines
Orchestrators must contain no business logic:
- Only sequence operations and handle integration concerns
- Maximum 4 dependencies per orchestrator (enforces single responsibility)
- All business rules must reside in Functional Core

Core provides pure workflow definitions:
- Core defines what needs to happen (the workflow specification)
- Orchestrators execute how it happens (the workflow coordination)
- Core functions must be pure with explicit input/output types

Explicit error handling strategies:
- Define retry, fallback, and compensation patterns at orchestration level
- Never bury error handling strategies in Core business logic
- Use domain-specific exceptions from Core, infrastructure exceptions in Shell

Stateless orchestrators:
- No internal state beyond current workflow execution context
- All state must be passed explicitly as parameters
- Orchestrators must be safe to recreate at any point

## Directory structure:
src/
├── core/
│   └── workflows/          # Pure workflow definitions and business rules
│       ├── checkout.py
│       └── payment_processing.py
└── shell/
    └── orchestrators/      # Imperative workflow coordinators
        ├── checkout_orchestrator.py
        └── payment_orchestrator.py

## Implementation example:
```python
# src/core/workflows/checkout.py
from dataclasses import dataclass
from typing import NewType, List

UserId = NewType("UserId", str)
OrderId = NewType("OrderId", str)

@dataclass(frozen=True)
class User:
    id: UserId
    is_verified: bool
    payment_method: str

@dataclass(frozen=True)
class CartItem:
    id: str
    price: float
    quantity: int

def validate_checkout(user: User, items: List[CartItem]) -> None:
    """Pure validation with no side effects"""
    if not user.is_verified:
        raise PermissionError("User not verified")
    # Additional validation logic...

# src/shell/orchestrators/checkout_orchestrator.py
from src.core.workflows.checkout import User, CartItem, validate_checkout
from src.shell.adapters import UserRepository, PaymentGateway

class CheckoutOrchestrator:
    """Coordinates workflow without containing business logic"""
    
    def __init__(self, user_repo: UserRepository, payment_gateway: PaymentGateway, logger):
        # Maximum 4 dependencies enforced
        self.user_repo = user_repo
        self.payment_gateway = payment_gateway
        self.logger = logger
    
    def process_checkout(self, user_id: str, cart_items: list) -> dict:
        try:
            # 1. Get data from external sources
            user_data = self.user_repo.get_by_id(user_id)
            
            # 2. Convert to Core types
            user = User(
                id=UserId(user_data["id"]),
                is_verified=user_data["is_verified"],
                payment_method=user_data["payment_method"]
            )
            items = [CartItem(**item) for item in cart_items]
            
            # 3. Execute pure Core functions
            validate_checkout(user, items)
            
            # 4. Coordinate side effects
            payment_result = self._process_payment(user, items)
            return {"status": "success", "payment_id": payment_result["id"]}
            
        except Exception as e:
            self.logger.error(f"Checkout failed: {str(e)}")
            self._handle_failure(items)
            raise
```

## Verification
- Code reviews must verify orchestrators contain no business logic
- Static analysis checks for dependency count in orchestrator constructors
- Tests must verify orchestrators can be recreated without losing workflow state

## Anti-Patterns
❌ Orchestrators containing business rules or calculations
❌ Orchestrators with >4 dependencies (violates single responsibility)
❌ Mixing domain exceptions with infrastructure exceptions
❌ Stateful orchestrators that maintain workflow state between calls
❌ Core modules importing from shell/orchestrators package