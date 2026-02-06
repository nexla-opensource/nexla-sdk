import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "node",
    coverage: {
      provider: "v8",
      reportsDirectory: "./coverage",
      reporter: ["text", "lcov"],
      thresholds: {
        lines: 80,
        functions: 80,
        statements: 80,
        branches: 70
      },
      exclude: [
        "dist/**",
        "coverage/**",
        "tests/**",
        "src/generated/**",
        "src/resources/generated/**",
        "scripts/**",
        "src/index.ts",
        "**/*.config.*",
        "src/auth/types.ts",
        "src/client/types.ts",
        "src/resources/index.ts"
      ]
    }
  }
});
