## Package and Module Architecture

This rule defines the unified directory structure and dependency boundaries for the entire project:

```
src/
├── core/                 # Functional Core (pure, no side effects)
│   ├── models/           # Immutable value objects and entities
│   ├── use_cases/        # Pure functions with business rules
│   ├── ports/            # Interfaces only (Protocols)
│   │   ├── order_ports.py
│   │   └── payment_ports.py
│   └── workflows/        # Pure definitions of workflows
│       ├── checkout.py
│       └── payment_processing.py
│
├── shell/                # Imperative Shell (coordinates side effects)
│   ├── adapters/         # Ports implementations (Hexagonal Architecture)
│   │   ├── db/           # Database implementations
│   │   ├── api/          # API Handlers
│   │   └── external/     # Integrations with external services
│   │
│   └── orchestrators/    # Flow Coordinators (Orchestrator Pattern)
│       ├── checkout_orchestrator.py
│       └── payment_orchestrator.py
│
└── app.py                # Composition root for dependency injection
```

**Note:** `src/shell/adapters/` corresponds to the `src/adapters/` concept from Hexagonal Architecture, adapted for the FCIS context.

Dependency rules:
- Dependencies must flow inward: shell → core
- No circular dependencies between packages
- Stable packages (core) must not depend on unstable packages (shell)
- Maximum 4 dependencies per orchestrator (enforces single responsibility)

Port naming conventions:
- Primary (driving) ports: `*CommandPort`, `*QueryPort`
- Secondary (driven) ports: `*GatewayPort`, `*RepositoryPort`, `*PublisherPort`

Example implementation:
```python
# src/core/ports/order_ports.py
from typing import Protocol
from .models import Order, OrderId

class OrderCommandPort(Protocol):
    def create_order(self, order: Order) -> OrderId: ...
    def cancel_order(self, order_id: OrderId) -> None: ...

# src/shell/adapters/db/order_repository.py
from src.core.ports.order_ports import OrderCommandPort

class PostgresOrderRepository(OrderCommandPort):
    def __init__(self, connection_pool):
        self.pool = connection_pool
```

Dependency validation:
```python
def test_core_does_not_depend_on_shell():
    """Verify architectural boundaries"""
    violations = get_dependency_violations(
        source_package="src.core",
        forbidden_dependencies=["src.shell"]
    )
    assert not violations, f"Core depends on shell: {violations}"
```

Anti-patterns to avoid:
❌ Domain/core objects importing infrastructure packages  
❌ Naming ports `IService`, `IHandler` — too vague  
❌ Orchestrators containing business rules or calculations  
❌ Orchestrators with >4 dependencies  
❌ Core modules importing from shell package