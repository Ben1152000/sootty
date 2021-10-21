from sootty.limits import LimitExpression


def test_limits():
    assert str(LimitExpression("a + b & c - d + const 1").tree.pretty('\t')) == "&\n\t+\n\t\twire\ta\n\t\twire\tb\n\t+\n\t\t-\n\t\t\twire\tc\n\t\t\twire\td\n\t\tconst\t1\n"

    assert str(LimitExpression("after (acc clk == const 5) & ready & value & (3 next data == const 64)").tree.pretty('\t')) == "&\n\t&\n\t\t&\n\t\t\tafter\n\t\t\t\t==\n\t\t\t\t\tacc\n\t\t\t\t\t\twire\tclk\n\t\t\t\t\tconst\t5\n\t\t\twire\tready\n\t\twire\tvalue\n\t==\n\t\tnext\n\t\t\t3\n\t\t\twire\tdata\n\t\tconst\t64\n"

    assert str(LimitExpression("D1 & D2").tree.pretty('\t')) == "&\n\twire\tD1\n\twire\tD2\n"


if __name__ == "__main__":
    test_limits()
    print('Success!')
