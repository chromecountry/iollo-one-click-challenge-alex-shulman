# DNS module - Route53 hosted zone, records, ACM certificate
# MOCK/DRY-RUN ONLY - Safe for terraform validate/plan

resource "aws_route53_zone" "main" {
  name = "${var.customer_id}.${var.domain_suffix}"

  tags = {
    Name        = "${var.customer_id}-zone"
    Environment = var.environment
    Customer    = var.customer_id
  }
}

resource "aws_route53_record" "app" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "app.${var.customer_id}.${var.domain_suffix}"
  type    = "A"

  alias {
    name                   = var.load_balancer_dns_name
    zone_id                = var.load_balancer_zone_id
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "www.${var.customer_id}.${var.domain_suffix}"
  type    = "CNAME"
  ttl     = 300
  records = ["app.${var.customer_id}.${var.domain_suffix}"]
}

# ACM certificate for SSL/TLS
resource "aws_acm_certificate" "main" {
  domain_name               = "${var.customer_id}.${var.domain_suffix}"
  subject_alternative_names = ["*.${var.customer_id}.${var.domain_suffix}"]
  validation_method         = "DNS"

  tags = {
    Name        = "${var.customer_id}-cert"
    Environment = var.environment
    Customer    = var.customer_id
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.main.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = aws_route53_zone.main.zone_id
}

resource "aws_acm_certificate_validation" "main" {
  certificate_arn         = aws_acm_certificate.main.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}
