import click
import os
from tcxAnalyse import * 

@click.command()
@click.option('--path',type=click.Path(exists=True))
def hello(path):
    d = path
    for path in os.listdir(d):
        full_path = os.path.join(d, path)
        print(full_path)
        output = printData(full_path)
        print(output)
        f = open("myfile.txt", "a")
        f.write(output)
        f.close


if __name__ == '__main__':
    hello()