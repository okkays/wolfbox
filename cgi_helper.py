import requests
import datetime
import cam_helper

CGI_ADDRESS_BASE = f'http://{cam_helper.CAM_ADDRESS}/cgi-bin/hisnet'
HISNET_ERRORS = {
    '0xFFFFF752': 'HISNET_SVR_RTN_ERROR',
    '0xFFFFF2FB': 'HISNET_SVR_REGFUNC_NULL',
    '0xFFFFEEA4': 'HISNET_SVR_CMD_INVALID',
    '0xFFFFEA4D': 'HISNET_SVR_ARGPARSER_ERROR',
}


def get_vars(varname, **kwargs):
    params = ''.join(f'&-{k}={v}' for k, v in kwargs.items())
    url = f'{CGI_ADDRESS_BASE}/{varname}.cgi?{params}'
    print('Getting', url)
    deviceattr_raw = requests.get(url,
                                  headers={
                                      'Accept-Encoding': 'gzip',
                                      'Connection': 'close'},
                                  cookies={'SessionID': 'null'},
                                  ).text
    deviceattr = _clean_var_result(deviceattr_raw)
    return {
        **deviceattr,
    }


def _clean_var_line_key(var_line):
    if 'SvrFuncResult' in var_line:
        return 'SvrFuncResult'
    if var_line.startswith('var '):
        return var_line.split('=')[0][4:]
    return None


def _clean_var_line_value(var_line):
    if 'SvrFuncResult' in var_line:
        hexerror = var_line.split('=')[1].strip('"')
        return HISNET_ERRORS.get(hexerror, hexerror)
    if var_line.startswith('var '):
        return var_line.split('=')[1].strip('";')
    return None


def _clean_var_result(var_result):
    lines = var_result.splitlines()
    return {
        # Remove the var prefix as well as quoted values:
        _clean_var_line_key(line): _clean_var_line_value(line)
        for line in lines
        if line.strip()
    }


def set_time():
    current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    requests.get(f'{CGI_ADDRESS_BASE}/setsystime.cgi'
                 f'?&-time={current_time}')
