import os
import logging
import hydra
import mlflow


import aiap_team6_miniproject as team6_miniproject


@hydra.main(config_path="../conf/base", config_name="pipelines.yml")
def main(args):
    """This main function does the following:
    - load logging config
    - initialise experiment tracking (MLflow)
    - loads training, validation and test data
    - initialises model layers and compile
    - trains, evaluates, and then exports the model
    """

    logger = logging.getLogger(__name__)
    logger.info("Setting up logging configuration.")
    logger_config_path = os.path.\
        join(hydra.utils.get_original_cwd(),
            "conf/base/logging.yml")
    team6_miniproject.general_utils.setup_logging(logger_config_path)

    mlflow_init_status, mlflow_run = team6_miniproject.general_utils.\
        mlflow_init(
            args, setup_mlflow=args["train"]["setup_mlflow"],
            autolog=args["train"]["mlflow_autolog"])
    team6_miniproject.general_utils.\
        mlflow_log(
            mlflow_init_status, "log_params",
            params=args["train"])

    if "POLYAXON_RUN_UUID" in os.environ:
        team6_miniproject.general_utils.\
            mlflow_log(
                mlflow_init_status, "log_param",
                key="polyaxon_run_uuid",
                value=os.environ["POLYAXON_RUN_UUID"])

    datasets = team6_miniproject.modeling.data_loaders.\
        load_datasets(hydra.utils.get_original_cwd(), args)

    model = team6_miniproject.modeling.models.seq_model(args)

    logger.info("Training the model...")
    model.fit(
        datasets["train"],
        epochs=args["train"]["epochs"],
        validation_data=datasets["val"])

    logger.info("Evaluating the model...")
    test_loss, test_acc = model.evaluate(datasets["test"])

    logger.info("Test Loss: {}, Test Accuracy: {}".\
        format(test_loss, test_acc))

    logger.info("Exporting the model...")
    team6_miniproject.modeling.utils.export_model(model)

    if mlflow_init_status:
        artifact_uri = mlflow.get_artifact_uri()
        logger.info("Artifact URI: {}".format(artifact_uri))
        team6_miniproject.general_utils.\
            mlflow_log(
                mlflow_init_status, "log_params",
                params={"artifact_uri": artifact_uri})
        logger.info("Model training with MLflow run ID {} has completed.".
            format(mlflow_run.info.run_id))
        mlflow.end_run()
    else:
        logger.info("Model training has completed.")


if __name__ == "__main__":
    main()
