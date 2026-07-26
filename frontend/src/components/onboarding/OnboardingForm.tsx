"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import { createFarmerProfile } from "@/services/farmer.service";

export default function OnboardingForm() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const [fullName, setFullName] = useState("");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState<"Male" | "Female" | "Other" | "">("");
  const [state, setState] = useState("");
  const [district, setDistrict] = useState("");
  const [village, setVillage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!fullName || !age || !gender || !state || !district || !village) {
      toast.warning("Please fill in all fields.");
      return;
    }

    try {
      setLoading(true);

      await createFarmerProfile({
        full_name: fullName,
        age: Number(age),
        gender,
        state,
        district,
        village,
      });

      toast.success("Profile created successfully.");
      router.push("/dashboard");
    } catch (error: any) {
      console.error("Profile creation error:", error);
      toast.error(
        error?.response?.data?.detail ??
          "Unable to save your profile. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-2">
        <Label>Full Name</Label>
        <Input
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          placeholder="Vishal Singh"
        />
      </div>

      <div className="grid gap-6 sm:grid-cols-2">
        <div className="space-y-2">
          <Label>Age</Label>
          <Input
            type="number"
            value={age}
            onChange={(e) => setAge(e.target.value)}
            placeholder="35"
            min={8}
            max={120}
          />
        </div>

        <div className="space-y-2">
          <Label>Gender</Label>
          <Select value={gender} onValueChange={(v) => setGender(v as any)}>
            <SelectTrigger className="w-full">
              <SelectValue placeholder="Select gender" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="Male">Male</SelectItem>
              <SelectItem value="Female">Female</SelectItem>
              <SelectItem value="Other">Other</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="space-y-2">
        <Label>State</Label>
        <Input
          value={state}
          onChange={(e) => setState(e.target.value)}
          placeholder="Bihar"
        />
      </div>

      <div className="grid gap-6 sm:grid-cols-2">
        <div className="space-y-2">
          <Label>District</Label>
          <Input
            value={district}
            onChange={(e) => setDistrict(e.target.value)}
            placeholder="Patna"
          />
        </div>

        <div className="space-y-2">
          <Label>Village</Label>
          <Input
            value={village}
            onChange={(e) => setVillage(e.target.value)}
            placeholder="Barauni"
          />
        </div>
      </div>

      <Button type="submit" disabled={loading} className="w-full rounded-xl py-6">
        {loading ? "Saving..." : "Complete Setup"}
      </Button>
    </form>
  );
}
