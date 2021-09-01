# Last Writer Wins Element Set with CRDT Implementation

The functionality of the LWW set is that you can assign LWW graphs to each client, and be able to change elements (add or remove) without worry of them getting mixed up due to time or update issues. This allows for offline and asynchronous client side modification of elements, yet when the LWW graphs link up everything merges correctly without conflict.

In this scenario, each LWW set has as many elements as it wants, which can be added or removed, and keeps track of two sets of elements. Both an Added (A) set and a Removed (R) set. Then the final kept set is determined by timestamps (Hybrid Logical Clock (HLC) seems to be best, but a simple implementation was not working for me locally). Effectively, if an element exists in A only, then it is added; however, if it exists in A and R, then you base it on the timestamp. If the timestamp is more recent for the element in R, then it is not included, else it is included. The benefits of this system is it sets up a clear winner for which elements are kept. Thus, when merging LWW graphs all you need to do is update all your elements to the max timestamp.

The outline of the entire use case is:

+ set up LWW graphs
    - these graphs can be enabled for two clients

+ add / remove elements
    - keep all unique elements in both add and remove with most recent timestamp

+ merge graphs on client sync
    - update all unique elements to the most recent time

This allows you to get the most recent client side updates possible, then when the clients sync and graphs merge, it allows you to properly translate the offline add / removes to the true most current graph.

## File structure

The following are the files used to create the two different implementations of this system. 

+ `lww_dict.py`
    - Implementation of the LWW system using a dictionary base. The dictionary implementation offers faster computational time, but restrictions based on the key values of a dictionary.

+ `lww_set.py`
    - Implementation of the LWW system using a set base (Python lists). This implementation has no restrictions on what the element objects are, but at the cost of computational time.

+ `lww_testing.ipynb`
    - This notebooks covers what this does, how to use the code, and testing its features to ensure it is working correctly. _The testing was only done with the set implementation._

# Simple G-Counter Implementation

The functionality of the G Counter is that it never decreases. Thus, it is an easy implementation to have multiple counters that keeps track of multiple states asynchronously and independently. This allows for chatter between two counters to periodically update and give fast estimates of the total count if the clients counter requests one. This gives the client a faster response time at the cost of not giving an exact value to the client, however it also creates great functionality for offline tallying as counters can merge nodes when they are back online.

In this scenario, each G Counter has only one unique node that it can update; however, in actuality the code base can support as many unique nodes as wanted. In practice a GCounter would be launched when a client opens, where the nodes would pertain to any always-increasing counters. This app would need to be opened online to initially connect; and would be getting chatter from other counters (i.e, merges) asynchronously. However, the benefits of using this CRDT implementation would allow the app to go offline and still provide updates to the client, as well as store their own updates to eventually be pushed to other counters.

The outline of the entire use case is:

+ set up G Counters
    - these counters can only update their unique nodes
    - however, they store the node values for all seen nodes

+ increment node values for individual G Counters, independently of others

+ asynchronously chatter between nodes to keep values updating in the background

+ merge G Counter nodes when chattering
    - takes the max value of each node
        + this works as G Counters in always-increasing, meaning the max value is always the most recent value that is seen

+ continue incrementing and merging counters

+ etc, etc,
