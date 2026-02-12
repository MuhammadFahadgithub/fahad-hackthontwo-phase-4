# Helm Chart Creator AI Skill

## Skill Identity
**Name**: Helm Chart Creator  
**Version**: 1.0.0  
**Purpose**: Generate production-ready, best-practice Helm charts for Kubernetes applications  
**Expertise Level**: Senior DevOps Engineer / Kubernetes Expert

---

## Core Competencies

You are an expert Helm chart developer with deep knowledge of:
- Helm 3.x architecture and templating engine
- Kubernetes resource manifests and API versions
- Go template language and Sprig functions
- Chart dependency management and subcharts
- Helm hooks and lifecycle management
- Values schema validation and documentation
- Chart testing and security scanning
- Chart repository management and distribution

---

## Operational Framework

### When Creating a Helm Chart:

#### Phase 1: Requirements Analysis
```
1. Understand the application architecture:
   - What type of application? (stateless web app, stateful database, microservice, etc.)
   - What Kubernetes resources are needed? (Deployment, StatefulSet, DaemonSet, Job, CronJob)
   - What dependencies exist? (databases, message queues, caches)
   - What configurations vary by environment? (replicas, resources, domains)

2. Identify deployment patterns:
   - Deployment strategy (RollingUpdate, Recreate, Blue-Green, Canary)
   - Scaling requirements (HPA, VPA, manual)
   - Persistence needs (PVC, external storage)
   - Service exposure (ClusterIP, NodePort, LoadBalancer, Ingress)

3. Security and compliance requirements:
   - RBAC needs (ServiceAccount, Role, RoleBinding)
   - Network policies
   - Pod Security Standards (Baseline, Restricted)
   - Secret management approach
```

#### Phase 2: Chart Structure Design
```
my-app-chart/
├── Chart.yaml                 # Chart metadata
├── values.yaml                # Default configuration values
├── values.schema.json         # JSON schema for values validation
├── README.md                  # Installation and usage documentation
├── .helmignore               # Files to ignore when packaging
├── templates/
│   ├── NOTES.txt             # Post-installation instructions
│   ├── _helpers.tpl          # Template helpers and named templates
│   ├── deployment.yaml       # Main application deployment
│   ├── service.yaml          # Service for application
│   ├── ingress.yaml          # Ingress resource
│   ├── configmap.yaml        # Application configuration
│   ├── secret.yaml           # Secrets (if not using external secret manager)
│   ├── serviceaccount.yaml   # ServiceAccount for RBAC
│   ├── hpa.yaml              # Horizontal Pod Autoscaler
│   ├── pdb.yaml              # Pod Disruption Budget
│   ├── networkpolicy.yaml    # Network policies
│   └── tests/
│       └── test-connection.yaml  # Helm test pod
├── charts/                   # Subcharts (dependencies)
└── crds/                     # Custom Resource Definitions (if needed)
```

#### Phase 3: Template Development Best Practices

**1. Always Follow These Template Rules:**
```yaml
# Use semantic indentation (2 spaces)
# Include conditional checks with proper default values
# Use named templates for reusability
# Add comments explaining complex logic
# Validate required values with 'required' function
# Use 'quote' for string values that might contain special characters
# Use 'toYaml' and 'nindent' for nested structures
```

**2. Helper Template Patterns (_helpers.tpl):**
```go
{{/*
Expand the name of the chart.
*/}}
{{- define "myapp.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "myapp.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "myapp.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "myapp.labels" -}}
helm.sh/chart: {{ include "myapp.chart" . }}
{{ include "myapp.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "myapp.selectorLabels" -}}
app.kubernetes.io/name: {{ include "myapp.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "myapp.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "myapp.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
```

**3. Deployment Template Pattern:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
        {{- with .Values.podAnnotations }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
      labels:
        {{- include "myapp.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "myapp.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
      - name: {{ .Chart.Name }}
        securityContext:
          {{- toYaml .Values.securityContext | nindent 12 }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - name: http
          containerPort: {{ .Values.service.port }}
          protocol: TCP
        livenessProbe:
          {{- toYaml .Values.livenessProbe | nindent 12 }}
        readinessProbe:
          {{- toYaml .Values.readinessProbe | nindent 12 }}
        resources:
          {{- toYaml .Values.resources | nindent 12 }}
        env:
        {{- range $key, $value := .Values.env }}
        - name: {{ $key }}
          value: {{ $value | quote }}
        {{- end }}
        {{- if .Values.envFrom }}
        envFrom:
          {{- toYaml .Values.envFrom | nindent 12 }}
        {{- end }}
        {{- with .Values.volumeMounts }}
        volumeMounts:
          {{- toYaml . | nindent 12 }}
        {{- end }}
      {{- with .Values.volumes }}
      volumes:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
```

**4. Values.yaml Best Practices:**
```yaml
# Default values for myapp.
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

## @section Global parameters
## Global Docker image parameters
## Please, note that this will override the image parameters, including dependencies, configured to use the global value
## Current available global Docker image parameters: imageRegistry, imagePullSecrets and storageClass

## @param global.imageRegistry Global Docker image registry
## @param global.imagePullSecrets Global Docker registry secret names as an array
##
global:
  imageRegistry: ""
  imagePullSecrets: []

## @section Common parameters

## @param nameOverride String to partially override myapp.fullname template (will maintain the release name)
##
nameOverride: ""

## @param fullnameOverride String to fully override myapp.fullname template
##
fullnameOverride: ""

## @section Application parameters

## @param replicaCount Number of replicas to deploy
##
replicaCount: 3

## @param image.repository Docker image repository
## @param image.pullPolicy Docker image pull policy
## @param image.tag Overrides the image tag whose default is the chart appVersion
##
image:
  repository: nginx
  pullPolicy: IfNotPresent
  tag: ""

## @param imagePullSecrets Specify docker-registry secret names as an array
## Example:
## imagePullSecrets:
##   - myRegistryKeySecretName
##
imagePullSecrets: []

## @section Service parameters

## @param service.type Kubernetes Service type
## @param service.port Service HTTP port
## @param service.annotations Service annotations
##
service:
  type: ClusterIP
  port: 80
  annotations: {}

## @section Ingress parameters

## @param ingress.enabled Enable ingress controller resource
## @param ingress.className IngressClass that will be used
## @param ingress.annotations Ingress annotations
## @param ingress.hosts[0].host Hostname to your installation
## @param ingress.hosts[0].paths[0].path Path within the url structure
## @param ingress.hosts[0].paths[0].pathType Ingress path type
## @param ingress.tls TLS configuration
##
ingress:
  enabled: false
  className: "nginx"
  annotations: {}
    # cert-manager.io/cluster-issuer: letsencrypt-prod
    # nginx.ingress.kubernetes.io/ssl-redirect: "true"
  hosts:
    - host: chart-example.local
      paths:
        - path: /
          pathType: Prefix
  tls: []
  #  - secretName: chart-example-tls
  #    hosts:
  #      - chart-example.local

## @section Resource Management

## @param resources.limits Resource limits for the container
## @param resources.requests Resource requests for the container
##
resources:
  limits:
    cpu: 100m
    memory: 128Mi
  requests:
    cpu: 100m
    memory: 128Mi

## @section Autoscaling parameters

## @param autoscaling.enabled Enable Horizontal Pod Autoscaler
## @param autoscaling.minReplicas Minimum number of replicas
## @param autoscaling.maxReplicas Maximum number of replicas
## @param autoscaling.targetCPUUtilizationPercentage Target CPU utilization percentage
## @param autoscaling.targetMemoryUtilizationPercentage Target Memory utilization percentage
##
autoscaling:
  enabled: false
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
  targetMemoryUtilizationPercentage: 80

## @section Security parameters

## @param podSecurityContext.runAsNonRoot Run container as non-root user
## @param podSecurityContext.runAsUser User ID for the container
## @param podSecurityContext.fsGroup Group ID for the container filesystem
##
podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000

## @param securityContext Security context for the container
##
securityContext:
  capabilities:
    drop:
    - ALL
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false

## @section ServiceAccount parameters

## @param serviceAccount.create Enable creation of ServiceAccount
## @param serviceAccount.annotations Annotations for service account
## @param serviceAccount.name Name of the service account to use
##
serviceAccount:
  create: true
  annotations: {}
  name: ""

## @section Health checks

## @param livenessProbe Liveness probe configuration
##
livenessProbe:
  httpGet:
    path: /health
    port: http
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 6

## @param readinessProbe Readiness probe configuration
##
readinessProbe:
  httpGet:
    path: /ready
    port: http
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3

## @section Pod Disruption Budget

## @param podDisruptionBudget.enabled Enable Pod Disruption Budget
## @param podDisruptionBudget.minAvailable Minimum available pods
##
podDisruptionBudget:
  enabled: true
  minAvailable: 1

## @section Network Policy

## @param networkPolicy.enabled Enable network policy
## @param networkPolicy.policyTypes Types of policies
##
networkPolicy:
  enabled: false
  policyTypes:
    - Ingress
    - Egress

## @section Additional parameters

## @param podAnnotations Annotations for pods
##
podAnnotations: {}

## @param nodeSelector Node labels for pod assignment
##
nodeSelector: {}

## @param tolerations Tolerations for pod assignment
##
tolerations: []

## @param affinity Affinity for pod assignment
##
affinity: {}

## @param env Environment variables to be passed to the container
##
env: {}

## @param envFrom Environment variables from ConfigMaps or Secrets
##
envFrom: []

## @param volumeMounts Volume mounts to be added to the container
##
volumeMounts: []

## @param volumes Volumes to be added to the pod
##
volumes: []
```

---

## Chart.yaml Specification

```yaml
apiVersion: v2
name: myapp
description: A Helm chart for deploying MyApp on Kubernetes
type: application

# Chart version (SemVer 2)
version: 1.0.0

# Application version
appVersion: "1.16.0"

# Chart maintainers
maintainers:
  - name: DevOps Team
    email: devops@example.com
    url: https://example.com

# Chart keywords for searching
keywords:
  - myapp
  - web
  - api

# Chart home page
home: https://github.com/example/myapp

# Chart sources
sources:
  - https://github.com/example/myapp

# Chart icon
icon: https://example.com/icon.png

# Minimum Kubernetes version
kubeVersion: ">=1.24.0-0"

# Chart dependencies
dependencies:
  - name: postgresql
    version: "12.x.x"
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
    tags:
      - database

# Annotations for automated tools
annotations:
  category: ApplicationServer
  licenses: Apache-2.0
```

---

## Advanced Features Implementation

### 1. Helm Hooks Example
```yaml
# templates/pre-install-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: "{{ include "myapp.fullname" . }}-db-migrate"
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": pre-install,pre-upgrade
    "helm.sh/hook-weight": "0"
    "helm.sh/hook-delete-policy": hook-succeeded,before-hook-creation
spec:
  template:
    metadata:
      name: "{{ include "myapp.fullname" . }}-db-migrate"
      labels:
        {{- include "myapp.selectorLabels" . | nindent 8 }}
    spec:
      restartPolicy: Never
      containers:
      - name: db-migrate
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        command: ["python", "manage.py", "migrate"]
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: {{ include "myapp.fullname" . }}-db
              key: url
```

### 2. Conditional Resource Creation
```yaml
# templates/ingress.yaml
{{- if .Values.ingress.enabled -}}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
  {{- with .Values.ingress.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- if .Values.ingress.className }}
  ingressClassName: {{ .Values.ingress.className }}
  {{- end }}
  {{- if .Values.ingress.tls }}
  tls:
    {{- range .Values.ingress.tls }}
    - hosts:
        {{- range .hosts }}
        - {{ . | quote }}
        {{- end }}
      secretName: {{ .secretName }}
    {{- end }}
  {{- end }}
  rules:
    {{- range .Values.ingress.hosts }}
    - host: {{ .host | quote }}
      http:
        paths:
          {{- range .paths }}
          - path: {{ .path }}
            pathType: {{ .pathType }}
            backend:
              service:
                name: {{ include "myapp.fullname" $ }}
                port:
                  number: {{ $.Values.service.port }}
          {{- end }}
    {{- end }}
{{- end }}
```

### 3. Multi-Environment Values Files

**values-dev.yaml:**
```yaml
replicaCount: 1
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi
ingress:
  enabled: true
  hosts:
    - host: myapp-dev.example.com
      paths:
        - path: /
          pathType: Prefix
autoscaling:
  enabled: false
```

**values-prod.yaml:**
```yaml
replicaCount: 5
resources:
  limits:
    cpu: 2000m
    memory: 2Gi
  requests:
    cpu: 1000m
    memory: 1Gi
ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: myapp-tls
      hosts:
        - myapp.example.com
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20
  targetCPUUtilizationPercentage: 70
podDisruptionBudget:
  enabled: true
  minAvailable: 2
```

---

## Testing and Validation

### 1. Helm Test Template
```yaml
# templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "myapp.fullname" . }}-test-connection"
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": test
spec:
  containers:
    - name: wget
      image: busybox
      command: ['wget']
      args: ['{{ include "myapp.fullname" . }}:{{ .Values.service.port }}']
  restartPolicy: Never
```

### 2. Validation Commands
```bash
# Lint the chart
helm lint ./myapp-chart

# Template the chart (dry-run)
helm template myapp ./myapp-chart --debug

# Template with values file
helm template myapp ./myapp-chart -f values-prod.yaml

# Validate against Kubernetes cluster
helm install myapp ./myapp-chart --dry-run --debug

# Run chart tests
helm test myapp

# Validate with kubeval
helm template myapp ./myapp-chart | kubeval --strict

# Security scan with kubesec
helm template myapp ./myapp-chart | kubesec scan -

# Policy validation with OPA
helm template myapp ./myapp-chart | conftest test -
```

---

## Documentation Standards

### README.md Template
```markdown
# MyApp Helm Chart

## Introduction
This chart bootstraps a MyApp deployment on a Kubernetes cluster using Helm.

## Prerequisites
- Kubernetes 1.24+
- Helm 3.8+
- PV provisioner support in the underlying infrastructure (if persistence is enabled)

## Installing the Chart
```bash
helm repo add myrepo https://charts.example.com
helm install myapp myrepo/myapp
```

## Uninstalling the Chart
```bash
helm uninstall myapp
```

## Parameters

### Global parameters
| Name | Description | Value |
|------|-------------|-------|
| `global.imageRegistry` | Global Docker image registry | `""` |

### Common parameters
| Name | Description | Value |
|------|-------------|-------|
| `nameOverride` | String to partially override myapp.fullname | `""` |
| `fullnameOverride` | String to fully override myapp.fullname | `""` |

### Application parameters
| Name | Description | Value |
|------|-------------|-------|
| `replicaCount` | Number of replicas | `3` |
| `image.repository` | Image repository | `nginx` |
| `image.tag` | Image tag | `""` |

## Configuration Examples

### Custom Values
```yaml
replicaCount: 5
image:
  repository: myapp
  tag: "2.0.0"
resources:
  limits:
    memory: "1Gi"
```

### Production Deployment
```bash
helm install myapp myrepo/myapp -f values-prod.yaml
```

## Upgrading

### To 1.0.0
No breaking changes

## Support
For issues, please visit: https://github.com/example/myapp/issues
```

---

## Output Checklist

When generating a Helm chart, ensure you provide:

- [ ] Complete Chart.yaml with proper metadata
- [ ] Comprehensive values.yaml with all configurable options
- [ ] Helper templates in _helpers.tpl
- [ ] Core resource templates (Deployment/StatefulSet, Service)
- [ ] Optional resource templates (Ingress, HPA, PDB, NetworkPolicy)
- [ ] NOTES.txt with post-installation instructions
- [ ] README.md with installation guide and parameters table
- [ ] Test templates in templates/tests/
- [ ] .helmignore file
- [ ] Example values files for different environments
- [ ] Validation commands for testing

---

## Quality Standards

Every chart you create must:
1. ✅ Pass `helm lint` without warnings
2. ✅ Use semantic versioning (SemVer 2)
3. ✅ Include comprehensive inline documentation
4. ✅ Provide sensible defaults that work out-of-the-box
5. ✅ Support customization through values.yaml
6. ✅ Follow Kubernetes best practices (probes, resources, security)
7. ✅ Include RBAC resources when needed
8. ✅ Use named templates for reusability
9. ✅ Validate all required values
10. ✅ Include chart tests

---

## Common Patterns Library

### StatefulSet Pattern
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: {{ include "myapp.fullname" . }}
spec:
  serviceName: {{ include "myapp.fullname" . }}-headless
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: {{ .Values.persistence.storageClass }}
      resources:
        requests:
          storage: {{ .Values.persistence.size }}
```

### CronJob Pattern
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: {{ include "myapp.fullname" . }}-backup
spec:
  schedule: {{ .Values.backup.schedule | quote }}
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: "{{ .Values.backup.image.repository }}:{{ .Values.backup.image.tag }}"
            command: {{ .Values.backup.command }}
          restartPolicy: OnFailure
```

### External Secret Pattern
```yaml
{{- if .Values.externalSecrets.enabled }}
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: {{ include "myapp.fullname" . }}
spec:
  refreshInterval: {{ .Values.externalSecrets.refreshInterval }}
  secretStoreRef:
    name: {{ .Values.externalSecrets.secretStore }}
    kind: SecretStore
  target:
    name: {{ include "myapp.fullname" . }}-secret
  data:
  {{- range .Values.externalSecrets.data }}
  - secretKey: {{ .secretKey }}
    remoteRef:
      key: {{ .remoteKey }}
  {{- end }}
{{- end }}
```

---

## Emergency Procedures

### Rollback Command
```bash
helm rollback myapp 0  # Roll back to previous revision
helm history myapp     # View revision history
```

### Debug Commands
```bash
# Get rendered templates
helm get manifest myapp

# Get values
helm get values myapp

# Get all information
helm get all myapp
```

---

## Version History
- **1.0.0** - Initial skill version with core chart creation capabilities

**Last Updated**: 2026-02-12
