import asyncio
from typing import List, Sequence

from temporalio import workflow
from temporalio.client import Client
from temporalio.common import RawValue
from temporalio.worker import Worker

"""dacx
A Dynamic Signal in Temporal is a Signal that is invoked dynamically at runtime if no other Signal with the same name is registered.
A Signal can be made dynamic by adding `dynamic=True` to the `@signal.defn` decorator.

The Signal Handler must then accept a single argument of type `Sequence[temporalio.common.RawValue]`.
The [payload_converter()](https://python.temporal.io/temporalio.workflow.html#payload_converter) function is used to convert a `RawValue` object to the desired type.
dacx"""


@workflow.defn
class GreetingWorkflow:
    def __init__(self) -> None:
        self._pending_greetings: asyncio.Queue[str] = asyncio.Queue()
        self._exit = False

    @workflow.run
    async def run(self) -> List[str]:
        greetings: List[str] = []
        while True:
            # Wait for queue item or exit
            await workflow.wait_condition(
                lambda: not self._pending_greetings.empty() or self._exit
            )

            # Drain and process queue
            while not self._pending_greetings.empty():
                greetings.append(f"Hello, {self._pending_greetings.get_nowait()}")

            # Exit if complete
            if self._exit:
                return greetings

    @workflow.signal
    async def dynamic_signal(self, name: str, args: Sequence[RawValue]) -> None:
        name = workflow.payload_converter().from_payload(args[0].payload)
        await self._pending_greetings.put(name)

    @workflow.signal
    def exit(self) -> None:
        self._exit = True


async def main():
    # Start client
    client = await Client.connect("localhost:7233")

    # Run a worker for the workflow
    async with Worker(
        client,
        task_queue="dynamic-signal-task-queue",
        workflows=[GreetingWorkflow],
    ):
        handle = await client.start_workflow(
            GreetingWorkflow.run,
            id="hello-dynamic-signal-id",
            task_queue="dynamic-signal-task-queue",
        )

        await handle.signal("unregister-signal", "Dynamic Signal argument 1")
        await handle.signal("unregister-signal", "Dynamic Signal argument 2")
        await handle.signal("unregister-signal", "Dynamic Signal argument 3")
        await handle.signal(GreetingWorkflow.exit)

        result = await handle.result()
        print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())


""" @dacx
id: how-to-set-a-dynamic-signal-in-python
title: How to set a Dynamic Signal
label: Set a Dynamic Signal
description: Use `dynamic=True` on the `@workflow.signal` decorator to make a Signal dynamic.
tags:
 - dynamic signal
 - python sdk
 - code sample
lines: 9-15, 41-44, 67
@dacx"""
