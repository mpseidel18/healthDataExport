import click
import os
from healthdataInterpret import * 

@click.command()
@click.option('--path')
def hello(path):
    d = path
    for path in os.listdir(d):
        full_path = os.path.join(d, path)
        output = printData(full_path)
        print(output)
        f = open("myfile.txt", "a")
        f.write(output)
        f.close


if __name__ == '__main__':
    hello()