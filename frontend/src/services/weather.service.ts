import api from "@/lib/api";
import type { CurrentWeather, WeatherForecast, WeatherAdvisory } from "@/types/weather";

export const getCurrentWeather = async (farmId: string): Promise<CurrentWeather> => {
  const response = await api.get(`/v1/weather/current/${farmId}`);
  return response.data.data;
};

export const getWeatherForecast = async (
  farmId: string,
  days = 5
): Promise<WeatherForecast> => {
  const response = await api.get(`/v1/weather/forecast/${farmId}`, {
    params: { days },
  });
  return response.data.data;
};

export const getWeatherAdvisories = async (farmId: string): Promise<WeatherAdvisory> => {
  const response = await api.get(`/v1/weather/advisory/${farmId}`);
  return response.data.data;
};