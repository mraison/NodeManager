from NodeManager.manager.services.command import CommandLineBind, CommandLineChain


def func1():
    return 1


def func2():
    return 2


def test_call():
    cmd = CommandLineBind(
        {
            'opt1': CommandLineBind(
                {
                    'subopt1': func1,
                    'subopt2': func2
                }
            )
        }
    )

    assert cmd('opt1')('subopt1')() == 1
    assert cmd('opt1')('subopt2')() == 2

def test_command_chain():
    cmd = CommandLineChain(
        CommandLineBind(
            {
                'opt1': CommandLineBind(
                    {
                        'subopt1': func1,
                        'subopt2': func2
                    }
                )
            }
        )
    )

    assert cmd(['opt1', 'subopt1']) == 1
    assert cmd(['opt1', 'subopt2']) == 2
