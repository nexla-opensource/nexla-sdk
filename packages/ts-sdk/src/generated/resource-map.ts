/**
 * Auto-generated resource map from OpenAPI.
 * Do not edit manually.
 */

export const resourceMap = {
  "api_keys": {},
  "approval_requests": {},
  "async_tasks": {
    "list": {
      "path": "/async_tasks",
      "method": "get"
    },
    "create": {
      "path": "/async_tasks",
      "method": "post"
    },
    "get": {
      "path": "/async_tasks/{task_id}",
      "method": "get"
    },
    "delete": {
      "path": "/async_tasks/{task_id}",
      "method": "delete"
    }
  },
  "attribute_transforms": {
    "list": {
      "path": "/attribute_transforms",
      "method": "get"
    },
    "create": {
      "path": "/attribute_transforms",
      "method": "post"
    },
    "get": {
      "path": "/attribute_transforms/{attribute_transform_id}",
      "method": "get"
    },
    "update": {
      "path": "/attribute_transforms/{attribute_transform_id}",
      "method": "put"
    },
    "delete": {
      "path": "/attribute_transforms/{attribute_transform_id}",
      "method": "delete"
    }
  },
  "auth_parameters": {},
  "auth_templates": {},
  "catalog_configs": {},
  "cluster_endpoints": {},
  "clusters": {},
  "code_containers": {
    "list": {
      "path": "/code_containers",
      "method": "get"
    },
    "create": {
      "path": "/code_containers",
      "method": "post"
    },
    "get": {
      "path": "/code_containers/{code_container_id}",
      "method": "get"
    },
    "update": {
      "path": "/code_containers/{code_container_id}",
      "method": "put"
    },
    "delete": {
      "path": "/code_containers/{code_container_id}",
      "method": "delete"
    }
  },
  "connectors": {},
  "credentials": {
    "list": {
      "path": "/data_credentials",
      "method": "get"
    },
    "create": {
      "path": "/data_credentials",
      "method": "post"
    },
    "get": {
      "path": "/data_credentials/{credential_id}",
      "method": "get"
    },
    "update": {
      "path": "/data_credentials/{credential_id}",
      "method": "put"
    },
    "delete": {
      "path": "/data_credentials/{credential_id}",
      "method": "delete"
    }
  },
  "cubejs": {},
  "custom_data_flows": {},
  "dashboard_transforms": {},
  "data_credentials_groups": {},
  "data_flows": {},
  "data_schemas": {},
  "destinations": {
    "list": {
      "path": "/data_sinks",
      "method": "get"
    },
    "create": {
      "path": "/data_sinks",
      "method": "post"
    },
    "get": {
      "path": "/data_sinks/{sink_id}",
      "method": "get"
    },
    "update": {
      "path": "/data_sinks/{sink_id}",
      "method": "put"
    },
    "delete": {
      "path": "/data_sinks/{sink_id}",
      "method": "delete"
    }
  },
  "doc_containers": {},
  "flow_nodes": {},
  "flow_triggers": {},
  "flows": {
    "list": {
      "path": "/flows",
      "method": "get"
    },
    "get": {
      "path": "/flows/{flow_id}",
      "method": "get"
    },
    "delete": {
      "path": "/flows/{flow_id}",
      "method": "delete"
    }
  },
  "lookups": {
    "list": {
      "path": "/data_maps",
      "method": "get"
    },
    "create": {
      "path": "/data_maps",
      "method": "post"
    },
    "get": {
      "path": "/data_maps/{data_map_id}",
      "method": "get"
    },
    "update": {
      "path": "/data_maps/{data_map_id}",
      "method": "put"
    },
    "delete": {
      "path": "/data_maps/{data_map_id}",
      "method": "delete"
    }
  },
  "marketplace": {},
  "mcp_sessions": {},
  "nexsets": {
    "list": {
      "path": "/data_sets",
      "method": "get"
    },
    "create": {
      "path": "/data_sets",
      "method": "post"
    },
    "get": {
      "path": "/data_sets/{set_id}",
      "method": "get"
    },
    "update": {
      "path": "/data_sets/{set_id}",
      "method": "put"
    },
    "delete": {
      "path": "/data_sets/{set_id}",
      "method": "delete"
    }
  },
  "notification_channel_settings": {
    "list": {
      "path": "/notification_channel_settings",
      "method": "get"
    },
    "create": {
      "path": "/notification_channel_settings",
      "method": "post"
    },
    "get": {
      "path": "/notification_channel_settings/{notification_channel_setting_id}",
      "method": "get"
    },
    "update": {
      "path": "/notification_channel_settings/{notification_channel_setting_id}",
      "method": "put"
    },
    "delete": {
      "path": "/notification_channel_settings/{notification_channel_setting_id}",
      "method": "delete"
    }
  },
  "notification_settings": {
    "list": {
      "path": "/notification_settings",
      "method": "get"
    },
    "create": {
      "path": "/notification_settings",
      "method": "post"
    },
    "get": {
      "path": "/notification_settings/{notification_setting_id}",
      "method": "get"
    },
    "update": {
      "path": "/notification_settings/{notification_setting_id}",
      "method": "put"
    },
    "delete": {
      "path": "/notification_settings/{notification_setting_id}",
      "method": "delete"
    }
  },
  "notification_types": {
    "list": {
      "path": "/notification_types",
      "method": "get"
    }
  },
  "notifications": {
    "list": {
      "path": "/notifications",
      "method": "get"
    },
    "get": {
      "path": "/notifications/{notification_id}",
      "method": "get"
    },
    "delete": {
      "path": "/notifications/{notification_id}",
      "method": "delete"
    }
  },
  "org_auth_configs": {
    "list": {
      "path": "/api_auth_configs",
      "method": "get"
    },
    "create": {
      "path": "/api_auth_configs",
      "method": "post"
    },
    "get": {
      "path": "/api_auth_configs/{auth_config_id}",
      "method": "get"
    },
    "update": {
      "path": "/api_auth_configs/{auth_config_id}",
      "method": "put"
    },
    "delete": {
      "path": "/api_auth_configs/{auth_config_id}",
      "method": "delete"
    }
  },
  "org_tiers": {},
  "organizations": {
    "list": {
      "path": "/orgs",
      "method": "get"
    },
    "get": {
      "path": "/orgs/{org_id}",
      "method": "get"
    },
    "update": {
      "path": "/orgs/{org_id}",
      "method": "put"
    }
  },
  "projects": {
    "list": {
      "path": "/projects",
      "method": "get"
    },
    "create": {
      "path": "/projects",
      "method": "post"
    },
    "get": {
      "path": "/projects/{project_id}",
      "method": "get"
    },
    "update": {
      "path": "/projects/{project_id}",
      "method": "put"
    },
    "delete": {
      "path": "/projects/{project_id}",
      "method": "delete"
    }
  },
  "quarantine_settings": {},
  "resource_parameters": {},
  "runtimes": {
    "list": {
      "path": "/runtimes",
      "method": "get"
    },
    "create": {
      "path": "/runtimes",
      "method": "post"
    },
    "get": {
      "path": "/runtimes/{runtime_id}",
      "method": "get"
    },
    "update": {
      "path": "/runtimes/{runtime_id}",
      "method": "put"
    },
    "delete": {
      "path": "/runtimes/{runtime_id}",
      "method": "delete"
    }
  },
  "search_health": {},
  "self_signup_blocked_domains": {
    "list": {
      "path": "/self_signup_blocked_domains",
      "method": "get"
    },
    "create": {
      "path": "/self_signup_blocked_domains",
      "method": "post"
    },
    "update": {
      "path": "/self_signup_blocked_domains/{domain_id}",
      "method": "put"
    },
    "delete": {
      "path": "/self_signup_blocked_domains/{domain_id}",
      "method": "delete"
    }
  },
  "service_keys": {},
  "sources": {
    "list": {
      "path": "/data_sources",
      "method": "get"
    },
    "create": {
      "path": "/data_sources",
      "method": "post"
    },
    "get": {
      "path": "/data_sources/{source_id}",
      "method": "get"
    },
    "update": {
      "path": "/data_sources/{source_id}",
      "method": "put"
    },
    "delete": {
      "path": "/data_sources/{source_id}",
      "method": "delete"
    }
  },
  "teams": {
    "list": {
      "path": "/teams",
      "method": "get"
    },
    "create": {
      "path": "/teams",
      "method": "post"
    },
    "get": {
      "path": "/teams/{team_id}",
      "method": "get"
    },
    "update": {
      "path": "/teams/{team_id}",
      "method": "put"
    },
    "delete": {
      "path": "/teams/{team_id}",
      "method": "delete"
    }
  },
  "tool_sets": {},
  "tools": {},
  "transforms": {
    "list": {
      "path": "/transforms",
      "method": "get"
    },
    "create": {
      "path": "/transforms",
      "method": "post"
    },
    "get": {
      "path": "/transforms/{transform_id}",
      "method": "get"
    },
    "update": {
      "path": "/transforms/{transform_id}",
      "method": "put"
    },
    "delete": {
      "path": "/transforms/{transform_id}",
      "method": "delete"
    }
  },
  "user_settings": {
    "list": {
      "path": "/user_settings",
      "method": "get"
    }
  },
  "user_tiers": {},
  "users": {
    "list": {
      "path": "/users",
      "method": "get"
    },
    "create": {
      "path": "/users",
      "method": "post"
    },
    "get": {
      "path": "/users/{user_id}",
      "method": "get"
    },
    "update": {
      "path": "/users/{user_id}",
      "method": "put"
    }
  },
  "validators": {},
  "vendor_endpoints": {},
  "vendors": {}
} as const;

export type ResourceMap = typeof resourceMap;
