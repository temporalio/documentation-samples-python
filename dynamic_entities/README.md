# Dynamic Entities README

Temporal supports Dynamic Workflows, Activities, Signals, and Queries.
These are unnamed entities that are invoked if no other statically defined entity with the given name exists.

This is a sample project to demonstrate how to use the Dynamic Entities.

1. Run the following at the root of the directory.

```bash
poetry install
```

2. Start your Worker and run your Workflow

Starts the Worker and runs the Workflow.

```bash
poetry run python your_dynamic_entity_dacx.py
```

```output
Current Greeting: Hello
Result: [RawValue(payload=metadata {
  key: "messageType"
  value: "temporal.api.common.v1.Payload"
}
metadata {
  key: "encoding"
  value: "json/protobuf"
}
data: "{\"data\":\"IldvcmxkIg==\",\"metadata\":{\"encoding\":\"anNvbi9wbGFpbg==\"}}"
)]!
Final Greeting: metadata {
  key: "encoding"
  value: "json/plain"
}
data: "[{\"payload\":\"Goodbye\"}]"
```

Dynamic Entities provide flexibility to handle cases where the names of Workflows, Activities, Signals, or Queries are not known at run time.