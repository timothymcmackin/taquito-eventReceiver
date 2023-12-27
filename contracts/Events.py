import smartpy as sp

@sp.module
def main():
    class Events(sp.Contract):
        def __init__(self, value):
            self.data.storedValue = value

        @sp.entrypoint
        def add(self, addAmount):
            sp.emit(sp.record(
                source=sp.source,
                addAmount=addAmount
            ), tag="add", with_type=True)
            self.data.storedValue += addAmount

        @sp.entrypoint
        def reset(self):
            sp.emit(sp.record(
                source=sp.source,
                previousValue=self.data.storedValue
            ), tag="reset", with_type=True)
            self.data.storedValue = 0

if "templates" not in __name__:

    @sp.add_test(name="Events")
    def test():
        c1 = main.Events(12)
        scenario = sp.test_scenario(main)
        scenario.h1("Add")
        scenario += c1
        c1.add(2).run(
            sender = sp.test_account("Alice")
        )
        scenario.verify(c1.data.storedValue == 14)