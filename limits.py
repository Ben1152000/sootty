from lark import Lark

lang = Lark("""
    %import common.WS
    %ignore WS
    %import common.WORD
    %import common.NUMBER
    lop : "&" | "|" | "^" | "->" | "="
    rop : "==" | "!=" | ">" | ">=" | "<" | "<="
    aop : "+" | "-" | ">>" | "<<" | "%"
    wire : WORD | "const" NUMBER | "time" NUMBER | "!" wire | "(" wire ")"
        | wire lop wire | wire rop wire | "-" wire | wire aop wire
        | "from" wire | "after" wire | "until" wire | "before" wire
        | "next" wire | "prev" wire | NUMBER "next" wire | NUMBER "prev" wire
        | "acc" wire
    start : wire
""")

print( lang.parse("after (acc clk == const 5) & ready & value & (next data == const 64)") )
