import { describe, expect, it } from "vitest";
import { NexlaError, RateLimitError } from "../src/errors.js";

describe("NexlaError", () => {
  it("captures summary metadata", () => {
    const err = new NexlaError("boom", { statusCode: 400, response: { message: "bad" } });
    const summary = err.getErrorSummary();

    expect(summary.message).toBe("boom");
    expect(summary.status_code).toBe(400);
  });

  it("includes retryAfter for rate limit errors", () => {
    const err = new RateLimitError("slow down", { retryAfter: 30 });
    expect(err.retryAfter).toBe(30);
  });
});
