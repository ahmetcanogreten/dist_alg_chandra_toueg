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

- Every correct, undecided process q (including p_c) sends to p_c the message <vote, n, value_q, last-update_q>.
- p_c (if not crashed and undecided) waits until N - k such messages have arrived, selects one, say <vote, n, b, l> with l as large as possible, and broadcasts <value, n, b>.
- Every correct, undecided process q (including p_c) waits either:
    - until <value, n, b> arrives; then it performs value_q ← b and last-update_q ← n, and sends <ack, n> to p_c;
    - or until it suspects that p_c has crashed; then it sends <nack, n> to p_c.
- p_c waits for N - k acknowledgments. If more than k of them are positive, then p_c decides for b, broadcasts <decide, b>, and terminates.

A correct, undecided process that receives <decide, b>, decides for b and terminates.

Distributed Algorithm: |Chandra-Toueg| 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _BlindFloodingAlgorithmLabel:

.. code-block:: RST
    :linenos:
    :caption: Chandra-Toueg Algorithm

    TODO

Example
~~~~~~~~

Provide an example for the distributed algorithm.

Correctness
~~~~~~~~~~~

Present Correctness, safety, liveness and fairness proofs.


Complexity 
~~~~~~~~~~

Present theoretic complexity results in terms of number of messages and computational complexity.

.. [Fokking2013] Wan Fokkink, Distributed Algorithms An Intuitive Approach, The MIT Press Cambridge, Massachusetts London, England, 2013
