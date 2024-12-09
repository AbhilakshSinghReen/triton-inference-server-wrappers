import express from "express";
import { default as modelRepositoryState } from "../models-repository.json" with {type: "json"};
import { default as modelRequirements } from "../models-requirements.json" with {type: "json"};

const port = 8020;

const app = express();
app.use(express.json());

const currentResourcesConsumption = {
  cpu: 0.0,
  ram: 0.0,
  gpu: 0.0,
  vram: 0.0,
};

function getModelLoadingTime() {
  return 15 + Math.random() * 10;
}

function getModelUnloadingTime() {
  return 5 + Math.random() * 10;
}

function getModelInferenceTime() {
  return 2 + Math.random() * 7;
}

app.get("/occupied-resources", async (request, response) => {
  console.log("GET /occupied-resources");
  console.log("  currentResourcesConsumption:-");
    console.log(`  ${JSON.stringify(currentResourcesConsumption)}`);

    const modelRepositoryStateArray = [];
  for (const modelName in modelRepositoryState) {
    modelRepositoryStateArray.push(modelRepositoryState[modelName]);
  }


  return response.status(200).json({
    result: {
      current_resources_consumption: currentResourcesConsumption,
      model_repository_state: modelRepositoryStateArray,
    },
  });
});

app.get("/model-repository", async (request, response) => {
  console.log("GET /model-repository");
  console.log("  modelRepositoryState:-");
  console.log(`  ${JSON.stringify(modelRepositoryState)}`);

  const modelRepositoryStateArray = [];
  for (const modelName in modelRepositoryState) {
    modelRepositoryStateArray.push(modelRepositoryState[modelName]);
  }

  return response.status(200).json({
    result: {
      model_repository_state: modelRepositoryStateArray,
    },
  });
});

app.post("/load-model", async (request, response) => {
  console.log("POST /load-model");

  const { modelId } = request.query;
  console.log(`  modelId = ${modelId}`);

  if (modelRepositoryState[modelId].state === "READY") {
    console.log(`  model '${modelId}' already loaded`);
    console.log("  modelRepositoryState:-");
    console.log(`  ${JSON.stringify(modelRepositoryState)}`);

    return response.status(200).json({
      result: {
        message: "ok",
      },
    });
  }

  const modelRequiredResources = modelRequirements[modelId];

  for (const resourceName in currentResourcesConsumption) {
    if (currentResourcesConsumption[resourceName] + modelRequiredResources[resourceName] >= 1.0) {
      console.log(`  model '${modelId}' cannot be loaded due to RLE on resource ${resourceName}`);
      console.log("  modelRequiredResources:-");
      console.log(`  ${JSON.stringify(modelRequiredResources)}`);
      console.log("  currentResourcesConsumption:-");
      console.log(`  ${JSON.stringify(currentResourcesConsumption)}`);

      return response.status(500).json({
        error: {
          code: "resource_limit_exceeded",
        },
      });
    }
  }

  setTimeout(() => {
    for (const resourceName in currentResourcesConsumption) {
      currentResourcesConsumption[resourceName] += modelRequiredResources[resourceName];
    }

    modelRepositoryState[modelId].state = "READY";

    console.log(`  model '${modelId}' loaded successfully`);
    console.log("  modelRepositoryState:-");
    console.log(`  ${JSON.stringify(modelRepositoryState)}`);
    console.log("  currentResourcesConsumption:-");
    console.log(`  ${JSON.stringify(currentResourcesConsumption)}`);

    response.status(200).json({
      result: {
        message: "ok",
      },
    });
  }, getModelLoadingTime());
});

app.post("/unload-model", async (request, response) => {
  console.log("POST /unload-model");

  const { modelId } = request.query;
  console.log(`  modelId = ${modelId}`);

  if (modelRepositoryState[modelId].state === "UNLOADING") {
    console.log(`  model '${modelId}' is already being unloaded`);
    console.log("  modelRepositoryState:-");
    console.log(`  ${JSON.stringify(modelRepositoryState)}`);

    return response.status(200).json({
      result: {
        message: "ok",
      },
    });
  }

  if (modelRepositoryState[modelId].state === "UNAVAILABLE") {
    console.log(`  model '${modelId}' is already unloaded`);
    console.log("  modelRepositoryState:-");
    console.log(`  ${JSON.stringify(modelRepositoryState)}`);

    return response.status(200).json({
      result: {
        message: "ok",
      },
    });
  }

  modelRepositoryState[modelId].state = "UNLOADING";

  setTimeout(() => {
    const modelRequiredResources = modelRequirements[modelId];

    for (const resourceName in currentResourcesConsumption) {
      currentResourcesConsumption[resourceName] -= modelRequiredResources[resourceName];
      currentResourcesConsumption[resourceName] = Math.max(currentResourcesConsumption[resourceName], 0);
    }

    modelRepositoryState[modelId].state = "UNAVAILABLE";

    console.log("  ---> Model unloaded log");
    console.log(`    model '${modelId}' unloaded successfully`);
    console.log("    modelRepositoryState:-");
    console.log(`    ${JSON.stringify(modelRepositoryState)}`);
    console.log("  currentResourcesConsumption:-");
    console.log(`  ${JSON.stringify(currentResourcesConsumption)}`);
  }, getModelUnloadingTime());

  return response.status(200).json({
    result: {
      message: "ok",
    },
  });
});

app.post("/infer", async (request, response) => {
  console.log("POST /infer");

  const { modelId } = request.query;
  console.log(`  modelId = ${modelId}`);

  if (modelRepositoryState[modelId].state !== "READY") {
    console.log(`  model '${modelId}' is not loaded, cannot infer`);
    console.log("  modelRepositoryState:-");
    console.log(`  ${JSON.stringify(modelRepositoryState)}`);

    return response.status(400).json({
      error: {
        code: "model_not_ready",
        detail: `current state: ${modelRepositoryState[modelId].state}`,
      },
    });
  }

  setTimeout(() => {
    console.log(`  model '${modelId}' has run inference successfully`);

    response.status(200).json({
      result: {
        message: "ok",
      },
    });
  }, getModelInferenceTime());
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
