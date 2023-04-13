import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import deposit, refund, withdraw
from workflow import MoneyTransferWorkflow


async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="money-transfer",
        workflows=[MoneyTransferWorkflow],
        activities=[withdraw, deposit, refund],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
