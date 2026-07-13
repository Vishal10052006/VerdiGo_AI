import { ENV } from "@/config/env";

export default function Home() {
  return (
    <main className="flex min-h-screen items-center justify-center">
      <div className="space-y-3 text-center">
        <h1 className="text-3xl font-bold">{ENV.APP_NAME}</h1>

        <p>{ENV.API_BASE_URL}</p>

        <p>{ENV.ENVIRONMENT}</p>
      </div>
    </main>
  );
}
