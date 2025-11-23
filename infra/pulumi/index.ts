import * as pulumi from "@pulumi/pulumi";
import * as gcp from "@pulumi/gcp";
import * as docker from "@pulumi/docker";

const cfg = new pulumi.Config();
const project = gcp.config.project;

if (!project) {
    throw new Error("Set gcp:project in Pulumi config or via PULUMI_CONFIG.");
}

const stack = pulumi.getStack();
const region = gcp.config.region || cfg.get("region") || "us-central1";
const location = region;
const prefix = cfg.get("namePrefix") ?? "hackaton";

const environment = cfg.get("environment") ?? "production";
const llmProvider = cfg.get("llmProvider") ?? "gemini";
const dbName = cfg.get("dbName") ?? "hackaton_db";
const dbUserName = cfg.get("dbUser") ?? "app_user";
const dbPassword = cfg.requireSecret("dbPassword");
const dbTier = cfg.get("dbTier") ?? "db-f1-micro";
const dbDiskSize = cfg.getNumber("dbDiskSize") ?? 20;

const secretKey = cfg.requireSecret("secretKey");
const jwtSecretKey = cfg.requireSecret("jwtSecretKey");
const adminUsername = cfg.get("adminUsername") ?? "admin";
const adminPassword = cfg.getSecret("adminPassword") ?? pulumi.secret("admin");

const geminiApiKey = cfg.getSecret("geminiApiKey") ?? pulumi.secret("");
const anthropicApiKey = cfg.getSecret("anthropicApiKey") ?? pulumi.secret("");
const googleClientId = cfg.getSecret("googleClientId") ?? pulumi.secret("");
const googleClientSecret = cfg.getSecret("googleClientSecret") ?? pulumi.secret("");
const googleProjectId = cfg.get("googleProjectId") ?? project;
const googleOauthRedirectUri = cfg.get("googleOauthRedirectUri") ?? "";
const gmailScopes =
    cfg.get("gmailScopes") ??
    "https://www.googleapis.com/auth/gmail.readonly openid email profile";
const gmailHistoryStartDays = cfg.getNumber("gmailHistoryStartDays") ?? 90;
const gmailSyncIntervalMinutes = cfg.getNumber("gmailSyncIntervalMinutes") ?? 15;
const gmailLlmConfidenceAuto = cfg.getNumber("gmailLlmConfidenceAuto") ?? 0.8;
const gmailLlmConfidenceReview = cfg.getNumber("gmailLlmConfidenceReview") ?? 0.5;
const enableGmailFeatures = cfg.getBoolean("enableGmailFeatures") ?? true;
const oauthEncryptionKey = cfg.getSecret("oauthEncryptionKey") ?? pulumi.secret("");
const gmailPubsubTopic = cfg.get("gmailPubsubTopic") ?? "";
const gmailPubsubSubscription = cfg.get("gmailPubsubSubscription") ?? "";

const frontendDomain = cfg.get("frontendDomain");
const backendMaxInstances = cfg.getNumber("backendMaxInstances") ?? 3;
const backendMinInstances = cfg.getNumber("backendMinInstances") ?? 0;
const frontendMaxInstances = cfg.getNumber("frontendMaxInstances") ?? 3;
const frontendMinInstances = cfg.getNumber("frontendMinInstances") ?? 0;

const network = new gcp.compute.Network(`${prefix}-net`, {
    autoCreateSubnetworks: false,
    description: "Isolated network for application services",
});

const subnetwork = new gcp.compute.Subnetwork(`${prefix}-subnet`, {
    region: location,
    ipCidrRange: "10.10.0.0/24",
    network: network.id,
    stackType: "IPV4_ONLY",
});

const vpcConnector = new gcp.vpcaccess.Connector(`${prefix}-connector`, {
    name: `${prefix}-connector`,
    region: location,
    network: network.id,
    ipCidrRange: "10.8.0.0/28",
});

const artifactRepo = new gcp.artifactregistry.Repository(`${prefix}-repo`, {
    location,
    format: "DOCKER",
    repositoryId: `${prefix}-containers`,
    description: "Container images for backend and frontend",
});

const registryBase = pulumi.interpolate`${location}-docker.pkg.dev/${project}/${artifactRepo.repositoryId}`;

const backendImage = new docker.Image(`${prefix}-backend-image`, {
    imageName: pulumi.interpolate`${registryBase}/backend:${stack}`,
    build: {
        context: "../../backend",
        platform: "linux/amd64",
    },
});

const dbInstance = new gcp.sql.DatabaseInstance(`${prefix}-db`, {
    region: location,
    databaseVersion: "POSTGRES_16",
    deletionProtection: true,
    settings: {
        tier: dbTier,
        diskSize: dbDiskSize,
        diskType: "PD_SSD",
        availabilityType: "ZONAL",
        ipConfiguration: {
            ipv4Enabled: true,
        },
        locationPreference: {
            zone: `${location}-a`,
        },
        maintenanceWindow: {
            day: 7,
            hour: 2,
        },
        backupConfiguration: {
            enabled: true,
        },
    },
});

const database = new gcp.sql.Database(`${prefix}-db-name`, {
    instance: dbInstance.name,
    name: dbName,
});

const dbUser = new gcp.sql.User(`${prefix}-db-user`, {
    instance: dbInstance.name,
    name: dbUserName,
    password: dbPassword,
});

const appServiceAccount = new gcp.serviceaccount.Account(`${prefix}-app-sa`, {
    accountId: `${prefix}-app-sa`,
    displayName: "Service account for Cloud Run services",
});

const saMember = appServiceAccount.email.apply(
    (email) => `serviceAccount:${email}`,
);

new gcp.projects.IAMMember(`${prefix}-sa-logs`, {
    project,
    role: "roles/logging.logWriter",
    member: saMember,
});

new gcp.projects.IAMMember(`${prefix}-sa-metrics`, {
    project,
    role: "roles/monitoring.metricWriter",
    member: saMember,
});

new gcp.projects.IAMMember(`${prefix}-sa-cloudsql`, {
    project,
    role: "roles/cloudsql.client",
    member: saMember,
});

new gcp.projects.IAMMember(`${prefix}-sa-artifact`, {
    project,
    role: "roles/artifactregistry.reader",
    member: saMember,
});

const databaseUrl = pulumi.interpolate`postgresql://${dbUser.name}:${dbPassword}@${dbInstance.firstIpAddress}:5432/${database.name}`;

const backendEnvs: gcp.types.input.cloudrunv2.ServiceTemplateContainerEnv[] = [
    { name: "ENVIRONMENT", value: environment },
    { name: "DATABASE_URL", value: databaseUrl },
    { name: "SECRET_KEY", value: secretKey },
    { name: "JWT_SECRET_KEY", value: jwtSecretKey },
    { name: "ADMIN_USERNAME", value: adminUsername },
    { name: "ADMIN_PASSWORD", value: adminPassword },
    { name: "LLM_PROVIDER", value: llmProvider },
    { name: "GEMINI_API_KEY", value: geminiApiKey },
    { name: "ANTHROPIC_API_KEY", value: anthropicApiKey },
    { name: "GOOGLE_PROJECT_ID", value: googleProjectId },
    { name: "GOOGLE_CLIENT_ID", value: googleClientId },
    { name: "GOOGLE_CLIENT_SECRET", value: googleClientSecret },
    { name: "GOOGLE_OAUTH_REDIRECT_URI", value: googleOauthRedirectUri },
    { name: "GMAIL_SCOPES", value: gmailScopes },
    { name: "GMAIL_HISTORY_START_DAYS", value: gmailHistoryStartDays.toString() },
    { name: "GMAIL_SYNC_INTERVAL_MINUTES", value: gmailSyncIntervalMinutes.toString() },
    { name: "GMAIL_LLM_CONFIDENCE_AUTO", value: gmailLlmConfidenceAuto.toString() },
    { name: "GMAIL_LLM_CONFIDENCE_REVIEW", value: gmailLlmConfidenceReview.toString() },
    { name: "OAUTH_ENCRYPTION_KEY", value: oauthEncryptionKey },
    { name: "GMAIL_PUBSUB_TOPIC", value: gmailPubsubTopic },
    { name: "GMAIL_PUBSUB_SUBSCRIPTION", value: gmailPubsubSubscription },
    { name: "ENABLE_GMAIL_FEATURES", value: `${enableGmailFeatures}` },
];

const backendService = new gcp.cloudrunv2.Service(`${prefix}-backend`, {
    location,
    name: `${prefix}-backend`,
    ingress: "INGRESS_TRAFFIC_ALL",
    template: {
        serviceAccount: appServiceAccount.email,
        scaling: {
            maxInstanceCount: backendMaxInstances,
            minInstanceCount: backendMinInstances,
        },
        containers: [
            {
                image: backendImage.imageName,
                ports: [{ containerPort: 8000 }],
                envs: backendEnvs,
                resources: {
                    limits: {
                        cpu: "1",
                        memory: "1Gi",
                    },
                },
                volumeMounts: [
                    {
                        name: "cloudsql",
                        mountPath: "/cloudsql",
                    },
                ],
            },
        ],
        volumes: [
            {
                name: "cloudsql",
                cloudSqlInstance: {
                    instances: [dbInstance.connectionName],
                },
            },
        ],
        vpcAccess: {
            connector: vpcConnector.id,
            egress: "ALL_TRAFFIC",
        },
    },
    traffics: [
        {
            percent: 100,
            type: "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST",
        },
    ],
});

new gcp.cloudrunv2.ServiceIamMember(`${prefix}-backend-invoke`, {
    name: backendService.name,
    location,
    role: "roles/run.invoker",
    member: "allUsers",
});

const frontendImage = new docker.Image(`${prefix}-frontend-image`, {
    imageName: pulumi.interpolate`${registryBase}/frontend:${stack}`,
    build: {
        context: "../../frontend",
        platform: "linux/amd64",
        args: {
            VITE_API_URL: backendService.uri,
        },
    },
});

const frontendService = new gcp.cloudrunv2.Service(`${prefix}-frontend`, {
    location,
    name: `${prefix}-frontend`,
    ingress: "INGRESS_TRAFFIC_ALL",
    template: {
        serviceAccount: appServiceAccount.email,
        scaling: {
            maxInstanceCount: frontendMaxInstances,
            minInstanceCount: frontendMinInstances,
        },
        containers: [
            {
                image: frontendImage.imageName,
                ports: [{ containerPort: 80 }],
                envs: frontendDomain
                    ? [{ name: "FRONTEND_DOMAIN", value: frontendDomain }]
                    : [],
                resources: {
                    limits: {
                        cpu: "1",
                        memory: "512Mi",
                    },
                },
            },
        ],
    },
    traffics: [
        {
            percent: 100,
            type: "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST",
        },
    ],
});

new gcp.cloudrunv2.ServiceIamMember(`${prefix}-frontend-invoke`, {
    name: frontendService.name,
    location,
    role: "roles/run.invoker",
    member: "allUsers",
});

export const backendUrl = backendService.uri;
export const frontendUrl = frontendService.uri;
export const artifactRegistry = artifactRepo.repositoryId;
export const cloudSqlInstanceConnectionName = dbInstance.connectionName;
