import asyncio

from temporalio import workflow

@workflow.defn
class LoopingWorkflow:
    @workflow.run
    async def run(self, iteration: int) -> None:
        if iteration == 5:
            return
        await asyncio.sleep(1)
        workflow.continue_as_new(iteration + 1)
