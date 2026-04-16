# Network Delay Measurement Tool
**Course:** UE24CS252B - Computer Networks  
**Student:** Archana Shivakumar  
**SRN:** PES1UG24CS078

## Problem Statement
Implement an SDN-based Network Delay Measurement Tool using Mininet and POX controller that:
- Measures and analyzes latency (RTT) between hosts using ICMP
- Implements MAC learning for efficient packet forwarding
- Enforces firewall rules to block specific host pairs
- Demonstrates controller-switch interaction via OpenFlow

## Topology
- 1 OVS Switch (s1)
- 3 Hosts: h1 (10.0.0.1), h2 (10.0.0.2), h3 (10.0.0.3)
- Remote POX Controller on port 6633

## Setup & Execution

### Prerequisites
sudo apt install mininet -y
git clone https://github.com/noxrepo/pox
### Steps
1. Copy controller to POX:
cp controller.py ~/pox/pox/forwarding/delay_controller.py
2. Start POX controller (Terminal 1):
cd ~/pox
python3 pox.py log.level --DEBUG forwarding.delay_controller
3. Start Mininet topology (Terminal 2):
sudo python3 topology.py
## Test Scenarios

### Scenario 1: Normal Latency Measurement (h1 → h2)
mininet> h1 ping -c 5 h2
Expected: 0% packet loss, RTT logged by controller

### Scenario 2: Blocked Traffic (h1 → h3)
mininet> h1 ping -c 5 h3
Expected: 100% packet loss, BLOCKED logged by controller

## Expected Output
- Scenario 1: Successful ping with RTT ~1-2ms
- Scenario 2: All packets dropped, controller logs BLOCKED
- Flow table shows installed rules via `sh ovs-ofctl dump-flows s1`

## References
- [Mininet](https://mininet.org)
- [POX Controller](https://github.com/noxrepo/pox)
- [OpenFlow Spec](https://opennetworking.org/wp-content/uploads/2014/10/openflow-spec-v1.3.0.pdf)

## Proof of Execution

### Scenario 1: Normal Latency Measurement (h1 → h2)
![Scenario 1]
(<img width="602" height="305" alt="Picture1" src="https://github.com/user-attachments/assets/aa1202ad-ed13-4096-b518-4d647f492136" />
)

### Scenario 2: Blocked Traffic (h1 → h3)
![Scenario 2](<img width="602" height="293" alt="Picture2" src="https://github.com/user-attachments/assets/08bcb7ce-c6fc-4b37-896c-3162505c209b" />
)

### Flow Table
![Flow Table](<img width="602" height="330" alt="Picture3" src="https://github.com/user-attachments/assets/42b5d56e-39bd-4b53-8670-41a290f9947d" />
)

### Performance Observation (iperf)
![iperf](<img width="602" height="135" alt="Picture4" src="https://github.com/user-attachments/assets/2aa9ebdc-509f-43fe-ad38-a4dd7290eaa3" />
)
