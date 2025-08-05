output "lambda_arn" {
  value = module.ebToLambda.lambda_arn
}

output "eventbridge_rule_name" {
  value = module.ebToLambda.eventbridge_rule_name
}

output "ses_identity_arn" {
    value = module.lambdaToSes.ses_identity_arn
}