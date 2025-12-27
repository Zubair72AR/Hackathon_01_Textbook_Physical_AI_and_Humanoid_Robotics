---
sidebar_position: 1
---

# ROS 2 Nodes, Topics, and Services

## Overview

In this section, we'll explore the fundamental communication patterns in ROS 2: Nodes, Topics, and Services. These form the backbone of the robotic nervous system that enables different components of a humanoid robot to communicate effectively.

## Nodes

A node is a process that performs computation. In ROS 2, nodes are the basic unit of execution. Each node can perform specific tasks and communicate with other nodes through topics, services, actions, and parameters.

```python
import rclpy
from rclpy.node import Node

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1
```

## Topics and Message Passing

Topics enable asynchronous, many-to-many communication between nodes. Messages are published to topics and can be subscribed to by multiple nodes simultaneously.

## Services

Services provide synchronous, request-response communication. A service client sends a request and waits for a response from the service server.

## Practical Example: Humanoid Robot Control

In a humanoid robot system, nodes might include:
- Sensor processing nodes
- Motor control nodes
- Perception nodes
- Planning nodes
- Behavior control nodes

These nodes communicate through topics for sensor data and motor commands, and through services for configuration and control actions.

## Summary

Understanding ROS 2's communication patterns is essential for building the robotic nervous system. These patterns provide the foundation for more complex robotic behaviors and control systems.