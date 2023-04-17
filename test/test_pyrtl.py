import pyrtl
from sootty import WireTrace, Visualizer

import unittest


class TestPyrtl(unittest.TestCase):
 
    def test_counter(self):
        pyrtl.reset_working_block()

        i = pyrtl.Input(3, "i")
        counter = pyrtl.Register(3, "counter")
        o = pyrtl.Output(3, "o")

        update = counter + i
        counter.next <<= update
        o <<= counter

        sim = pyrtl.Simulation()
        sim.step_multiple({"i": [1, 1, 1, 1, 1]})
        sim.tracer.render_trace()

        wiretrace = WireTrace.from_pyrtl(sim.tracer)
        Visualizer().to_svg(wiretrace).display()

        print(pyrtl.working_block())


    def test_alu(self):
        pyrtl.reset_working_block()

        LW = 0
        SW = 1
        BEQ = 2
        RT = 3
        AND = 0
        OR = 1
        ADD = 2
        SUB = 3

        def ALU(ctrl, a, b):
            result = pyrtl.WireVector(16)
            zero = pyrtl.WireVector(1)

            with pyrtl.conditional_assignment:
                with ctrl == AND:
                    result |= a & b
                with ctrl == OR:
                    result |= a | b
                with ctrl == ADD:
                    result |= a + b
                with ctrl == SUB:
                    result |= a - b

            zero <<= result == 0
            return result, zero

        def ALUControl(op, func):
            ctrl = pyrtl.WireVector(2, "ctrl")
            with pyrtl.conditional_assignment:
                with op == LW:
                    ctrl |= 2
                with op == SW:
                    ctrl |= 2
                with op == BEQ:
                    ctrl |= 3
                with op == RT:
                    with func == 0:
                        ctrl |= AND
                    with func == 1:
                        ctrl |= OR
                    with func == 2:
                        ctrl |= ADD
                    with func == 3:
                        ctrl |= SUB
            return ctrl

        op = pyrtl.Input(2, "op")
        a = pyrtl.Input(16, "a")
        b = pyrtl.Input(16, "b")
        func = pyrtl.Input(2, "func")

        r = pyrtl.Output(16, "result")
        z = pyrtl.Output(1, "zero")

        ctl = ALUControl(op, func)
        (
            r_o,
            z_o,
        ) = ALU(ctl, a, b)
        r <<= r_o
        z <<= z_o

        sim_inputs = {
            "op": [0] * 2 + [1] * 2 + [2] * 2 + [3] * 2,
            "a": [2, 1] * 4,
            "b": [1, 0, 1, 0] * 2,
            "func": [0] * 6 + [0, 1],
        }

        sim = pyrtl.Simulation()

        sim.step_multiple(sim_inputs)
        sim.tracer.render_trace(trace_list=["op", "func", "a", "b", "result", "zero"])

        wiretrace = WireTrace.from_pyrtl(sim.tracer)
        Visualizer().to_svg(wiretrace).display()


if __name__ == "__main__":
    unittest.main()
