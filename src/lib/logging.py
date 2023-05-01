from enum import Enum
from colorama import Fore, Style, init


class Logger:
    class LogLevel(Enum):
        DEBUG = 1
        INFO = 2
        WARN = 3
        FATAL = 4
    
    
    class Colors(Enum):
        GREEN = 1
        RED = 2
        YELLOW = 3
        BLUE = 4
    
    def colorize(self, color: Colors, message):
        colors = {
            1: f"{Fore.GREEN}{message}{Fore.RESET}",
            2: f"{Fore.RED}{message}{Fore.RESET}",
            3: f"{Fore.YELLOW}{message}{Fore.RESET}",
            4: f"{Fore.BLUE}{message}{Fore.RESET}",
        }

        if color.value > 4 or color.value < 1:
            # TODO: Make the error message update dynamically with class
            raise ValueError("Color must be a valid option. GREEN, RED, YELLOW, BLUE")
        
        return str(colors[color.value])

    
    def log(self, lvl: LogLevel = LogLevel.DEBUG, message = "Test"):
        # init for colormam
        init()

        levels = {
            1: f'[{Fore.CYAN}{Style.BRIGHT}Debug{Style.RESET_ALL}]',
            2: f'[{Fore.BLUE}{Style.BRIGHT}Info{Style.RESET_ALL}]',
            3: f'[{Fore.YELLOW}{Style.BRIGHT}Warn{Style.RESET_ALL}]',
            4: f'[{Fore.RED}{Style.BRIGHT}Fatal{Style.RESET_ALL}]'
        }



        if lvl.value > 4 or lvl.value < 1:
            raise ValueError(f"Log level must be an valid option. DEBUG, INFO, WARN, FATAL")
        
        print(f"{levels[lvl.value]} {message}")
