from NodeManager.manager.command_parser.command import CommandLineBind, CommandLineChain
from NodeManager.manager.command_parser.option import FuncCommandOptionWrap, CommandOptionCollection, CommandOption


def func1():
    return 1


def func2(data: int):
    return data


def test_call():
    cmd = CommandLineBind(
        {
            'opt1': CommandLineBind(
                {
                    'subopt1': FuncCommandOptionWrap(func1),
                    'subopt2': FuncCommandOptionWrap(
                        func2,
                        CommandOptionCollection(
                            [CommandOption(int)]
                        )
                    )
                }
            )
        }
    )

    assert cmd('opt1')('subopt1')() == 1
    assert cmd('opt1')('subopt2')('2') == 2


def test_command_chain():
    cmd = CommandLineChain(
        CommandLineBind(
            {
                'opt1': CommandLineBind(
                    {
                        'subopt1': FuncCommandOptionWrap(func1),
                        'subopt2': FuncCommandOptionWrap(
                            func2,
                            CommandOptionCollection(
                                [CommandOption(int)]
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
