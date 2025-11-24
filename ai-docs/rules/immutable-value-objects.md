## Value Objects and Immutability

This rule enforces immutability for domain objects in the core layer to ensure data integrity and referential transparency:

Value objects must be immutable to enable:
- Reliable reasoning about program behavior
- Safe sharing across threads without synchronization
- Simplified testing without setup/teardown complexity

Core implementation pattern:
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int
    
    def with_quantity(self, new_qty: int) -> "OrderLine":
        """Return new instance with updated quantity"""
        return OrderLine(orderid=self.orderid, sku=self.sku, qty=new_qty)
```

Value objects follow functional programming principles:
- Once created, their state never changes
- Operations on value objects return new instances
- They can be safely shared across threads

Immutability verification test:
```python
def test_orderline_immutable():
    """Verify value objects cannot be modified after creation"""
    line = OrderLine(orderid="123", sku="BOOK", qty=2)
    with pytest.raises(FrozenInstanceError):
        line.qty = 3
```

Package location requirements:
- Value objects must reside in the domain layer
- No infrastructure dependencies allowed in value object modules

Anti-patterns to avoid:
❌ Domain/core objects importing infrastructure packages
❌ Concrete implementations in domain layer
❌ Infrastructure concerns leaking into application or domain layers

**Verification:**
- Code reviews must check for `@dataclass(frozen=True)` in domain models
- Static analysis should flag mutable classes in domain layer
- Unit tests should verify immutability where critical to business rules

**Note:** This rule focuses specifically on immutable value objects in the core layer. General rules about the Functional Core (pure functions, no side effects) are defined in the "Functional Core & Imperative Shell" document. Thread safety and performance implications of immutability are implementation details to be considered during code review.