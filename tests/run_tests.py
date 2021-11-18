if __name__ == "__main__":
    tests = [
        'test_general',
        'test_limits',
        'test_pyrtl',
        'test_style',
        'test_wire_types'
    ]

    modules = map(__import__, tests)

    for module in modules:
        for name, test in module.__dict__.items():
            if callable(test):
                if name[:4] == 'test':
                    test()
