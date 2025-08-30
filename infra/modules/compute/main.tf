# Compute module - EC2 instances, load balancer
# MOCK/DRY-RUN ONLY - Safe for terraform validate/plan

locals {
  # Size mappings for different deployment sizes
  size_config = {
    small = {
      instance_type  = "t3.micro"
      instance_count = 1
    }
    medium = {
      instance_type  = "t3.small"
      instance_count = 2
    }
    large = {
      instance_type  = "t3.medium"
      instance_count = 3
    }
  }

  instance_type  = local.size_config[var.size].instance_type
  instance_count = local.size_config[var.size].instance_count
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

resource "aws_launch_template" "app" {
  name_prefix   = "${var.customer_id}-app-"
  image_id      = data.aws_ami.amazon_linux.id
  instance_type = local.instance_type

  vpc_security_group_ids = [var.security_group_id]

  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    customer_id = var.customer_id
  }))

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name        = "${var.customer_id}-app"
      Environment = var.environment
      Customer    = var.customer_id
      Size        = var.size
    }
  }

  tags = {
    Name        = "${var.customer_id}-app-template"
    Environment = var.environment
    Customer    = var.customer_id
  }
}

resource "aws_autoscaling_group" "app" {
  name               = "${var.customer_id}-app-asg"
  vpc_zone_identifier = var.subnet_ids
  target_group_arns   = [aws_lb_target_group.app.arn]
  health_check_type   = "ELB"

  min_size         = local.instance_count
  max_size         = local.instance_count * 2
  desired_capacity = local.instance_count

  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "${var.customer_id}-app-asg"
    propagate_at_launch = false
  }

  tag {
    key                 = "Environment"
    value               = var.environment
    propagate_at_launch = true
  }

  tag {
    key                 = "Customer"
    value               = var.customer_id
    propagate_at_launch = true
  }
}

resource "aws_lb" "app" {
  name               = "${var.customer_id}-app-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [var.security_group_id]
  subnets            = var.subnet_ids

  tags = {
    Name        = "${var.customer_id}-app-lb"
    Environment = var.environment
    Customer    = var.customer_id
  }
}

resource "aws_lb_target_group" "app" {
  name     = "${var.customer_id}-app-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 30
    path                = "/health"
    matcher             = "200"
  }

  tags = {
    Name        = "${var.customer_id}-app-tg"
    Environment = var.environment
    Customer    = var.customer_id
  }
}

resource "aws_lb_listener" "app" {
  load_balancer_arn = aws_lb.app.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}
