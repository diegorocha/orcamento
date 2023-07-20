locals {
  app_envs = {
    DEBUG                   = "False"
    CONTAS_URL              = "https://orcamento-contas.diegorocha.com.br"
    CORS_ORIGIN_WHITELIST   = "orcamento-contas.diegorocha.com.br,localhost:3000"
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
  app_secrets = {
    DATABASE_URL        = "database_url"
    SECRET              = "secret"
    EMAIL_HOST_USER     = "email_host_user"
    EMAIL_HOST_PASSWORD = "email_host_password"
  }
  app_healthcheck = {
    path    = "/healthcheck/"
    port    = 80
    period  = 15
    initial = 15
  }
  database_name = "raych"
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

resource "kubernetes_manifest" "backend_config_orcamento" {
  manifest = {
    apiVersion = "cloud.google.com/v1"
    kind       = "BackendConfig"

    metadata = {
      name      = "orcamento"
      namespace = local.namespace
    }

    spec = {
      healthCheck = {
        checkIntervalSec = local.app_healthcheck.period
        port             = local.app_healthcheck.port
        type             = "HTTP"
        requestPath      = local.app_healthcheck.path
      }
    }
  }
}

resource "kubernetes_service" "orcamento" {
  metadata {
    name      = "orcamento"
    namespace = local.namespace
  }

  spec {
    selector = {
      app = "orcamento"
    }

    port {
      port        = 80
      target_port = 80
    }

    type = "NodePort"
  }

  lifecycle {
    ignore_changes = [
      metadata[0].annotations
    ]
  }
}

resource "kubernetes_annotations" "service_orcamento" {
  api_version = "v1"
  kind        = "Service"

  metadata {
    name = kubernetes_service.orcamento.metadata[0].name
  }

  annotations = {
    "cloud.google.com/neg" = jsonencode({
      ingress = true
    })
    "cloud.google.com/backend-config" = jsonencode({
      default = "orcamento"
    })
  }

  depends_on = [kubernetes_manifest.backend_config_orcamento]
}


resource "kubernetes_deployment" "orcamento" {
  metadata {
    name      = "orcamento"
    namespace = local.namespace
    labels = {
      app = "orcamento"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "orcamento"
      }
    }

    template {
      metadata {
        labels = {
          app = "orcamento"
        }
      }

      spec {
        container {
          image = "${var.app_image}:${var.app_version}"
          name  = "orcamento"

          resources {
            limits = {
              cpu               = "250m"
              memory            = "512Mi"
              ephemeral-storage = "128Mi"
            }
            requests = {
              cpu               = "250m"
              memory            = "512Mi"
              ephemeral-storage = "128Mi"
            }
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
              port = local.app_healthcheck.port
            }

            initial_delay_seconds = local.app_healthcheck.initial
            period_seconds        = local.app_healthcheck.period
          }

          liveness_probe {
            http_get {
              path = local.app_healthcheck.path
              port = local.app_healthcheck.port
            }

            initial_delay_seconds = local.app_healthcheck.initial
            period_seconds        = local.app_healthcheck.period
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
