import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from backgroundcheck import BackgroundCheck
from backgroundcheck_non_deterministic_code import BackgroundCheckNonDeterministic
from ssntraceactivity import ssn_trace_activity


async def main():
    client = await Client.connect(
        "localhost:7233", namespace="backgroundcheck_namespace"
    )

    worker = Worker(
        client,
        task_queue="backgroundcheck-boilerplate-task-queue-local",
        workflows=[BackgroundCheck, BackgroundCheckNonDeterministic],
        activities=[ssn_trace_activity],
    )

    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
