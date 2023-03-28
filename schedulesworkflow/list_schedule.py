import asyncio

from temporalio.client import Client


async def main() -> None:
    client = await Client.connect("localhost:7233")
    """
    To list all schedules, use the [list_schedules()](https://python.temporal.io/temporalio.client.Client.html#list_schedules) asynchronous method on the Client.
    If a schedule is added or deleted, it may not be available in the list immediately.
    """

    async for schedule in await client.list_schedules():
        print(f"List Schedule Info: {schedule.info}.")


if __name__ == "__main__":
    asyncio.run(main())


""" @dac
id: how-to-list-scheduled-workflow-executions-in-python
title: How to list Scheduled Workflow Executions in Python
sidebar_label: List Scheduled Workflow Executions
description: Use `list_schedules()` on the Client to list all Workflow Execution in the Python SDK.
lines: 8-14
@dac """
