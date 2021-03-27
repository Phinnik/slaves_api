import re
from sys import argv


def main() -> None:
    if len(argv) == 1:
        exit('provide arguments')
    curl = ' '.join(argv[1:])
    result = re.search(r"authorization:(.*?)-H", curl).group(0).lstrip("-H 'authorization: ").rstrip('-H ').rstrip('\\').rstrip("' ")
    print(result)


if __name__ == '__main__':
    main()
