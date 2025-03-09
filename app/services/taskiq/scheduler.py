from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_nats import NATSKeyValueScheduleSource

from .broker import broker

nats_source = NATSKeyValueScheduleSource("nats_mail")
source = LabelScheduleSource(broker)

scheduler = TaskiqScheduler(broker, sources=[nats_source, source])