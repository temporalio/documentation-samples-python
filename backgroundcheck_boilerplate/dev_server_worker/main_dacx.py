import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import ssn_trace_activity
from workflows import BackgroundCheck

"""dacx
To run a Worker Process with a local development server, define the following steps in code:

- Initialize a Temporal Client.
- Create a new Worker by passing the Client to creation call.
- Register the application's Workflow and Activity functions.
- Call run on the Worker.

In regards to organization, we recommend keeping Worker code separate from Workflow and Activity code.
dacx"""


async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="background-check-boilerplate-task-queue",
        workflows=[BackgroundCheck],
        activities=[ssn_trace_activity],
    )

    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())

""" @dacx
id: backgroundcheck-boilerplate-run-a-dev-server-worker
title: Run a dev server Worker
description: Define the code needed to run a Worker Process in Go.
label: Dev server Worker
lines: 9-18, 1-7, 21-31
tags:
- worker
- developer guide
- temporal client
@dacx """
