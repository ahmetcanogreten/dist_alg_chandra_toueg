.. include:: substitutions.rst

|Chandra-Toueg|
=========================================



Background and Related Work
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As explained in [Fokking2013]_ as below:

A failure detector is called eventually weakly accurate if from some point in time
on, some correct process is never suspected by any process. The Chandra-Toueg
crash consensus algorithm, which uses an eventually weakly accurate failure detector,
is an always correctly terminating k-crash consensus algorithm for any k < N / 2.

Let the processes be numbered: p_0, . . . , p_N-1. Initially, each process randomly
chooses a value 0 or 1. The algorithm proceeds in rounds. Each process q records
the number of the last round last-update_q in which it updated its value; initially,
last-update_q = -1.
Each round n >= 0 is coordinated by the process p_c with c = n mod N. Round
n progresses as follows.

- Every correct, undecided process q (including p_c) sends to p_c the message vote(n, value_q, last-update_q).
- p_c (if not crashed and undecided) waits until N - k such messages have arrived, selects one, say vote(n, b, l) with l as large as possible, and broadcasts value(n, b).
- Every correct, undecided process q (including p_c) waits either:
    - until value(n, b) arrives; then it performs value_q ← b and last-update_q ← n, and sends ack(n) to p_c;
    - or until it suspects that p_c has crashed; then it sends nack(n) to p_c.
- p_c waits for N - k acknowledgments. If more than k of them are positive, then p_c decides for b, broadcasts decide(b), and terminates.

A correct, undecided process that receives decide(b), decides for b and terminates.

Distributed Algorithm: |Chandra-Toueg| 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _BlindFloodingAlgorithmLabel:

.. code-block:: RST
    :linenos:
    :caption: Chandra-Toueg Algorithm


    OnRound: (r) do
        if (r == 0)
            value ← randomly choose value as either 0 or 1
            last_update ← -1
            round ← 0
        
        send vote(round, value, last_update)

        if q == r mod N # is Coordinator
            # Do this in a separate thread since the same process will also run Slave code
            wait for N - k messages vote( r, v, l )

            vote( r, v, l) ← max ( vote(r, v, l) ) for all incoming messages of max last_update
            value ← v
            last_update ← r

            send value(r, value) # Coordinator sends value to all processes

            waits for N - k acknowledgment messages ( r )
            if more than k ack's are received then
                send decide( value ) # Coordinator sends decide message to all processes



        # The coordinator is also Slave
        wait for value( r, b ) or until the coordinator is suspected to be crashed
        if value( r, b ) is received then
            value ← b
            last_update ← r
            send ack( r ) to the coordinator
        else
            send nack( r ) to the coordinator

Example
~~~~~~~~

Below example is taken from [Fokking2013]_:

Given a complete network of three processes p_0, p_1, p_2, and k = 1.
Each round the coordinator waits for two incoming votes, and needs two positive
acknowledgments to decide. We consider one possible computation of the Chandra-
Toueg 1-crash consensus algorithm on this network.

    - Initially, p_0 and p_2 randomly choose the value 1 and p_1 the value 0; last-update=-1 at all three processes.
    - In round 0, the coordinator p_0 takes into account the messages from p_0 and p_1, selects the message from p_1 to determine its new value, and broadcasts the value 0. When p_0 and p_1 receive this message, they set their value to 0 and last-update to 0, and send ack to p_0; moreover, p_1 moves to round 1. However, p_2 moves to round 1 without waiting for a message from p_0, because its failure detector falsely suspects that p_0 has crashed; p_2 sends nack to p_0, and moves to round 1. The coordinator p_0 receives the ack's of p_0 and p_1, decides for 0, and crashes before it can broadcast a decide message.
    - In round 1, the coordinator p_1 can take into account only the messages from p_1 and p_2. It must select the message from p_1 to determine its new value, because it has the highest last-update. So p_1 broadcasts the value 0. When p_1 receives this message, it sets its value to 0 and last-update to 1, and sends ack to itself. The process p_2 moves to round 2 without waiting for a message from p_1, because its failure detector falsely suspects that p_1 has crashed; p_2 sends nack to p_0, and moves to round 2. After p_1 has received the ack and nack from p_1 and p_2, respectively, it also moves to round 2.
    - In round 2, the coordinator p_2 can take into account only the messages from p_1 and p_2. It must select the message from p_1 to determine its new value, because it has the highest last-update. So p_2 broadcasts the value 0. When p_1 and p_2 receive this message, they set their value to 0 and last-update to 2, and send ack to p_2; moreover, p_1 moves to round 3. The coordinator p_2 receives the ack's of p_1 and p_2, decides for 0, and broadcasts <decide, 0>. When p_1 receives this message, it also decides for 0.

Correctness
~~~~~~~~~~~

A failure detector is called eventually weakly accurate if from some point in time
on, some correct process is never suspected by any process.

In the presence of an eventually weakly accurate failure detector, the
Chandra-Toueg algorithm is an (always correctly terminating) k-crash consensus
algorithm for any k < N/2 .

This theorem is proved in [Fokking2013]_ as below:

First we prove that processes cannot decide for different values. Then we
prove that the algorithm always terminates.

Let round n be the first round in which the coordinator decides for a value, say
b. Then the coordinator received more than k ack's in this round, so that:

    (1) there are more than k processes q with last-update_q >= n, and
    (2) last-update_q >= n implies value_q = b.

We argue, by induction on m - n, that properties (1) and (2) are preserved in all
rounds m > n. In round m, since the coordinator ignores votes of only k processes,
by (1) it takes into account at least one vote with last-update >= n to determine
its new value. Hence, by (2), the coordinator of round m sets its value to b, and
broadcasts <value,m, b>. To conclude, from round n onward, processes can decide
only for b.

Now we argue that eventually some correct process will decide. Since the failure
detector is eventually weakly accurate, from some round onward, some correct process
p will never be suspected. So in the next round where p is the coordinator, all
correct processes will wait for a value message from p. Therefore, p will receive at
least N - k ack's, and since N-k > k, it will decide. All correct processes will
eventually receive the decide message of p and will also decide.

Complexity 
~~~~~~~~~~

As explained in [Mostefaoui1999]_:

Time complexity of a round: The number of rounds of the protocolis bounded by n, when used with a failure detector of the class S. There is no upper bound when it is used with a failure detector of the class <>S.

Message complexity of a round: During each round, each process sends a message to eachprocess (including itself). Hence, the message complexity of a round is upper bounded by n^2.

Message type and size: There are two types of message: est and decide. A decide message carries only a proposed value. An est message carries a proposed value (or the default value)plus a round number. The size of the round number is bounded by log2(n) when the underlying failure detector belongs to S. It is not bounded in the other case.

.. [Fokking2013] Wan Fokkink, Distributed Algorithms An Intuitive Approach, The MIT Press Cambridge, Massachusetts London, England, 2013
.. [Mostefaoui1999] Mostéfaoui, Achour & Raynal, Michel. (1999). Solving Consensus Using Chandra-Toueg’s Unreliable Failure Detectors: A General Quorum-Based Approach. Lecture Notes in Computer Science (including subseries Lecture Notes in Artificial Intelligence and Lecture Notes in Bioinformatics). 49-63. 10.1007/3-540-48169-9_4. 