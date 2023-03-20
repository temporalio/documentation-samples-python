import asyncio
from datetime import datetime, timedelta

from temporalio.client import (
    Client,
    Schedule,
    ScheduleActionStartWorkflow,
    ScheduleIntervalSpec,
    ScheduleSpec,
    ScheduleUpdate,
    ScheduleUpdateInput,
)

from your_workflows import YourSchedulesWorkflow


async def main():
    client = await Client.connect("localhost:7233")
    handle = await client.create_schedule(
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
    Create a function that takes `ScheduleUpdateInput` and returns `ScheduleUpdate`.
    To update a Schedule, use a callback to build the update from the description.
    The following example updates the schedule to use a new argument and changes the timeout.
    """

    async def update_schedule_simple(
        input: ScheduleUpdateInput, timeout_minutes: int = 7
    ) -> ScheduleUpdate:
        schedule_action = input.description.schedule.action
        schedule_action.task_timeout = timedelta(minutes=timeout_minutes)
        schedule_action.args = ["my new schedule arg"]

        return ScheduleUpdate(schedule=input.description.schedule)

    await handle.update(update_schedule_simple)
    await handle.trigger()

    """
    To list all schedules, use the [list_schedules()](https://python.temporal.io/temporalio.client.Client.html#list_schedules) asynchronous method on the Client.
    If a schedule is added or deleted, it may not be available in the list immediately.
    """

    async def schedule_count() -> int:
        return len([i async for i in await client.list_schedules()])

    print(f"Schedule count: {await schedule_count()}")
    print(f"Result: {handle}")


if __name__ == "__main__":
    asyncio.run(main())


""" @dac
id: how-to-list-scheduled-workflow-executions-in-python
title: How to list Scheduled Workflow Executions in Python
sidebar_label: List Scheduled Workflow Executions
description: Use `list_schedules()` on the Client to list all Workflow Execution in the Python SDK.
lines:
@dac """
