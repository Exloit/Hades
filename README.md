# Hades

# Hades is a pentest tools best work in python27
```bash
usage: python msf.py -p "msfrpcd Password" -lh "multi/handler LHOST" -lp "multi/handler LPORT"
```

## Tips:
Befor run this script , you must start the msfrpcd .
`$./msfrpcd -P mypassword -n -f -a 127.0.0.1`

The -f parameter tells msfrpcd to remain in the foreground and the -n parameter disables database support. Finally, the -a parameter tells msfrcpd to listen for requests only on the local loopback interface (127.0.0.1).
