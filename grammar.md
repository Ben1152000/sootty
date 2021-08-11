W := wire
    | S             <wire name>
    | const C       <constant>
    | time C        <time with value c>
    | ! W           <not when applied to any number gives zero>
    | W Lop W       <logical operation>
    | W Rop W       <relational operation>
    | - W           <negation>
    | W Aop W       <arithmetic operation>
    | from W        <time starting at t>
    | after W       <time starting after t>
    | until W       <time ending at t>
    | before W      <time ending before t>
    | next W        <shift all values left by one>
    | prev W        <shift all values right by one>
    | C next W      <shift all values left by c>
    | C prev W      <shift all values right by c>
    | acc W         <sum of all previous rising edges>
    | 

C := [integer]
S := [string]

Lop := &            <and>
    | |             <or>
    | ^             <xor>
    | ->            <implies>
    | =             <equivalent>

Rop := ==           <equals>
    | !=            <not equals>
    | >             <greater than>
    | >=            <greater than equals>
    | <             <less than>
    | <=            <less than equals>

Aop := +            <add>
    | -             <subtract>
    | >>            <shift right>
    | <<            <shift left>
    | %             <modulo>

S -> string

- The time a wire evaluates to is equal to the cycle of the first rising edge, or one after the last cycle otherwise

Examples:
- After five clock ticks, when ready and value are both high followed by data equalling 64:

```
after (acc clk == const 5) & ready & value & (next data == 64)
```

asd
