# Instructions
This is a bit more complicated than the tensorflow/serving counterpart.

For torchserve to work, we have to include a model archive, which is denoted in a .mar file.
This .mar file is created using the `torch-model-archiver` tool, where we have to include our serialized
model, as well as custom handlers and index to name mappings.

Handlers: define how the data is preprocessed, inferred, and then post processed for each model.

`index_to_name.json`: is automatically picked up by `torch-model-archiver` to give us access to self.mapping, so we
can return the proper labels in the post processing step. To create the archive, we have to run the following command:

```
MODEL_NAME=...
MODEL_FILE=...pt
EXPORT_PATH=...

torch-model-archiver --model-name $MODEL_NAME \
--serialized-file MODEL_FILE \
--extra-files ./index_to_name.json,./Handler.py \
--handler my_handler.py  \
--export-path $EXPORT_PATH -f
```

Once created, we can then run this as a single docker container with the command
```
docker run --rm -it \
-p 3000:8080 -p 3001:8081 \
-v $(pwd)/$EXPORT_PATH:/home/model-server/model-store pytorch/torchserve:0.1-cpu \
torchserve --start --model-store model-store --models $MODEL_NAME=$MODEL_NAME.mar
```

or in a `docker-compose.yaml` file, substituting the ports and volumes in the right location.