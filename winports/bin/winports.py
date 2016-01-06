import subprocess

import time
from collections import OrderedDict


def split_ip_port(param):
    last_colon = param.rfind(':')
    return param[0:last_colon], param[last_colon + 1:]


def get_ports():
    return_value = []
    output = subprocess.Popen(
            ['netstat', '-ano'],
            stdout=subprocess.PIPE).communicate()[0]

    # $ netstat -ano
    #
    # Active Connections
    #
    # Proto  Local Address          Foreign Address        State           PID
    # TCP    0.0.0.0:80             0.0.0.0:0              LISTENING       2128
    # TCP    0.0.0.0:135            0.0.0.0:0              LISTENING       952
    # TCP    0.0.0.0:443            0.0.0.0:0              LISTENING       2128

    lines = output.strip().splitlines()
    lines.pop(0)  # Active Connections
    lines.pop(0)  # Blank line
    lines.pop(0)  # Proto Local Address etc
    for line in lines:
        vals = line.strip().split()
        v = OrderedDict({
            'protocol': vals[0],
        })

        (v['local_ip'], v['local_port']) = split_ip_port(vals[1])
        (v['remote_ip'], v['remote_port']) = split_ip_port(vals[2])

        if v['protocol'] == 'TCP':
            v['state'] = vals[3]
            v['pid'] = vals[4]
        else:
            v['pid'] = vals[3]

        return_value.append(v)

    return return_value


if __name__ == '__main__':
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    for port in get_ports():
        out_line = timestamp + ' ' + ' '.join(['{}="{}"'.format(i, j) for i, j in port.items()])
        print(out_line)
