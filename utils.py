import sys
import os
from typing import Callable

def clear_terminal() -> None:
    #print(chr(27) + "[2J")
    os.system('clear')

input_char: Callable[[], str]

try:
    import tty, termios
except ImportError:
    # Probably Windows.
    try:
        import msvcrt
    except ImportError:
        raise ImportError('getch not available')
    else:
        def _input_char() -> str:
            c = msvcrt.getch() # type: ignore
            c_str = str(c)
            if c_str.startswith("b'"): # need to decode binary string
                return c.decode("utf-8") # type: ignore
            else:
                return c_str[0]

        input_char = _input_char
else:
    def _input_char() -> str:
        """getch() -> key character

        Read a single keypress from stdin and return the resulting character.
        Nothing is echoed to the console. This call will block if a keypress
        is not already available, but will not wait for Enter to be pressed.

        If the pressed key was a modifier key, nothing will be detected; if
        it were a special function key, it may return the first character of
        of an escape sequence, leaving additional characters in the buffer.
        """
        fd = sys.stdin.fileno()
        try:
            old_settings = termios.tcgetattr(fd)
        except termios.error as err:
            if 'Operation not supported on socket' in str(err):
                print("Erreur: impossible de lire un caractère depuis le terminal.\n\nVous devez faire tourner ce code dans le terminal et pas dans la\nconsole en lecture seule de VS Code.\nVérifiez dans les settings de votre workspace que vous avez une ligne qui dit\n\n\t\"code-runner.runInTerminal\": true,\n\nSi ça ne marche pas, suivez les instructions pour refaire tourner\nsetup.sh de la première semaine ou demandez à un assistant.")
                sys.exit(1)
            else:
                raise err
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    input_char = _input_char