
# Sootty Timing Expressions:

Sootty provides a temporal-logic language that is used to define the bounds of the displayed window. This language can select points in time within time-series data. Each expression represents the value of a n-bit vector over time. The language allows for both combinational expressions that are time-independent and some temporal expressions, including from, after, until, etc., that are time-dependent. The selected points in time for a given expression are defined as following each rising edge of the wire. When only a single point is needed, the first rising edge is used and the rest are discarded.

The grammar for the temporal logic expression is described below:

## Grammar
*exp* ∈ Expression := *wire* | *type* *num* | *unop* *exp* | *exp* *binop* *exp* | *timeop* *exp*

*wire* ∈ Identifier (e.g., `clk`, `data`, ...)

*type* ∈ Types := `const` | `time`

*num* ∈ Number (e.g., `0`, `1`, `2`, ...)

*unop* ∈ UnaryOps := `!` | `-` | `~`

*binop* ∈ BinaryOps := `&` | `|` | `&&` | `||` | `^` | `==` | `!=` | `>` | `>=` | `<` | `<=` | `<<` | `>>` | `+` | `-` | `%`  

*timeop* ∈ TimeOps := `from` | `after` | `until` | `before` | `next` | `prev` | *num* `next` | *num* `prev` | `acc`

## Explanation for selected examples

`x` — A wire with pre-defined values at each point in time.

`time 4` — A wire with value 0 from until time 3, and value 1 from time 4 and after.

`const 5` — A wire with a constant value of 5 at all points in time.

`x == const 5` — A wire with value 1 during all points when the value of x equals 5, and a 0 otherwise.

`x & y` — A wire defined as the bitwise and of the values of x and y at each point in time.

`x ^ y` — A wire defined as the bitwise xor of the values of x and y at each point in time.

`x && y` — A wire defined as the logical and of the values of x and y at each point in time.

`x || y` — A wire defined as the logical or of the values of x and y at each point in time.

`x << const 1` — A wire defined as the values of x shifted left by 1 at each point in time.

`from x` — A wire with value 1 for all points including and after the first rising edge of x, and value 0 otherwise.

`after x` — A wire with value 1 for all points after the first rising edge of x, and value 0 otherwise.

`until x` — A wire with value 1 for all points including and before the first rising edge of x, and value 0 otherwise.

`before x` — A wire with value 1 for all points after the first rising edge of x, and value 0 otherwise.

`next x` — A wire with the value of x at time t+1 shifted to time t.

`3 prev x` — A wire with the value of x at time t-3 shifted to time t.

`acc clk` — A wire with a value equal to the number of rising edges of clk before each point in time. (The accumulated sum of values)

## Operator Precedence

The operator precendence defined in the grammar is as follows in descending order.

- Modulus — `%`
- Add, Subtract — `+` | `-`
- Left Shift, Right Shift — `<<` | `>>`
- Bitwise operators — `&` | `|` | `^`
- Relational operators — `==` | `!=` | `>` | `>=` | `<` | `<=`
- Logical operators — `&&` | `||`