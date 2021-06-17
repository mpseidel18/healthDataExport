import click
import os
from healthdataInterpret import * 

@click.command()
@click.argument('path')
def hello(path):
    d = path
    for path in os.listdir(d):
        full_path = os.path.join(d, path)
        print(full_path)
        printData(full_path)


if __name__ == '__main__':
    hello()