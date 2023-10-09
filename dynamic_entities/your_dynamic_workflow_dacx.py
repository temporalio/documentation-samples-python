import asyncio
from dataclasses import dataclass
from datetime import timedelta
from typing import Sequence

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.common import RawValue
from temporalio.worker import Worker

"""dacx
A Dynamic Workflow in Temporal is an Workflow that is invoked dynamically at runtime if no other Workflow with the same name is registered.
A Workflow can be made dynamic by adding `dynamic=True` to the `@workflow.defn` decorator.
You must register the Workflow with the [Worker](https://python.temporal.io/temporalio.worker.html) before it can be invoked.

The Workflow function must then accept a single argument of type `Sequence[temporalio.common.RawValue]`.
The [payload_converter()](https://python.temporal.io/temporalio.workflow.html#payload_converter) function is used to convert a `RawValue` object to the desired type.
dacx"""


@dataclass
class YourDataClass:
    greeting: str
    name: str


@activity.defn()
async def default_greeting(input: YourDataClass) -> str:
    return f"{input.greeting}, {input.name}!\nActivity Type: {activity.info().activity_type}"


@workflow.defn(dynamic=True)
class DynamicWorkflow:
    @workflow.run
    async def run(self, args: Sequence[RawValue]) -> str:
        name = workflow.payload_converter().from_payload(args[0].payload, str)
        return await workflow.execute_activity(
            default_greeting,
            YourDataClass("Hello", name),
            start_to_close_timeout=timedelta(seconds=10),
        )


async def main():
    client = await Client.connect("localhost:7233")
    async with Worker(
        client,
        task_queue="dynamic-workflow-task-queue",
        workflows=[DynamicWorkflow],
        activities=[default_greeting],
    ):

        result = await client.execute_workflow(
            "UnregisteredWorkflowType",
            "Dynamic Workflow argument",
            id="hello-dynamic-workflow-id",
            task_queue="dynamic-workflow-task-queue",
        )
        print(f"Result: {result}")


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
lines: 11-18, 32-41, 44-59
@dacx """
