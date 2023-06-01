import asyncio

from temporalio import workflow

"""dacx
To Continue-As-New in Python, call the [`continue_as_new()`](https://python.temporal.io/temporalio.workflow.html#continue_as_new) function from inside your Workflow, which will stop the Workflow immediately and Continue-As-New.
dacx"""


@workflow.defn
class LoopingWorkflow:
    @workflow.run
    async def run(self, iteration: int) -> None:
        if iteration == 5:
            return
        await asyncio.sleep(1)
        workflow.continue_as_new(iteration + 1)


""" @dacx
id: how-to-continue-as-new-in-python
title: How to Continue-As-New in Python
label: Continue-As-New
description: To Continue-As-New in Python, call the continue_as_new() function from inside your Workflow, which will stop the Workflow immediately and Continue-As-New.
lines: 5-7, 17
@dacx """
