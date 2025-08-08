# Session 001: Python Decorators and Dataclasses

## Date: 2025-08-08
## Topics: Decorators, Dataclasses, field(default_factory), __post_init__

---

## 1. The Mutable Default Problem and field(default_factory)

### The Problem
In Python, default parameter values are evaluated once when the function/class is defined, not each time it's called. This creates issues with mutable defaults:

```python
# DANGER: All instances share the same dict!
@dataclass
class BadExample:
    data: dict = {}  # This dict is shared across ALL instances
```

### The Solution
Use `field(default_factory=callable)` to create a new object for each instance:

```python
from dataclasses import dataclass, field

@dataclass
class GoodExample:
    data: dict = field(default_factory=dict)  # Each instance gets its own dict
    items: list = field(default_factory=list)  # Each instance gets its own list
    id: str = field(default_factory=lambda: str(uuid.uuid4()))  # Computed default
```

**Key Point:** `default_factory` takes a callable (function/class) that's called fresh for each new instance.

---

## 2. Python Decorators

### Core Concept
Decorators are functions that modify or enhance other functions/classes. They wrap the original function with additional functionality.

### Basic Structure
```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        # Before the function
        result = func(*args, **kwargs)
        # After the function
        return result
    return wrapper

@my_decorator
def my_function():
    pass

# Equivalent to: my_function = my_decorator(my_function)
```

### How They Work
1. Python sees `@decorator` above a definition
2. After defining the function/class, Python passes it to the decorator
3. The decorator returns a modified version
4. That version replaces the original

### Common Built-in Decorators
- `@property` - Makes a method behave like an attribute
- `@staticmethod` - Method doesn't need self/cls
- `@classmethod` - Method receives class as first arg
- `@dataclass` - Auto-generates class methods
- `@functools.cache` - Memoization

### Decorators with Arguments
```python
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    print(f"Hello {name}")
```

---

## 3. Dataclasses

### Purpose
Automatically generate boilerplate code for classes that primarily store data. Reduces repetitive code for `__init__`, `__repr__`, `__eq__`, etc.

### Before vs After
```python
# Traditional Class
class Position:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Position(x={self.x}, y={self.y})"
    
    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y

# With Dataclass
from dataclasses import dataclass

@dataclass
class Position:
    x: float
    y: float
    # All methods auto-generated!
```

### What Gets Generated
1. `__init__` - Constructor from annotated fields
2. `__repr__` - String representation
3. `__eq__` - Equality comparison
4. `__hash__` - If `frozen=True`
5. Comparison methods - If `order=True`

### Configuration Options
```python
@dataclass(
    init=True,      # Generate __init__
    repr=True,      # Generate __repr__
    eq=True,        # Generate __eq__
    frozen=False,   # Immutable if True
    order=False,    # Generate <, >, <=, >=
    slots=False     # Use __slots__ for memory
)
```

### Field Options
```python
@dataclass
class Example:
    # Basic field with default
    name: str = "default"
    
    # Mutable default (list/dict/set)
    items: list = field(default_factory=list)
    
    # Exclude from __repr__
    _internal: int = field(default=0, repr=False)
    
    # Not included in __init__
    computed: int = field(default=0, init=False)
    
    # Field with metadata
    tagged: str = field(metadata={'unit': 'meters'})
```

---

## 4. __post_init__ and Advanced Features

### __post_init__ Method
Runs automatically after the generated `__init__` completes. Used for:
- Validation
- Computing derived fields
- Complex initialization
- Type conversions

```python
@dataclass
class Sprite:
    image: pygame.Surface
    rect: pygame.Rect = field(init=False)  # Not in __init__
    
    def __post_init__(self):
        # Compute rect from image
        self.rect = self.image.get_rect()

@dataclass
class Temperature:
    celsius: float
    
    def __post_init__(self):
        # Validation
        if self.celsius < -273.15:
            raise ValueError("Below absolute zero!")
        # Computed field
        self.fahrenheit = self.celsius * 9/5 + 32
```

### InitVar: Initialization-Only Variables
Pass temporary values that aren't stored as fields:

```python
from dataclasses import dataclass, InitVar

@dataclass
class Player:
    name: str
    level: InitVar[int]  # Used in __post_init__ but not stored
    
    def __post_init__(self, level: int):
        # level is available here but won't be self.level
        self.health = level * 100
        self.mana = level * 50
```

### Inheritance
Dataclasses support inheritance, combining parent and child fields:

```python
@dataclass
class Entity:
    id: int
    position: Position

@dataclass
class Player(Entity):
    name: str
    health: int = 100
    # Player has: id, position, name, health
```

### Important Rules
1. **Type hints are required** - Only annotated attributes become fields
2. **Mutable defaults need default_factory** - Avoid shared state bugs
3. **Order matters with defaults** - Fields with defaults must come after fields without
4. **__post_init__ for complex logic** - Keep __init__ simple

---

## Practical Application in Our Game

### For Components (ECS)
```python
@dataclass
class Input:
    # Mutable default for key states
    keys_pressed: dict = field(default_factory=dict)
    
@dataclass
class Sprite:
    image: pygame.Surface
    rect: pygame.Rect = field(init=False)
    
    def __post_init__(self):
        self.rect = self.image.get_rect()
```

### Why This Matters for Our Project
1. **Components are data containers** - Dataclasses are perfect for ECS components
2. **Avoid shared state bugs** - Each entity needs its own component data
3. **Clean, readable code** - Less boilerplate, more game logic
4. **Type hints help IDEs** - Better autocomplete and error detection

---

## Key Takeaways

1. **Always use `default_factory` for mutable defaults** (lists, dicts, sets)
2. **Decorators modify behavior** - They wrap functions/classes with extra functionality
3. **Dataclasses eliminate boilerplate** - Perfect for data-holding classes like ECS components
4. **`__post_init__` handles complex initialization** - Validation, computation, derived fields
5. **Type hints are not optional in dataclasses** - They define what becomes a field

---

## Next Steps
- Implement proper Input component with field(default_factory=dict)
- Create more game components using dataclasses
- Consider using __post_init__ for component validation
- Explore frozen dataclasses for immutable game constants

---

## Addendum: Low-Level Python - Why default_factory?

### The Root Cause: Python's Object Model

**Everything in Python is a heap-allocated object** with:
- **PyObject header**: Reference count + type pointer
- **Object data**: The actual content

When you assign `x = 5`, Python doesn't copy the value - it creates a reference to a PyObject on the heap.

### Mutable vs Immutable: The Critical Difference

**Immutable Types (Safe as Defaults):**
- `int`, `float`, `str`, `tuple`, `frozenset`, `bytes`
- Cannot be modified after creation
- Multiple references don't cause problems
- Python even **interns** common values (small ints -5 to 256, common strings) for efficiency

**Mutable Types (Need default_factory):**
- `list`, `dict`, `set`, `bytearray`, custom objects
- Can be modified in-place
- Sharing references leads to unexpected shared state

### What Happens at the Low Level

```python
# WITHOUT default_factory - at class definition time:
class BadClass:
    items = []  # Creates ONE list object when class is defined

# Simplified C pseudocode of what happens:
PyObject* default_list = PyList_New(0);  // Allocate ONCE
class_dict["items"] = default_list;      // Store the reference

# Every instance creation:
instance1.items = class_dict["items"];  // Same reference!
instance2.items = class_dict["items"];  // Same reference!
```

```python
# WITH default_factory - at instance creation time:
@dataclass
class GoodClass:
    items: list = field(default_factory=list)

# What happens internally:
# Each __init__ call executes:
instance.items = list()  # Calls PyList_New(0) each time
# Fresh allocation for each instance!
```

### Why Not Copy Semantics?

Unlike C++ or Rust, Python has:
- **No value types** - Everything is a reference to a heap object
- **No implicit copying** - Assignment (`=`) creates references, not copies
- **No move semantics** - There's no expensive copying to optimize away
- **Explicit copying only** - Must use `copy.copy()` or `copy.deepcopy()`

This is why:
```python
a = [1, 2, 3]
b = a  # NOT a copy - b references the SAME list
b.append(4)
print(a)  # [1, 2, 3, 4] - a changed too!
```

### The Memory Layout

```
Immutable (int):
x = 5  -->  [RefCount: 2][Type: int][Value: 5]
y = 5  -->  (same object due to interning)

Mutable (list) without default_factory:
Class.default  -->  [RefCount: N][Type: list][Length][Items...]
instance1.attr -->  (all point to same object)
instance2.attr -->  

Mutable (list) with default_factory:
instance1.attr -->  [RefCount: 1][Type: list][Length][Items...]
instance2.attr -->  [RefCount: 1][Type: list][Length][Items...]
                    (separate objects)
```

### Key Insight

The need for `default_factory` isn't about heap allocation (everything is heap allocated) or copy/move semantics (Python doesn't have them). It's about **when the object is created**:
- **Without default_factory**: Object created once at class definition
- **With default_factory**: New object created for each instance

This distinction only matters for mutable types because immutable types can safely share references without side effects.

---

## Instance vs Class Variables in Dataclasses

### All Dataclass Fields Become Instance Variables

A critical clarification: **dataclass fields are always instance variables**, never class variables. The confusion arises from how defaults work:

```python
@dataclass
class Player:
    name: str                    # Instance variable (no default)
    health: int = 100           # Instance variable (with default)
    items: list = []            # Instance variable (DANGEROUS default)
    inventory: list = field(default_factory=list)  # Instance variable (safe default)
```

The generated `__init__` creates instance variables:
```python
def __init__(self, name: str, health: int = 100, items=_DEFAULT_LIST):
    self.name = name        # Instance var
    self.health = health    # Instance var
    self.items = items      # Instance var (but may share reference!)
    self.inventory = list() # Instance var (fresh list)
```

### The Mutable Default Problem Clarified

With `items: list = []`:
- `items` IS an instance variable on each object
- But all instances' `items` variables **reference the same list object**
- The list was created once at class definition time

```python
@dataclass
class BadDesign:
    items: list = []  # One list created at class definition

player1 = BadDesign()
player2 = BadDesign()
# player1.items and player2.items are different instance variables
# But they reference the SAME list object in memory!
```

### Mixing Class and Instance Variables

```python
from typing import ClassVar

@dataclass
class Entity:
    # Instance variables (included in __init__)
    id: int
    position: tuple = (0, 0)
    
    # Class variables (shared, NOT in __init__)
    entity_count: ClassVar[int] = 0  # Using ClassVar annotation
    _registry = {}  # No annotation = class variable
    
    def __post_init__(self):
        Entity.entity_count += 1  # Accessing class variable
        Entity._registry[self.id] = self
```

Rules:
- **Type annotation** → Instance variable (in `__init__`)
- **ClassVar[T] annotation** → Class variable (excluded from `__init__`)
- **No annotation** → Class variable (not a dataclass field)

---

## Frozen Dataclasses: Immutable Objects

### What Are Frozen Dataclasses?

Frozen dataclasses create **immutable instances** - once created, fields cannot be reassigned:

```python
@dataclass(frozen=True)
class Point:
    x: float
    y: float

p = Point(3, 4)
p.x = 5  # FrozenInstanceError: cannot assign to field 'x'
```

### What frozen=True Provides

1. **Read-only fields** - Overrides `__setattr__` and `__delattr__`
2. **Automatic `__hash__`** - Immutable objects are hashable
3. **Dict key / set compatibility** - Can use as dictionary keys

### Use Cases

```python
# Mathematical vectors
@dataclass(frozen=True)
class Vector2D:
    x: float
    y: float
    
    def __add__(self, other):
        # Must return new instance since we can't modify self
        return Vector2D(self.x + other.x, self.y + other.y)

# Configuration constants
@dataclass(frozen=True)
class GameConfig:
    screen_width: int = 800
    screen_height: int = 600
    fps: int = 60

# As dictionary keys
@dataclass(frozen=True)
class TileCoord:
    x: int
    y: int

tile_map = {
    TileCoord(0, 0): "grass",
    TileCoord(1, 0): "water",  # Works! TileCoord is hashable
}
```

### Frozen Limitations

**Shallow immutability** - Only field assignment is prevented:

```python
@dataclass(frozen=True)
class Container:
    items: list  # The field reference is frozen, not the list!

c = Container([1, 2, 3])
c.items = [4, 5]     # ERROR: Cannot reassign field
c.items.append(4)    # OK: List itself is still mutable
c.items[0] = 999     # OK: Modifying list contents
```

For deep immutability, use immutable types all the way down:
```python
@dataclass(frozen=True)
class TrulyImmutable:
    values: tuple  # Immutable collection
    name: str      # Immutable string
    count: int     # Immutable integer
```

### Benefits of Frozen Dataclasses

1. **Thread safety** - No synchronization needed for immutable objects
2. **Caching/memoization** - Safe to cache since they can't change
3. **Predictability** - No surprising mutations
4. **Performance** - Python can optimize immutable objects
5. **Functional style** - Encourages pure functions that return new objects

### When to Use Frozen

- **Value objects** - Points, vectors, colors, coordinates
- **Configuration** - Settings that shouldn't change at runtime
- **Dictionary keys** - When you need custom objects as keys
- **Multi-threading** - Shared data between threads
- **Game constants** - Tile types, entity stats, level data