from sootty.parser import parser

import unittest


class TestLimits(unittest.TestCase):
    def test_parse_1(self):
        self.assertEqual(
            str(parser.parse("a + b & c - d + const 1").pretty("\t")),
            "&\n\t+\n\t\twire\ta\n\t\twire\tb\n\t+\n\t\t-\n\t\t\twire\tc\n\t\t\twire\td\n\t\tconst\t1\n",
        )

    def test_parse_2(self):
        self.assertEqual(
            str(
                parser.parse(
                    "after (acc clk == const 5) & ready & value & (3 next data == const 64)"
                ).pretty("\t")
            ),
            "&\n\t&\n\t\t&\n\t\t\tafter\n\t\t\t\t==\n\t\t\t\t\tacc\n\t\t\t\t\t\twire\tclk\n\t\t\t\t\tconst\t5\n\t\t\twire\tready\n\t\twire\tvalue\n\t==\n\t\tnext\n\t\t\t3\n\t\t\twire\tdata\n\t\tconst\t64\n",
        )

    def test_parse_3(self):
        self.assertEqual(
            str(parser.parse("D1 & D2").pretty("\t")), "&\n\twire\tD1\n\twire\tD2\n"
        )


if __name__ == "__main__":
    unittest.main()
