from NodeManager.manager.services.command_parser.command import CommandOptionBind, CommandChain
from NodeManager.manager.services.command_parser.option import Option, OptionCollection
from NodeManager.manager.services.command_parser.func import FuncWrap


def func1():
    return 1


def func2(data: int):
    return data


def test_call():
    cmd = CommandOptionBind(
        {
            'opt1': CommandOptionBind(
                {
                    'subopt1': FuncWrap(f=func1, help_txt="sample"),
                    'subopt2': FuncWrap(
                        func2,
                        OptionCollection(
                            [Option(int, help_txt="must be int")]
                        ),
                        help_txt="sample2"
                    )
                }
            )
        }
    )

    assert cmd('opt1')('subopt1')() == 1
    assert cmd('opt1')('subopt2')('2') == 2


def test_command_chain():
    cmd = CommandChain(
        CommandOptionBind(
            {
                'opt1': CommandOptionBind(
                    {
                        'subopt1': FuncWrap(func1),
                        'subopt2': FuncWrap(
                            func2,
                            OptionCollection(
                                [Option(int)]
                            )
                        )
                    }
                )
            }
        )
    )

    assert cmd(['opt1', 'subopt1']) == 1
    assert cmd(['opt1', 'subopt2', '2']) == 2
    assert cmd(['opt1', 'subopt2', '3']) == 3
