import asyncio

from temporalio.client import Client


async def main():
    client = await Client.connect("localhost:7233")
    handle = client.get_schedule_handle(
        "workflow-schedule-id",
    )
    desc_handle = await handle.describe()
    print(f"{desc_handle.schedule}")
    """
    To delete a Scheduled Workflow Execution in Python, use the [delete()](https://python.temporal.io/temporalio.client.ScheduleHandle.html#delete) asynchronous method on the Schedule Handle.
    """
    await handle.delete()
    print(f"State: {desc_handle.schedule.state}")


if __name__ == "__main__":
    asyncio.run(main())

""" @dac
id: how-to-delete-a-scheduled-workflow-execution-in-python
title: How to delete a Scheduled Workflow Execution in Python
sidebar_label: Delete a Scheduled Workflow Execution
description: Use the `delete()` asynchronous method on the Schedule Handler.
lines: 13-16
@dac """
