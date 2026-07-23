import { CheckCircle2, AlertTriangle, ShieldAlert } from "lucide-react";
import type { DiseaseDetection } from "@/types/disease";

const SEVERITY_STYLES: Record<string, string> = {
  none: "bg-emerald-100 text-emerald-700",
  low: "bg-yellow-100 text-yellow-700",
  moderate: "bg-orange-100 text-orange-700",
  high: "bg-red-100 text-red-700",
  critical: "bg-red-200 text-red-900",
};

export default function DiseaseResultCard({ result }: { result: DiseaseDetection }) {
  return (
    <div className="rounded-3xl border bg-white p-8 shadow-sm">
      <div className="mb-6 flex items-center justify-between">
        <div className="flex items-center gap-3">
          {result.is_healthy ? (
            <CheckCircle2 className="h-8 w-8 text-emerald-600" />
          ) : (
            <AlertTriangle className="h-8 w-8 text-red-600" />
          )}
          <div>
            <h3 className="text-2xl font-bold text-slate-900">
              {result.is_healthy ? "Healthy Plant" : result.disease_name}
            </h3>
            {result.crop_type && (
              <p className="text-sm text-slate-500">{result.crop_type}</p>
            )}
          </div>
        </div>

        <span
          className={`rounded-full px-4 py-1.5 text-sm font-semibold ${SEVERITY_STYLES[result.severity]}`}
        >
          {result.severity.toUpperCase()} · {Math.round(result.confidence)}% confidence
        </span>
      </div>

      {result.treatment.length > 0 && (
        <div className="mb-6">
          <h4 className="mb-2 flex items-center gap-2 font-semibold text-slate-900">
            <ShieldAlert className="h-4 w-4 text-red-500" /> Treatment
          </h4>
          <ul className="space-y-1.5 text-sm text-slate-600">
            {result.treatment.map((step, i) => (
              <li key={i}>• {step}</li>
            ))}
          </ul>
        </div>
      )}

      {result.prevention_tips.length > 0 && (
        <div>
          <h4 className="mb-2 font-semibold text-slate-900">Prevention Tips</h4>
          <ul className="space-y-1.5 text-sm text-slate-600">
            {result.prevention_tips.map((tip, i) => (
              <li key={i}>• {tip}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}