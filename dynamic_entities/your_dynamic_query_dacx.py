import asyncio
from typing import Sequence

from temporalio import workflow
from temporalio.client import Client
from temporalio.common import RawValue
from temporalio.worker import Worker

"""dacx
A Dynamic Query in Temporal is a Query that is invoked dynamically at runtime if no other Query with the same name is registered.
A Query can be made dynamic by adding `dynamic=True` to the `@query.defn` decorator.

The Query function must then accept a single argument of type `Sequence[temporalio.common.RawValue]`.
The [payload_converter()](https://python.temporal.io/temporalio.workflow.html#payload_converter) function is used to convert a `RawValue` object to a string representation.
dacx"""


@workflow.defn
class GreetingWorkflow:
    def __init__(self) -> None:
        self._greeting = "<no greeting>"

    @workflow.run
    async def run(self, name: str) -> None:
        self._greeting = f"Hello, {name}!"
        await asyncio.sleep(2)
        self._greeting = f"Goodbye, {name}!"

    @workflow.query(dynamic=True)
    def dynamic_query(self, name: str, args: Sequence[RawValue]) -> str:
        name = workflow.payload_converter().from_payload(args[0].payload)
        return self._greeting


async def main():
    client = await Client.connect("localhost:7233")

    async with Worker(
        client,
        task_queue="dynamic-query-task-queue",
        workflows=[GreetingWorkflow],
    ):

        handle = await client.start_workflow(
            GreetingWorkflow.run,
            "World",
            id="hello-dynamic-query-id",
            task_queue="dynamic-query-task-queue",
        )
        # Querying with an unregistered Query name and passing a payload.
        current_greeting = await handle.query("unregistered-query", arg="None")
        print(f"First greeting result: {current_greeting}")

        await asyncio.sleep(3)

        # Querying with an unregistered Query name and passing a payload.
        current_greeting = await handle.query("unregistered-query", arg="None")
        print(f"Second greeting result: {current_greeting}")


if __name__ == "__main__":
    asyncio.run(main())

""" @dacx
id: how-to-set-a-dynamic-query-in-python
title: How to set a Dynamic Query
label: Set a Dynamic Query
description: Use `dynamic=True` on the `@workflow.query` decorator to make a Query dynamic.
tags:
 - dynamic query
 - python sdk
 - code sample
lines: 9-15, 29-32, 50-58
@dacx"""
