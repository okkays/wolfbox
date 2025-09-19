import cgi_helper


def get_files():
    dirnames = [
        dirname
        for dirname
        in cgi_helper.get_vars('getdircapability')['capability'].split(',')
        if dirname
    ]

    counts = {
        dirname: cgi_helper.get_vars('getdirfilecount', dir=dirname)
        for dirname in dirnames
    }

    print(counts)


if __name__ == "__main__":
    get_files()
