import argparse
import asyncio

from temporalio.client import Client

from workflow_1_initial import BackgroundCheck


async def main():
    parser = argparse.ArgumentParser(description="Run worker")
    parser.add_argument("--start-workflow", help="Start workflow with this ID")
    parser.add_argument("--query-workflow", help="Query workflow with this ID")
    args = parser.parse_args()
    if not args.start_workflow and not args.query_workflow:
        raise RuntimeError("Either --start-workflow or --query-workflow is required")

    # Connect client
    client = await Client.connect(
        "localhost:7233", namespace="backgroundcheck_namespace"
    )

    if args.start_workflow:
        handle = await client.start_workflow(
            BackgroundCheck.run,
            id=args.start_workflow,
            task_queue="backgroundcheck-boilerplate-task-queue-local",
        )
        print(f"Started workflow with ID {handle.id} and run ID {handle.result_run_id}")
    if args.query_workflow:
        handle = client.get_workflow_handle_for(
            BackgroundCheck.run, args.query_workflow
        )
        result = await handle.query(BackgroundCheck.result)
        print(f"Query result for ID {handle.id}: {result}")


if __name__ == "__main__":
    asyncio.run(main())
