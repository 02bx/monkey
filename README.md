Infected Chaos Monkey
====================

Datacenter Security Tool
------------------------

### http://www.guardicore.com/the-infected-chaos-monkey/

The Infected Chaos Monkey is a security tool which tests your Data Center's ability to withstand perimeter breaches and internal server infection. It uses various methods to propagate through a data center, and reports its success to a centralized C&C server.

Features include:

* Multiple propagation techniques:
  * Predefined passwords
  * Common exploits
* Multiple propagation protocols:
  * SSH 
  * SMB
  * RDP
* A C&C server with a dedicated UI to visualize the Monkey's progress inside the data center

Getting Started
---------------

The Infected Chaos Monkey is comprised of two parts: the Monkey and the C&C server.
The monkey is the tool which infects other machines and propagates to them, while the C&C server collects all Monkey reports and displays them to the user.

### Requirements

<Supported OS Versions for monkey>
<Supported OS Versions for C&C Server>

### Installation

Usage
-----

### Configuring the Monkey

Monkey configuration is stored in two places:
1. By default, the monkey uses a local configuration file (usually, config.bin). This configuration file must include the address of the Monkey's C&C server.
2. After successfully connecting to the C&C server, the monkey downloads a new configuration from the server and discards the local configuration. It is possible to change the default configuration from the C&C server's UI.

Both configuration options use a JSON format for specifying options; see "Options" below for details.

### Running the C&C Server

### Unleashing the Monkey

Download the latest Monkey binary from <> (alternatively, build it by yourself by following the instructions below).
The download includes executables for various operating systems, and a default configuration file (config.bin).
You can edit the configuration file according the the options detailed below; the default configuration assumes <WHAT?>.

Once downloaded, run the monkey using ```./monkey-linux-64 m0nk3y -c config.bin```

Command line options include:
* `-c`, `--config`: set configuration file. JSON file with configuration values, will override compiled configuration.
* `-p`, `--parent`: set monkey’s parent uuid, allows better recognition of exploited monkeys in c&c
* `-t`, `--tunnel`: ip:port, set default tunnel for monkey when connecting to c&c.


Monkey Modus Operandi
---------------------

1.  Wakeup connection to c&c, sends basic info of the current machine and the configuration  the monkey uses to the c&c.
  1. First try direct connection to c&c.
  2. If direct connection fails, try connection through a tunnel, a tunnel is found according to specified parameter (the default tunnel) or by sending a multicast query and waiting for another monkey to answer.
  3. If no connection can be made to c&c, continue without it.
2. If a firewall app is running on the machine (supports Windows Firewall for Win XP and Windows Advanced Firewall for Win 7+), try to add a rule to allow all our traffic.
3. Startup of tunnel for other monkeys (if connection to c&c works).
  1. firewall is checked to allow listening sockets (if we failed to add a rule to windows firewall for example, the tunnel will not be created)
  2. will answer multicast requests from other monkeys in search of a tunnel.
4. Running exploitation sessions, will run x sessions according to configuration:
  1. Connect to c&c and get the latest configuration
  2. Scan ip ranges according to configuration.
  3. Try fingerprinting each host that answer, using the classes defined in the configuration (SMBFinger, SSHFinger, etc)
  4. Try exploitation on each host found, for each exploit class in configuration:
    1. check exploit class supports target host (can be disabled by configuration)
    2. each exploitation class will use the data acquired in fingerprinting, or during the exploit, to find the suitable monkey executable for the host from the c&c. 
      1. If c&c connection fails, and the source monkey’s executable is suitable, we use it. 
      2. If a suitable executable isn’t found, exploitation will fail.
      3. Executables are cached in memory.
  5. will skip hosts that are already exploited in next run
  6. will skip hosts that failed during exploitation in next run (can be disabled by configuration)
5. Close tunnel before exiting
Wait for monkeys using the tunnel to unregister for it
Cleanup
Remove firewall rules if added

Configuration Options
---------------------

Key | Type | Description | Possible Values
--- | ---- | ----------- | ---------------
singleton_mutex_name | string | string of the mutex name for single instance | example: {2384ec59-0df8-4ab9-918c-843740924a28}
alive | bool | sets whether or not the monkey is alive. if false will stop scanning and exploiting.
self_delete_in_cleanup | bool | sets whether or not to self delete the monkey executable when stopped.
use_file_logging | bool | sets whether or not to use a log file.
timeout_between_iterations | int | how long to wait between scan iterations
max_iterations | int | how many scan iterations to perform on each run
victims_max_find | int | how many victims to look for in a single scan iteration
victims_max_exploit | int | how many victims to exploit before stopping
command_servers | array | addresses of c&c servers to try to connect | example: ["russian-mail-brides.com:5000"]
serialize_config | bool | sets whether or not to save the monkey to disk when finished (will be loaded in next run), saved next to the monkey exe with the name monkey.bin
retry_failed_explotation | bool | sets whether or not to retry failed hosts on next scan
range_class | class name | sets which ip ranges class is used to construct the list of ips to scan | `FixedRange` - scan list is a static ips list, `RelativeRange` - scan list will be constructed according to ip address of the machine and size of the scan, `ClassCRange` - will scan the entire class c the machine is in.
scanner_class | class name | sets which scan class to use when scanning for hosts to exploit | `TCPScanner` - searches for hosts according to open tcp ports, `PingScanner` - searches for hosts according to ping scan
finger_classes | tuple of class names | sets which fingerprinting classes to use. | in the list: `SMBFinger` - get host os info by checking smb info, `SSHFinger` - get host os info by checking ssh banner, `PingScanner` - get host os type by checking ping ttl. For example: `(SMBFinger, SSHFinger, PingScanner)`
exploiter_classes | tuple of class names | | `SmbExploiter` - exploit using smb connection, `WmiExploiter` - exploit using wmi connection, `RdpExploiter` - exploit using rdp connection, `Ms08_067_Exploiter` - exploit using ms08_067 smb exploit, `SSHExploiter` - exploit using ssh connection
range_fixed | tuple of strings | list of ips to scan
RelativeRange range_size | int | number of hosts to scan in relative range.
TCPScanner tcp_target_ports | list of int | which ports to scan using tcp scan.
tcp_scan_timeout | int | timeout for tcp connection in tcp scan (in milliseconds).
tcp_scan_interval | int | time to wait between ports in the tcp scan (in milliseconds).
tcp_scan_get_banner | bool  | sets whether or not to read a banner from the tcp ports when scanning
PingScanner ping_scan_timeout | int | timeout for the ping command (in milliseconds).
SmbExploiter/WmiExploiter/RdpExploiter psexec_user | string | user to use for connection
psexec_passwords | list of strings | list of passwords to use when trying to exploit
SmbExploiter skip_exploit_if_file_exist | bool | sets whether or not to abort exploit if the monkey already exists in target.
RdpExploiter rdp_use_vbs_download | bool | sets whether to use vbs payload for rdp exploitation. If false, bits payload is used (will fail if bitsadmin.exe doesn’t exist).
Ms08_067_Exploiter ms08_067_exploit_attempt | int | number of times to try and exploit using ms08_067 exploit.
ms08_067_remote_user_add | string  | user to add to target when using ms08_067 exploit
ms08_067_remote_user_pass | string | password of the user the exploit will add
SSHExploiter ssh_user | string | user to use for ssh connection
ssh_passwords | list of strings | list of passwords to use when trying to exploit





Building the Monkey from source
-------------------------------
<how to build the monkey>


License
=======


