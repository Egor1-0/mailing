from taskiq_nats import NATSObjectStoreResultBackend, PullBasedJetStreamBroker

result_backend = NATSObjectStoreResultBackend(
    servers="nats_mail",
)
broker = PullBasedJetStreamBroker(
    servers="nats_mail"
).with_result_backend(
    result_backend=result_backend,
)


