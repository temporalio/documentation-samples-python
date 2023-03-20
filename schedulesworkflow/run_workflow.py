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


async def main():
    client = await Client.connect("localhost:7233")

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
