import argparse
import sys


def parse_args():
    parser = argparse.ArgumentParser(description='CLI interface for EnvyControl')
    parser.add_argument('--status', action='store_true', help='Query the current status of the dGPU')
    parser.add_argument('--switch', type=str, metavar='MODE', action='store',
                        help='Switch the dGPU mode. You need to reboot for changes to take effect.'
                            ' Supported modes: on | off')
    parser.add_argument('-v', '--version', action='store_true', help='Print version and exit')

    # if no argument is provided then display help and exit
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    
    return parser.parse_args()
