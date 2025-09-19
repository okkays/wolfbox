import cgi_helper


def enter_read_mode():
    print(cgi_helper.run_cgi('client', operation='register',
                             ip=cgi_helper.CLIENT_ADDRESS))
    print(cgi_helper.run_cgi('setworkmode', workmode='ENTER_PLAYBACK'))
    print(cgi_helper.run_cgi('workmodecmd', cmd='stop'))


def get_dirnames():
    return [
        dirname
        for dirname
        in cgi_helper.run_cgi('getdircapability')['capability'].split(',')
        if dirname
    ]


def count_files(dirnames):
    for dirname in dirnames:
        yield dirname, cgi_helper.run_cgi('getdirfilecount', dir=dirname)


def list_files(counts):
    for dirname, count in counts:
        if count.get('count') is None:
            yield (dirname, {'Error': count})
        yield (dirname, cgi_helper.run_cgi('getdirfilelist',
                                           dir=dirname,
                                           start=0,
                                           end=int(count.get('count')) - 1))
