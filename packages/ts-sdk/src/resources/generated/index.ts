import type { NexlaClient } from "../../client/nexla-client.js";
import { AccessControlResource } from "./access_control.js";
import { ApprovalRequestsResource } from "./approval_requests.js";
import { AsyncTasksResource } from "./async_tasks.js";
import { AuditLogsResource } from "./audit_logs.js";
import { CodeContainersResource } from "./code_containers.js";
import { CredentialsResource } from "./credentials.js";
import { DestinationsResource } from "./destinations.js";
import { FlowsResource } from "./flows.js";
import { GenaiResource } from "./genai.js";
import { LimitsResource } from "./limits.js";
import { LookupsResource } from "./lookups.js";
import { MarketplaceResource } from "./marketplace.js";
import { MetricsResource } from "./metrics.js";
import { NexsetsResource } from "./nexsets.js";
import { NotificationsResource } from "./notifications.js";
import { OrgAuthConfigsResource } from "./org_auth_configs.js";
import { OrganizationsResource } from "./organizations.js";
import { ProjectsResource } from "./projects.js";
import { QuarantineSettingsResource } from "./quarantine_settings.js";
import { RuntimesResource } from "./runtimes.js";
import { SelfSignupResource } from "./self_signup.js";
import { SelfSignupAdminResource } from "./self_signup_admin.js";
import { SourcesResource } from "./sources.js";
import { TeamsResource } from "./teams.js";
import { TokensResource } from "./tokens.js";
import { TransformsResource } from "./transforms.js";
import { UserSettingsResource } from "./user_settings.js";
import { UsersResource } from "./users.js";

export { AccessControlResource };
export { ApprovalRequestsResource };
export { AsyncTasksResource };
export { AuditLogsResource };
export { CodeContainersResource };
export { CredentialsResource };
export { DestinationsResource };
export { FlowsResource };
export { GenaiResource };
export { LimitsResource };
export { LookupsResource };
export { MarketplaceResource };
export { MetricsResource };
export { NexsetsResource };
export { NotificationsResource };
export { OrgAuthConfigsResource };
export { OrganizationsResource };
export { ProjectsResource };
export { QuarantineSettingsResource };
export { RuntimesResource };
export { SelfSignupResource };
export { SelfSignupAdminResource };
export { SourcesResource };
export { TeamsResource };
export { TokensResource };
export { TransformsResource };
export { UserSettingsResource };
export { UsersResource };

export interface GeneratedResourceClients {
  access_control: AccessControlResource;
  approval_requests: ApprovalRequestsResource;
  async_tasks: AsyncTasksResource;
  audit_logs: AuditLogsResource;
  code_containers: CodeContainersResource;
  credentials: CredentialsResource;
  destinations: DestinationsResource;
  flows: FlowsResource;
  genai: GenaiResource;
  limits: LimitsResource;
  lookups: LookupsResource;
  marketplace: MarketplaceResource;
  metrics: MetricsResource;
  nexsets: NexsetsResource;
  notifications: NotificationsResource;
  org_auth_configs: OrgAuthConfigsResource;
  organizations: OrganizationsResource;
  projects: ProjectsResource;
  quarantine_settings: QuarantineSettingsResource;
  runtimes: RuntimesResource;
  self_signup: SelfSignupResource;
  self_signup_admin: SelfSignupAdminResource;
  sources: SourcesResource;
  teams: TeamsResource;
  tokens: TokensResource;
  transforms: TransformsResource;
  user_settings: UserSettingsResource;
  users: UsersResource;
}

export const createGeneratedResources = (client: NexlaClient): GeneratedResourceClients => ({
    access_control: new AccessControlResource(client),
    approval_requests: new ApprovalRequestsResource(client),
    async_tasks: new AsyncTasksResource(client),
    audit_logs: new AuditLogsResource(client),
    code_containers: new CodeContainersResource(client),
    credentials: new CredentialsResource(client),
    destinations: new DestinationsResource(client),
    flows: new FlowsResource(client),
    genai: new GenaiResource(client),
    limits: new LimitsResource(client),
    lookups: new LookupsResource(client),
    marketplace: new MarketplaceResource(client),
    metrics: new MetricsResource(client),
    nexsets: new NexsetsResource(client),
    notifications: new NotificationsResource(client),
    org_auth_configs: new OrgAuthConfigsResource(client),
    organizations: new OrganizationsResource(client),
    projects: new ProjectsResource(client),
    quarantine_settings: new QuarantineSettingsResource(client),
    runtimes: new RuntimesResource(client),
    self_signup: new SelfSignupResource(client),
    self_signup_admin: new SelfSignupAdminResource(client),
    sources: new SourcesResource(client),
    teams: new TeamsResource(client),
    tokens: new TokensResource(client),
    transforms: new TransformsResource(client),
    user_settings: new UserSettingsResource(client),
    users: new UsersResource(client),
});