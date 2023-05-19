import asyncio

from temporalio.client import Client
from signal_external_wf_dacx import WorkflowA, WorkflowB


async def main():
    client = await Client.connect("localhost:7233")
    handle_b = await client.start_workflow(
        WorkflowB.run,
        id="workflow-b",
        task_queue="signal-tq",
    )
    await handle_b.signal(WorkflowA.your_signal, "workflow-a")

    handle_a = await client.start_workflow(
        WorkflowA.run,
        id="workflow-a",
        task_queue="signal-tq",
    )
    result = await handle_a.result()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
