// frontend/src/services/admin.service.ts
import adminApi from "@/lib/adminApi";

export const adminLogin = async (email: string, password: string) => {
  const response = await adminApi.post("/admin/auth/login", { email, password });
  return response.data;
};

export const getFarmers = async (params: {
  page?: number;
  page_size?: number;
  search?: string;
  state?: string;
  is_active?: boolean;
}) => {
  const response = await adminApi.get("/admin/farmers", { params });
  return response.data.data;
};

export const getFarmerDetail = async (userId: string) => {
  const response = await adminApi.get(`/admin/farmers/${userId}`);
  return response.data.data;
};

export const updateFarmerStatus = async (userId: string, isActive: boolean) => {
  const response = await adminApi.patch(`/admin/farmers/${userId}/status`, {
    is_active: isActive,
  });
  return response.data.data;
};

export const getAnalyticsOverview = async () => {
  const response = await adminApi.get("/admin/analytics/overview");
  return response.data.data;
};

export const getGrowthAnalytics = async (days = 30) => {
  const response = await adminApi.get("/admin/analytics/growth", { params: { days } });
  return response.data.data;
};