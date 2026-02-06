export interface AuthProvider {
  getAccessToken(): Promise<string>;
  refreshAccessToken(): Promise<void>;
  logout(): Promise<void>;
  readonly isRefreshable: boolean;
}
