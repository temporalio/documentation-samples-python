import asyncio
from datetime import datetime, timedelta

from temporalio.client import (
    Client,
    Schedule,
    ScheduleActionStartWorkflow,
    ScheduleBackfill,
    ScheduleIntervalSpec,
    ScheduleOverlapPolicy,
    ScheduleSpec,
)

from your_workflows import YourSchedulesWorkflow

"""
Use the `connect()` method on the Client class to create and connect to a Temporal Client to the Temporal Cluster.
"""

"""
To start a Workflow Execution in Python, use either the start_workflow() or execute_workflow() asynchronous methods in the Client.
"""


async def main():
    client = await Client.connect("localhost:7233")

    # Start workflow every day at 4 o'clock
    result = await client.create_schedule(
        "workflow-schedule-id",
        Schedule(
            action=ScheduleActionStartWorkflow(
                YourSchedulesWorkflow.run,
                "my schedule arg",
                id="schedules-workflow-id",
                task_queue="my-task-queue",
            ),
            spec=ScheduleSpec(
                intervals=[
                    ScheduleIntervalSpec(
                        every=timedelta(days=10),
                        offset=timedelta(days=2),
                    )
                ],
            ),
        ),
    )
    """
    To trigger a Scheduled Workflow Execution in Python, use the [trigger()](https://python.temporal.io/temporalio.client.ScheduleHandle.html#trigger) asynchronous method on the Schedule Handle.
    """
    await result.trigger()
    now = datetime.utcnow()
    if now.second == 0:
        now += timedelta(seconds=1)
    await result.backfill(
        ScheduleBackfill(
            start_at=now,
            end_at=now,
            overlap=ScheduleOverlapPolicy.ALLOW_ALL,
        ),
    )

    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())


""" @dac
id: how-to-connect-to-a-cluster-in-python
title: How to connect to a Temporal Cluster in Python
sidebar_label: Connect a Temporal Client
description: Connect a Temporal Client to a Cluster in the Python SDK.
lines:
@dac """

""" @dac
id: how-to-schedule-a-workflow-execution-in-python
title: How to Schedule a Workflow Execution in Python
sidebar_label: Schedule a Workflow Execution
description: Schedule a Workflow Execution in the Python SDK.
lines:
@dac """

""" @dac
id: how-to-trigger-a-scheduled-workflow-execution-in-python
title: How to Trigger a Scheduled Workflow Execution in Python
sidebar_label: Trigger a Scheduled Workflow Execution
description: Trigger a Scheduled Workflow Execution in the Python SDK.
lines:
@dac """
