import random
from adhoccomputing.Experimentation.Topology import Event, EventTypes
from adhoccomputing.GenericModel import GenericModel
from threading import Lock


class Message:
    """
    Base class for all types of messages in the consensus algorithm.
    """

    pass


class VoteMessage(Message):
    """
    Message class for voting, includes proposal number, proposed value, and last update timestamp.
    """

    def __init__(self, n: int, value: int, last_update: int):
        self.n = n
        self.value = value
        self.last_update = last_update


class ACKMessage(Message):
    """Acknowledgment message that includes the proposal number being acknowledged."""

    def __init__(self, n: int):
        self.n = n


class NACKMessage(Message):
    """Negative acknowledgment message with a proposal number."""

    def __init__(self, n: int):
        self.n = n


class ValueMessage(Message):
    """Value message for proposing a value during consensus, includes proposal number and the proposed value."""

    def __init__(self, n: int, b: int):
        self.n = n
        self.b = b


class DecideMessage(Message):
    """Decision message to communicate the decided value after consensus."""

    def __init__(self, value: int):
        self.value = value


class ChandraTouegCrashConsensusAlgorithmComponentModel(GenericModel):
    """Implements the Chandra-Toueg crash consensus algorithm component model."""

    def __init__(
        self,
        componentname,
        componentinstancenumber,
        context=None,
        configurationparameters=None,
        num_worker_threads=1,
        topology=None,
    ):
        """Initializes the consensus model with basic configuration and topology."""
        super().__init__(
            componentname,
            componentinstancenumber,
            context,
            configurationparameters,
            num_worker_threads,
            topology,
        )

        self.incoming_messages = {}  # Stores messages by round number
        self.is_coordinator = False
        self.is_coordinator_continued_from_value = False
        self.is_coordinator_continued_from_ack = False
        self.coordinator_wait_lock = Lock()

    def on_init(self, eventobj: Event):
        """Initializes the round counter, random initial value, and determines the coordinator."""
        self.n = 0
        self.q = random.randint(0, 1)
        self.last_update = -1
        total_nodes = len(self.topology.nodes)

        if self.componentinstancenumber == self.n % total_nodes:
            self.is_coordinator = True
        self.start()

    def start(self):
        """Sends an initial vote message at the start of the algorithm."""
        message = VoteMessage(n=self.n, value=self.q, last_update=self.last_update)
        event = Event(self, event=EventTypes.MFRT, eventcontent=message)
        self.send_down(event)

    def continue_as_coordinator_from_value_messages(self):
        """Coordinator handles the highest timestamped value messages to decide a proposal."""
        sorted_messages = sorted(
            self.incoming_messages[self.n], key=lambda x: x.last_update, reverse=True
        )
        message = ValueMessage(n=self.n, b=sorted_messages[0].value)
        event = Event(self, event=EventTypes.MFRT, eventcontent=message)
        self.send_down(event)

    def continue_as_coordinator_from_ack_messages(self):
        """Coordinator sends a decide message after receiving sufficient acknowledgments."""
        message = DecideMessage(value=self.q)
        event = Event(self, event=EventTypes.MFRT, eventcontent=message)
        self.send_down(event)

    def continue_as_non_coordinator(self, message: ValueMessage):
        """Non-coordinator nodes update their value and send an acknowledgment."""
        self.q = message.b
        self.last_update = self.n
        message = ACKMessage(n=self.n)
        event = Event(self, event=EventTypes.MFRT, eventcontent=message)
        self.send_down(event)

    def on_message_from_bottom(self, eventobj: Event):
        """Handles incoming messages, sorting and processing them based on the role of coordinator or non-coordinator."""
        self.incoming_messages[self.n] = self.incoming_messages.get(self.n, []) + [
            eventobj.eventcontent
        ]

        if self.is_coordinator:
            vote_messages = list(
                filter(
                    lambda x: isinstance(x, VoteMessage),
                    self.incoming_messages.get(self.n, []),
                )
            )
            if (
                len(vote_messages) > len(self.topology.nodes) / 2
                and not self.is_coordinator_continued_from_value
            ):
                self.is_coordinator_continued_from_value = True
                self.continue_as_coordinator_from_value_messages()

            ack_messages = list(
                filter(
                    lambda x: isinstance(x, ACKMessage),
                    self.incoming_messages.get(self.n, []),
                )
            )
            if (
                len(ack_messages) > len(self.topology.nodes) / 2
                and not self.is_coordinator_continued_from_ack
            ):
                self.continue_as_coordinator_from_ack_messages()

        else:
            message = eventobj.eventcontent
            if isinstance(message, ValueMessage):
                self.continue_as_non_coordinator(message=message)
