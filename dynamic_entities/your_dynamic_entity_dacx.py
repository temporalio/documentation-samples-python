import asyncio
from dataclasses import dataclass
from datetime import timedelta
from typing import Sequence

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.common import RawValue
from temporalio.worker import Worker

"""dacx
A Workflow can be made dynamic by adding dynamic=True to the `@workflow.defn` decorator.
The Workflow's run method must then accept a single argument of type `Sequence[temporalio.common.RawValue]`.
At runtime, the Workflow will be invoked if no Workflow with the given name is registered.
The input arguments are passed to the run method as the single `Sequence[RawValue]` argument.
dacx"""

"""dacx
Similar to dynamic Workflows, an Activity can be made dynamic by adding `dynamic=True` to the `@activity.defn` decorator.
The Activity function must then accept a single argument of type `Sequence[temporalio.common.RawValue]`.

At runtime, the Activity will be invoked if no Activity with the given name is registered.
The input arguments are passed to the Activity function as the single `Sequence[RawValue]` argument.
dacx"""

"""dacx
A Signal can be made dynamic by adding dynamic=True to the `@workflow.signal` decorator.
The Signal method must accept two arguments - a str name and a `Sequence[temporalio.common.RawValue]` args.
At runtime, the Signal will be invoked if no Signal with the given name exists on the Workflow.
dacx"""

"""dacx
Similar to dynamic Signals, a Query can be made dynamic by adding `dynamic=True` to the `@workflow.query` decorator.
The Query method must accept two arguments - a `str` name and a `Sequence[temporalio.common.RawValue]` args.
At runtime, the Query will be invoked if no Query with the given name is defined on the Workflow.
dacx"""


@dataclass
class ComposeGreetingInput:
    greeting: str
    name: str


@activity.defn(dynamic=True)
async def compose_greeting(args: Sequence[RawValue]) -> str:
    return f"{args}!"


@activity.defn()
async def default_greeting(input: ComposeGreetingInput) -> str:
    return f"{input.greeting}, {input.name}!"


@workflow.defn()
class DefaultWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        return await workflow.execute_activity(
            default_greeting,
            name,
            start_to_close_timeout=timedelta(seconds=10),
        )


@workflow.defn(dynamic=True)
class GreetingWorkflow:
    def __init__(self):
        # Set initial greeting
        self.greeting = "Hello"

    @workflow.run
    async def run(self, args: Sequence[RawValue]) -> str:
        name = args[0].payload
        return await workflow.execute_activity(
            "unregistered_activity_name",
            name,
            start_to_close_timeout=timedelta(seconds=10),
        )

    @workflow.signal(dynamic=True)
    async def set_greeting(self, name: str, new_greeting: Sequence[RawValue]):
        # self.greeting = "Goodbye"
        self.greeting = new_greeting[0].payload

    @workflow.query(dynamic=True)
    def get_greeting(self, name: str, args: Sequence[RawValue]) -> str:
        return self.greeting


async def main():
    client = await Client.connect("localhost:7233")
    async with Worker(
        client,
        task_queue="hello-activity-task-queue",
        workflows=[DefaultWorkflow, GreetingWorkflow],
        activities=[default_greeting, compose_greeting],
    ):

        handle = await client.start_workflow(
            "UnregisteredWorkflowName",
            "World",
            id="hello-activity-workflow-id",
            task_queue="hello-activity-task-queue",
        )
        # Gets the current greeting
        current_greeting = await handle.query("unregistered-query")
        print(f"Current Greeting: {current_greeting}")

        # Sets the greeting to "Goodbye"
        await handle.signal("unregistered-signal", [RawValue("Goodbye")])

        result = await handle.result()
        print(f"Result: {result}")

        # Gets the final greeting
        current_greeting = await handle.query("unregistered-query")
        print(f"Final Greeting: {current_greeting}")


if __name__ == "__main__":
    asyncio.run(main())


""" @dacx
id: how-to-set-a-dynamic-workflow-in-python
title: How to set a Dynamic Workflow
label: Set a Dynamic Workflow
description: Use `dynamic=True` on the `@workflow.defn` decorator to make a Workflow dynamic.
tags:
 - dynamic workflow
 - python sdk
 - code sample
lines: 11-16, 66-79, 100-105
@dacx """

""" @dacx
id: how-to-set-a-dynamic-activity-in-python
title: How to set a Dynamic Activity
label: Set a Dynamic Activity
description: Use `dynamic=True` on the `@activity.defn` decorator to make an Activity dynamic.
tags:
 - dynamic activity
 - python sdk
 - code sample
lines: 18-24, 45-47, 72-79
@dacx """

""" @dacx
id: how-to-set-a-dynamic-signal-in-python
title: How to set a Dynamic Signal
label: Set a Dynamic Signal
description: Use `dynamic=True` on the `@workflow.signal` decorator to make a Signal dynamic.
tags:
 - dynamic signal
 - python sdk
 - code sample
lines: 26-30, 81-84, 111
@dacx"""

""" @dacx
id: how-to-set-a-dynamic-query-in-python
title: How to set a Dynamic Query
label: Set a Dynamic Query
description: Use `dynamic=True` on the `@workflow.query` decorator to make a Query dynamic.
tags:
 - dynamic query
 - python sdk
 - code sample
lines: 32-36, 86-88, 107-108
@dacx"""
