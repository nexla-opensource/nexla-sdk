import type { FetchResponse, RequestOptions } from "openapi-fetch";
import type { MediaType } from "openapi-typescript-helpers";
import type { operations } from "../generated/schema.js";

export type OperationId = keyof operations;

export type OperationInit<OpId extends OperationId> = RequestOptions<operations[OpId]>;

export type OperationResponse<OpId extends OperationId> = FetchResponse<
  operations[OpId],
  OperationInit<OpId>,
  MediaType
>;

export type OperationData<OpId extends OperationId> = OperationResponse<OpId> extends {
  data: infer D;
}
  ? D
  : never;
