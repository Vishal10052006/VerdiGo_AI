/**
 * ============================================================================
 * Farm Page (Add / Edit)
 * ============================================================================
 *
 * Route: /farm
 *
 * Single unified page for farm management — backend enforces exactly
 * one farm per farmer, so this page detects whether a farm already
 * exists and switches between "Create" and "Edit" modes automatically,
 * rather than having separate /farm/add and /farms routes that don't
 * match the actual single-farm data model.
 *
 * Module:
 * Phase 1 → Module 2 → Farmer Registration
 * ============================================================================
 */

"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { MapPin, Loader2, Tractor } from "lucide-react";

import ProtectedRoute from "@/components/auth/ProtectedRoute";
import AuthenticatedLayout from "@/layouts/AuthenticatedLayout";
import { PageHeader } from "@/components/common/PageHeader";
import { LoadingSkeleton } from "@/components/common/LoadingSkeleton";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import { getFarm, createFarm, updateFarm, FarmPayload } from "@/services/farm.service";

const SOIL_TYPES = [
  "Clay", "Sandy", "Loamy", "Silty", "Black",
  "Red", "Laterite", "Alluvial", "Mountain", "Unknown",
];

const LAND_UNITS = ["Acre", "Hectare", "Bigha"] as const;

const EMPTY_FORM: FarmPayload = {
  farm_name: "",
  land_area: 0,
  land_unit: "Acre",
  soil_type: "",
  latitude: 0,
  longitude: 0,
};

export default function FarmPage() {
  const router = useRouter();

  const [mode, setMode] = useState<"loading" | "create" | "edit">("loading");
  const [form, setForm] = useState<FarmPayload>(EMPTY_FORM);
  const [saving, setSaving] = useState(false);
  const [locating, setLocating] = useState(false);

  // --------------------------------------------------------------
  // Load existing farm, if any
  // --------------------------------------------------------------
  useEffect(() => {
    let cancelled = false;

    const load = async () => {
      try {
        const farm = await getFarm();

        if (!cancelled) {
          setForm({
            farm_name: farm.farm_name,
            land_area: Number(farm.land_area),
            land_unit: farm.land_unit ?? "Acre",
            soil_type: farm.soil_type,
            latitude: farm.latitude,
            longitude: farm.longitude,
          });
          setMode("edit");
        }
      } catch (err: any) {
        // 404 = no farm registered yet -> Create mode.
        // Any other error, we still default to Create rather than
        // trapping the farmer on a dead error screen.
        if (!cancelled) {
          setMode("create");
        }
      }
    };

    load();

    return () => {
      cancelled = true;
    };
  }, []);

  // --------------------------------------------------------------
  // Use current GPS location
  // --------------------------------------------------------------
  const handleUseCurrentLocation = () => {
    if (!navigator.geolocation) {
      toast.error("Geolocation is not supported by your browser.");
      return;
    }

    setLocating(true);

    navigator.geolocation.getCurrentPosition(
      (position) => {
        setForm((prev) => ({
          ...prev,
          latitude: Number(position.coords.latitude.toFixed(6)),
          longitude: Number(position.coords.longitude.toFixed(6)),
        }));
        setLocating(false);
        toast.success("Location captured.");
      },
      () => {
        setLocating(false);
        toast.error("Unable to get your location. Enter it manually.");
      }
    );
  };

  // --------------------------------------------------------------
  // Submit
  // --------------------------------------------------------------
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!form.farm_name.trim()) {
      toast.warning("Farm name is required.");
      return;
    }

    if (!form.soil_type) {
      toast.warning("Select a soil type.");
      return;
    }

    if (form.land_area <= 0) {
      toast.warning("Land area must be greater than 0.");
      return;
    }

    if (form.latitude === 0 && form.longitude === 0) {
      toast.warning("Set your farm's location (use current location or enter manually).");
      return;
    }

    setSaving(true);

    try {
      if (mode === "create") {
        await createFarm(form);
        toast.success("Farm registered successfully.");
      } else {
        await updateFarm(form);
        toast.success("Farm updated successfully.");
      }

      router.push("/dashboard");
    } catch (err: any) {
      const detail = err?.response?.data?.detail ?? err?.response?.data?.message;
      toast.error(detail ?? "Unable to save farm. Please try again.");
    } finally {
      setSaving(false);
    }
  };

  if (mode === "loading") {
    return (
      <ProtectedRoute>
        <AuthenticatedLayout>
          <div className="mx-auto max-w-2xl px-4 py-10">
            <LoadingSkeleton variant="card" />
          </div>
        </AuthenticatedLayout>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <AuthenticatedLayout>
        <PageHeader
          title={mode === "create" ? "Register Your Farm" : "Edit Farm"}
          description={
            mode === "create"
              ? "Add your farm details to unlock weather, crop, and disease recommendations."
              : "Update your farm's details."
          }
          icon={<Tractor className="h-6 w-6" />}
        />

        <div className="mx-auto max-w-2xl px-4 py-8 sm:px-6 lg:px-8">
          <form
            onSubmit={handleSubmit}
            className="space-y-6 rounded-3xl border bg-white p-8 shadow-sm"
          >
            {/* Farm Name */}
            <div className="space-y-2">
              <Label>Farm Name</Label>
              <Input
                value={form.farm_name}
                onChange={(e) => setForm({ ...form, farm_name: e.target.value })}
                placeholder="e.g. North Field"
                maxLength={100}
              />
            </div>

            {/* Land Area + Unit */}
            <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                    <Label>Land Area</Label>
                    <Input
                    type="number"
                    step="0.01"
                    min="0"
                    value={form.land_area || ""}
                    onChange={(e) =>
                        setForm({ ...form, land_area: parseFloat(e.target.value) || 0 })
                    }
                    placeholder="5"
                    />
                </div>

                <div className="space-y-2">
                    <Label>Unit</Label>
                    <Select
                    value={form.land_unit}
                    onValueChange={(value) => {
                        // FIX: base-ui's Select.onValueChange is typed as
                        // (value: string | null) => void — it can emit null when
                        // cleared. FarmPayload.land_unit is a strict union with no
                        // null allowed, so TS correctly flagged the raw assignment.
                        // Guard against null and fall back to the current value
                        // rather than ever writing null into form state.
                        if (value) {
                        setForm({ ...form, land_unit: value as FarmPayload["land_unit"] });
                        }
                    }}
                    >
                        <SelectTrigger className="w-full">
                            <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                            {LAND_UNITS.map((unit) => (
                            <SelectItem key={unit} value={unit}>
                                {unit}
                            </SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                </div>
            </div>

            {/* Soil Type */}
            <div className="space-y-2">
                <Label>Soil Type</Label>
                <Select
                    value={form.soil_type}
                    onValueChange={(value) => {
                    // Same null-guard as land_unit above.
                    if (value) {
                        setForm({ ...form, soil_type: value });
                    }
                    }}
                >
                    <SelectTrigger className="w-full">
                        <SelectValue placeholder="Select soil type" />
                    </SelectTrigger>
                    <SelectContent>
                        {SOIL_TYPES.map((soil) => (
                            <SelectItem key={soil} value={soil}>
                            {soil}
                            </SelectItem>
                        ))}
                    </SelectContent>
                </Select>
            </div>

            {/* Location */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label>Farm Location</Label>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={handleUseCurrentLocation}
                  disabled={locating}
                >
                  {locating ? (
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  ) : (
                    <MapPin className="mr-2 h-4 w-4" />
                  )}
                  Use Current Location
                </Button>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1">
                  <Label className="text-xs text-slate-500">Latitude</Label>
                  <Input
                    type="number"
                    step="0.000001"
                    value={form.latitude || ""}
                    onChange={(e) =>
                      setForm({ ...form, latitude: parseFloat(e.target.value) || 0 })
                    }
                    placeholder="25.4358"
                  />
                </div>
                <div className="space-y-1">
                  <Label className="text-xs text-slate-500">Longitude</Label>
                  <Input
                    type="number"
                    step="0.000001"
                    value={form.longitude || ""}
                    onChange={(e) =>
                      setForm({ ...form, longitude: parseFloat(e.target.value) || 0 })
                    }
                    placeholder="86.1347"
                  />
                </div>
              </div>
            </div>

            <Button
              type="submit"
              disabled={saving}
              className="w-full rounded-xl py-6 text-base"
            >
              {saving
                ? "Saving..."
                : mode === "create"
                  ? "Register Farm"
                  : "Save Changes"}
            </Button>
          </form>
        </div>
      </AuthenticatedLayout>
    </ProtectedRoute>
  );
}