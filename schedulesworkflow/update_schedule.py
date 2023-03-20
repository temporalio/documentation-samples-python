import asyncio
from datetime import timedelta

from temporalio.client import (
    Client,
    ScheduleUpdate,
    ScheduleUpdateInput,
)


async def main():
    client = await Client.connect("localhost:7233")
    handle = client.get_schedule_handle(
        "workflow-schedule-id",
    )

    """
    Create a function that takes `ScheduleUpdateInput` and returns `ScheduleUpdate`.
    To update a Schedule, use a callback to build the update from the description.
    The following example updates the Schedule to use a new argument and changes the timeout.
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


if __name__ == "__main__":
    asyncio.run(main())

""" @dac
id: how-to-update-scheduled-workflow-execution-in-python
title: How to update a Scheduled Workflow Execution in Python
sidebar_label: Update a Scheduled Workflow Execution
description: Create a function that takes `ScheduleUpdateInput` and returns `ScheduleUpdate`.
lines: 17-32
@dac """

""" @dac
id: how-to-list-scheduled-workflow-executions-in-python
title: How to list Scheduled Workflow Executions in Python
sidebar_label: List Scheduled Workflow Executions
description: Use `list_schedules()` on the Client to list all Workflow Execution in the Python SDK.
lines: 35-41
@dac """
