"use client";

import { useEffect, useState } from "react";
import ProtectedRoute from "@/components/auth/ProtectedRoute";
import { PageHeader } from "@/components/common/PageHeader";
import DiseaseUpload from "@/components/disease/DiseaseUpload";
import DiseaseResultCard from "@/components/disease/DiseaseResultCard";
import { ErrorState } from "@/components/common/ErrorState";
import { EmptyState } from "@/components/common/EmptyState";
import { useDiseaseDetection } from "@/hooks/useDiseaseDetection";
import { getFarm } from "@/services/farm.service";
import { Bug } from "lucide-react";

export default function DiseaseDetectionPage() {
  const [farmId, setFarmId] = useState<string | null>(null);
  const { result, analyzing, error, analyze } = useDiseaseDetection();

  useEffect(() => {
    getFarm()
      .then((farm) => setFarmId(farm.id))
      .catch(() => setFarmId(null));
  }, []);

  return (
    <ProtectedRoute>
      <main className="min-h-screen bg-slate-50">
        <PageHeader
          title="Disease Detection"
          description="Upload a crop photo for instant AI diagnosis"
          icon={<Bug className="h-6 w-6" />}
        />

        <div className="mx-auto max-w-3xl space-y-6 px-4 py-6 sm:px-6 lg:px-8">
          {!farmId ? (
            <EmptyState
              title="No farm registered yet"
              description="Register a farm before using disease detection."
              icon={<Bug className="h-10 w-10" />}
            />
          ) : (
            <>
              <DiseaseUpload
                analyzing={analyzing}
                onSelect={(file) => analyze(farmId, file)}
              />

              {error && (
                <ErrorState title="Analysis failed" description={error} />
              )}

              {result && <DiseaseResultCard result={result} />}
            </>
          )}
        </div>
      </main>
    </ProtectedRoute>
  );
}