locals {
  app_name = "orcamento"
  app_envs = {
    DEBUG                   = "False"
    CONTAS_URL              = "https://orcamento-contas.diegorocha.com.br"
    CORS_ORIGIN_WHITELIST   = "https://orcamento-contas.diegorocha.com.br"
    ADMIN_NAME              = "Diego Rocha"
    ADMIN_EMAIL             = "diego@diegorocha.com.br"
    USE_SMTP                = "True"
    EMAIL_HOST              = "email-smtp.us-east-1.amazonaws.com"
    EMAIL_PORT              = 587
    EMAIL_USE_TLS           = "True"
    DEFAULT_FROM_EMAIL      = "noreply@diegorocha.com.br"
    SERVER_EMAIL            = "noreply@diegorocha.com.br"
    STATIC_S3               = "True"
    AWS_STORAGE_BUCKET_NAME = "orcamento-static"
    AWS_S3_CUSTOM_DOMAIN    = "orcamento-static.diegorocha.com.br"
    AWS_QUERYSTRING_AUTH    = "False"
  }
  app_secret_name = "orcamento"
  app_timeout     = 60
  app_secrets = {
    DATABASE_URL        = "database_url"
    SECRET              = "secret"
    EMAIL_HOST_USER     = "email_host_user"
    EMAIL_HOST_PASSWORD = "email_host_password"
  }
  app_port = 80
  app_resources = {
    cpu               = "250m"
    memory            = "512Mi"
    ephemeral-storage = "128Mi"
  }
  app_healthcheck = {
    path    = "/healthcheck/"
    period  = 30
    initial = 15
    timeout = 5
  }
  database_name = "raych"
  gateway_name  = "gateway"
  namespace     = "default"
}

resource "kubernetes_secret" "orcamento" {
  metadata {
    name      = local.app_secret_name
    namespace = local.namespace
  }

  data = var.orcamento_secrets

  type = "Opaque"
}

resource "kubernetes_manifest" "healthcheck_policy" {
  manifest = {
    apiVersion = "networking.gke.io/v1"
    kind       = "HealthCheckPolicy"

    metadata = {
      name      = local.app_name
      namespace = local.namespace
    }

    spec = {
      default = {
        checkIntervalSec = local.app_healthcheck.period
        timeoutSec       = local.app_healthcheck.timeout
        config = {
          type = "HTTP"
          httpHealthCheck = {
            portSpecification = "USE_SERVING_PORT"
            requestPath       = local.app_healthcheck.path
          }
        }
      }
      targetRef = {
        group = ""
        kind  = "Service"
        name  = local.app_name
      }
    }
  }
}

resource "kubernetes_manifest" "backend_policy" {
  manifest = {
    apiVersion = "networking.gke.io/v1"
    kind       = "GCPBackendPolicy"

    metadata = {
      name      = local.app_name
      namespace = local.namespace
    }

    spec = {
      default = {
        timeoutSec = local.app_timeout
      }
      targetRef = {
        group = ""
        kind  = "Service"
        name  = local.app_name
      }
    }
  }
}

resource "kubernetes_service" "orcamento" {
  metadata {
    name      = local.app_name
    namespace = local.namespace
  }

  spec {
    selector = {
      app = local.app_name
    }

    port {
      port        = local.app_port
      target_port = local.app_port
    }

    type = "NodePort"
  }

  lifecycle {
    ignore_changes = [
      metadata[0].annotations
    ]
  }
}

resource "kubernetes_manifest" "route" {
  manifest = {
    apiVersion = "gateway.networking.k8s.io/v1beta1"
    kind       = "HTTPRoute"

    metadata = {
      name      = local.app_name
      namespace = local.namespace
    }

    spec = {
      parentRefs = [
        {
          name      = local.gateway_name
          namespace = local.namespace
        }
      ]
      hostnames = [
        local.subdomain
      ]
      rules = [
        {
          matches = [{
            path = {
              value = "/"
            }
          }]
          backendRefs = [{
            name = local.app_name
            port = local.app_port
          }]
        },
      ]
    }
  }
}

resource "kubernetes_deployment" "orcamento" {
  metadata {
    name      = local.app_name
    namespace = local.namespace
    labels = {
      app = local.app_name
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = local.app_name
      }
    }

    template {
      metadata {
        labels = {
          app = local.app_name
        }
      }

      spec {
        termination_grace_period_seconds = 25
        affinity {
          node_affinity {
            required_during_scheduling_ignored_during_execution {
              node_selector_term {
                match_expressions {
                  key      = "cloud.google.com/gke-spot"
                  operator = "In"
                  values   = ["true"]
                }
              }
            }
          }
        }
        container {
          image = "${var.app_image}:${var.app_version}"
          name  = local.app_name

          resources {
            limits   = local.app_resources
            requests = local.app_resources
          }

          security_context {
            allow_privilege_escalation = false
            privileged                 = false
            read_only_root_filesystem  = false
            run_as_non_root            = false

            capabilities {
              add = []
              drop = [
                "NET_RAW",
              ]
            }
          }

          readiness_probe {
            http_get {
              path = local.app_healthcheck.path
              port = local.app_port
            }

            initial_delay_seconds = local.app_healthcheck.initial
            period_seconds        = local.app_healthcheck.period
            timeout_seconds       = local.app_healthcheck.timeout
          }

          liveness_probe {
            http_get {
              path = local.app_healthcheck.path
              port = local.app_port
            }

            initial_delay_seconds = local.app_healthcheck.initial
            period_seconds        = local.app_healthcheck.period
            timeout_seconds       = local.app_healthcheck.timeout
          }

          dynamic "env" {
            for_each = local.app_envs
            iterator = each

            content {
              name  = each.key
              value = each.value
            }
          }

          dynamic "env" {
            for_each = local.app_secrets
            iterator = each

            content {
              name = each.key
              value_from {
                secret_key_ref {
                  name = local.app_secret_name
                  key  = each.value
                }
              }
            }
          }
        }
      }
    }
  }

  lifecycle {
    ignore_changes = [
      spec[0].template[0].spec[0].security_context,
      spec[0].template[0].spec[0].toleration,
    ]
  }

  depends_on = [
    kubernetes_secret.orcamento,
  ]
}
