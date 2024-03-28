.. include:: substitutions.rst

Introduction
============


In a distributed system, where processes potentially live on different computers, some processes may crash at any point. At that point, the system must correctly identify those faulty processes and isolate them so that they will not cause further harm to the system itself. Since processes are partitioned across the network, resolving this distinction may not always be trivial. This is where failure detector algorithms come in. That is, they help correct processes identify incorrect, faulty processes in a distributed environment.

Faulty processes may or may not harm the system while there are correct processes. However, even though they might not, in order to prevent potential further harm, correct processes are also responsible for detecting, isolating and perhaps killing those faulty processes. Otherwise, they may start to create problems for the system or continue creating bigger problems which makes the resolution even harder.

Theoretically speaking, it is impossible to know if a process failed or took too much time to respond. Therefore, we need to make certain trade-offs by perhaps categorizing slow processes as faulty ones as well.

The Chandra-Toueg Algorithm requires that up to k processes, where k is less than the half of the total number of processes, fail at any point for correct processes to correctly detect those faulty k processes. If there are more faulty processes crashing, it will not be able to provide certainty that correct processes will detect faulty processes.

In this study, I will implement the Chandra-Toueg Algorithm on the AHCv2 platform to test how well it works under different challenging conditions, such as crashes, delays in communication, and changes in the network structure. I want to see if the algorithm could still help correct processes to identify faulty processes, keep everything running smoothly, and recover quickly from any problems.