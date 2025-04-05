"""
Ensures that ports are not assigned multiple times
"""

from threading import Lock
from typing import Dict, Set


class PortManager:
    def __init__(self):
        self.port_locks: Dict[str, Lock] = {"c": Lock(), "e": Lock()}
        self.used_ports: Dict[str, Set[int]] = {"c": set(), "e": set()}
        self.port_ranges = {"c": (9000, 9050), "e": (9500, 9550)}

    def get_next_port(self, instance_type: str) -> int:
        if instance_type not in self.port_ranges:
            raise ValueError(f"Invalid instance type: {instance_type}")

        with self.port_locks[instance_type]:
            start_port, end_port = self.port_ranges[instance_type]
            used = self.used_ports[instance_type]

            for port in range(start_port, end_port + 1):
                if port not in used:
                    used.add(port)
                    return port

            raise RuntimeError(f"No available ports for instance type {instance_type}")

    def release_port(self, instance_type: str, port: int):
        with self.port_locks[instance_type]:
            self.used_ports[instance_type].remove(port)
