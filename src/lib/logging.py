from enum import Enum
from colorama import Fore, Style, init


# Test to see if colorama has already been initalized.
colorama_initalized = False

class Colorization:
    def __init__(self) -> None:
        global colorama_initalized
        if not colorama_initalized:
            init()
            colorama_initalized = True

    class Colors(Enum):
        GREEN = 1
        RED = 2
        YELLOW = 3
        BLUE = 4
    
    def colorize(self, color: Colors, message: str) -> str:
        """Colorizes an string.
        
        ### Arguments
        - color: The color to colorize the text (Type: Colors)
        - message: The text to color

        ### Returns
        - A string with the new colorized text
        """
        if not isinstance(color, self.Colors):
            raise ValueError(f"You must enter an Color. {', '.join(key.name for key in self.Colors)}")
        
        colors = {
            1: f"{Fore.GREEN}{message}{Fore.RESET}",
            2: f"{Fore.RED}{message}{Fore.RESET}",
            3: f"{Fore.YELLOW}{message}{Fore.RESET}",
            4: f"{Fore.BLUE}{message}{Fore.RESET}",
        }
        
        return str(colors[color.value])


class Logger:
    def __init__(self) -> None:
        global colorama_initalized
        if not colorama_initalized:
            init()
            colorama_initalized = True
    
    class LogLevel(Enum):
        DEBUG = 1
        INFO = 2
        WARN = 3
        FATAL = 4

    
    def log(self, lvl: LogLevel, message: str) -> None:
        """
        Prints out formatted logs
        
        ### Arguments
        - lvl: The log level
        """
        if not isinstance(lvl, self.LogLevel):
            raise ValueError(f"Log level must be an valid option. {', '.join(key.name for key in self.LogLevel)}")
        
        levels = {
            1: f'[{Fore.CYAN}{Style.BRIGHT}Debug{Style.RESET_ALL}]',
            2: f'[{Fore.GREEN}{Style.BRIGHT}Info{Style.RESET_ALL}]',
            3: f'[{Fore.YELLOW}{Style.BRIGHT}Warn{Style.RESET_ALL}]',
            4: f'[{Fore.RED}{Style.BRIGHT}Fatal{Style.RESET_ALL}]'
        }
        
        print(f"{levels[lvl.value]} {message}")


if __name__ == "__main__":
    # Testing
    log = Logger()
    colors = Colorization()
    log.log(log.LogLevel.DEBUG, "Debug")
    log.log(log.LogLevel.INFO, "Info")
    log.log(log.LogLevel.WARN, "Warn")
    log.log(log.LogLevel.FATAL, "Fatal")
    print(colors.colorize(colors.Colors.BLUE, "Blue"))
    print(colors.colorize(colors.Colors.RED, "Red"))
    print(colors.colorize(colors.Colors.GREEN, "Green"))
    print(colors.colorize(colors.Colors.YELLOW, "Yellow"))
