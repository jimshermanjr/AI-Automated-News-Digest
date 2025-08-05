module "ebToLambda" {
    source = "git::https://github.com/jimshermanjr/awsModules.git//modules/eventBridgeSchedule_lambda/module"
    function_name        = var.function_name
    lambda_source_path   = var.lambda_source_path
    handler              = var.handler
    runtime              = var.runtime
    schedule_expression  = var.schedule_expression
    lambda_role_arn      = var.lambda_role_arn
}

module "lambdaToSes" {
    source              = "git::https://github.com/jimshermanjr/awsModules.git//modules/lambda_sesEmailIdentity/module"
    senderEmail         = var.senderEmail
    lambda_role_name    = var.lambda_role_name
}