import os

import pytest

from edenai_apis import Image
from edenai_apis.interface import list_providers
from edenai_apis.loaders.loaders import load_feature
from edenai_apis.loaders.data_loader import FeatureDataEnum
from edenai_apis.utils.constraints import validate_all_provider_constraints

automl_image_providers = sorted(
    list_providers(feature="image", subfeature="automl_classification")
)
MAX_TIME = 180
TIME_BETWEEN_CHECK = 10


@pytest.mark.skipif(
    os.environ.get("TEST_SCOPE") == "CICD-OPENSOURCE",
    reason="Skip in opensource package cicd workflow",
)
@pytest.mark.parametrize(("provider"), automl_image_providers)
@pytest.mark.xdist_group(name="image_automl_classification")
class TestImageAutomlClassification:
    def test_create_project(self, provider):
        feature_args = load_feature(
            FeatureDataEnum.SAMPLES_ARGS,
            feature="image",
            subfeature="automl_classification",
            phase="create_project",
            provider_name=provider,
        )
        feature_args = validate_all_provider_constraints(
            provider,
            "image",
            "automl_classification",
            "create_project",
            feature_args,
        )
        try:
            create_project_method = Image.automl_classification__create_project(
                provider
            )
        except AttributeError:
            raise AttributeError("Could not create project phase.")

        create_project_output = create_project_method(**feature_args).model_dump()

        assert create_project_output.get("status") == "success", "Create Project failed"
