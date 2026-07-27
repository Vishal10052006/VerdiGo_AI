export interface CurrentWeather {
  temperature: number;
  humidity: number;
  wind_speed: number;
  condition: string;
  rainfall: number;
  provider: string;
  fetched_at: string;
}

export interface ForecastDay {
  date: string;
  min_temperature: number;
  max_temperature: number;
  rainfall: number;
  humidity: number;
  wind_speed: number;
  condition: string;
}

export interface WeatherForecast {
  provider: string;
  generated_at: string;
  forecast: ForecastDay[];
}

export interface Advisory {
  type: string;
  severity: "low" | "moderate" | "high" | "critical";
  title: string;
  message: string;
}

export interface WeatherAdvisory {
  generated_at: string;
  advisories: Advisory[];
}