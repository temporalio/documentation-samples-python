import asyncio
import os

from temporalio.client import Client, TLSConfig
from temporalio.worker import Worker

from activities import ssn_trace_activity
from workflows import BackgroundCheck

"""dacx
Set IP address, port, and Namespace in the Temporal Client options.
dacx"""

async def main():

    with open(os.getenv("TEMPORAL_MTLS_TLS_CERT"), "rb") as f:
        client_cert = f.read()

    with open(os.getenv("TEMPORAL_MTLS_TLS_KEY"), "rb") as f:
        client_key = f.read()

    client = await Client.connect(
        os.getenv("TEMPORAL_HOST_URL"),
        namespace=os.getenv("TEMPORAL_NAMESPACE"),
        tls=TLSConfig(
            client_cert=client_cert,
            client_private_key=client_key,
        ),
    )

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
id: backgroundcheck-boilerplate-self-hosted-worker
title: Customize Client options
description: Configure the Temporal Client with the specific IP Address of the Temporal Server on your network.
label: Self-hosted Client options
lines: 1-40
tags:
- worker
- self-hosted
- developer guide
@dacx """
