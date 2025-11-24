## Functional Core & Imperative Shell (FCIS)

This rule enforces strict separation between pure logic and side effects:

Core functions must be:
- Pure (no I/O, no mutation of inputs, no time/random)
- Small (≤15 lines; ≤3 parameters)
- Named with clear verb + domain object
- Follow CQS: Queries (`calculate_total`) vs. Commands (`update_status`) — never both
- Must reside in `src/core/` directory structure

Shell functions must be:
- Thin wrappers (≤25 lines) around core logic
- Responsible for: I/O, error translation, logging, retries
- Contain `try/except` blocks only — extracted into helpers like `execute_with_retry(fn, max_retries=3)`
- Must reside in `src/shell/` directory structure

Retry helper implementation:
```python
import time

def execute_with_retry(fn, max_retries=3):
    """Execute function with retry strategy"""
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(1)  # Fixed delay between retries
```

Examples:
```python
# ✅ Core (pure)
def calculate_total(order: Order, tax_rates: TaxTable) -> Money:
    subtotal = sum(item.price * item.qty for item in order.items)
    tax = subtotal * tax_rates.rate_for(order.region)
    return subtotal + tax

# ✅ Shell (side-effectful)
def handle_create_order_request(request: OrderRequest) -> Response:
    try:
        order = Order.from_request(request)
        total = calculate_total(order, global_tax_table)
        persisted = order_repository.save(order.with_total(total))
        return Response.json(OrderDTO.from_model(persisted))
    except OrderValidationError as e:
        return Response.error(400, f"Invalid order: {e}")
```

Exception handling:
- Domain exceptions defined in core (e.g., `OutOfStock`, `InvalidEmail`)
- Shell translates domain exceptions to appropriate response formats
- No exception handling in core functions (let exceptions propagate)

Core must never contain:
- Database calls, HTTP requests, file operations
- Random number generation, current time usage
- Direct mutation of input parameters
- Global state access or modification

**Verification:**
- Unit tests must target Functional Core only
- Core functions must pass in <100ms each
- Unit test naming pattern: `test_<function>_<scenario>_<expectation>`

Core functions should aim for low cyclomatic complexity:
- Prefer simple, linear execution paths
- Extract complex conditionals into separate pure functions

Anti-patterns to avoid:
❌ Core function calling `requests.get()` or database operations  
❌ Shell function containing business rules (e.g., "if user is premium, apply 10% off")  
❌ Command function returning computed values (e.g., `save_user(user) -> UserDTO`)  
❌ Direct mutation of input parameters in core functions  
❌ Using global state or singletons in core logic  
❌ Implementing retries or circuit breakers in core functions  