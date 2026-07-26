"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

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

import { createFarmerProfile } from "@/services/farmer.service";

const NAME_REGEX = /^[A-Za-z .'-]+$/;
const PLACE_REGEX = /^[A-Za-z .&'-]+$/;
const VILLAGE_REGEX = /^[A-Za-z0-9 .&'-]+$/;

export default function OnboardingForm() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const [fullName, setFullName] = useState("");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState<"Male" | "Female" | "Other" | "">("");
  const [state, setState] = useState("");
  const [district, setDistrict] = useState("");
  const [village, setVillage] = useState("");

  const validate = (): string | null => {
    if (fullName.trim().length < 3) return "Name must be at least 3 characters.";
    if (!NAME_REGEX.test(fullName.trim()))
      return "Name can contain only letters, spaces, dots, hyphens, apostrophes.";

    const ageNum = Number(age);
    if (!age || Number.isNaN(ageNum) || ageNum < 8 || ageNum > 120)
      return "Age must be between 8 and 120.";

    if (!gender) return "Please select a gender.";

    if (state.trim().length < 2 || !PLACE_REGEX.test(state.trim()))
      return "Enter a valid state.";

    if (district.trim().length < 2 || !PLACE_REGEX.test(district.trim()))
      return "Enter a valid district.";

    if (village.trim().length < 2 || !VILLAGE_REGEX.test(village.trim()))
      return "Enter a valid village.";

    return null;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const validationError = validate();
    if (validationError) {
      toast.warning(validationError);
      return;
    }

    setLoading(true);

    try {
      await createFarmerProfile({
        full_name: fullName.trim(),
        age: Number(age),
        gender: gender as "Male" | "Female" | "Other",
        state: state.trim(),
        district: district.trim(),
        village: village.trim(),
      });

      toast.success("Profile created successfully.");
      router.push("/dashboard");
    } catch (error) {
      console.error("Profile creation error:", error);
      toast.error("Unable to save your profile. Please try again.");
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
          placeholder="e.g. Ramesh Kumar"
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label>Age</Label>
          <Input
            type="number"
            value={age}
            onChange={(e) => setAge(e.target.value)}
            placeholder="35"
          />
        </div>

        <div className="space-y-2">
          <Label>Gender</Label>
          <Select
            value={gender}
            onValueChange={(value) =>
              setGender(value as "Male" | "Female" | "Other")
            }
          >
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
          placeholder="e.g. Bihar"
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label>District</Label>
          <Input
            value={district}
            onChange={(e) => setDistrict(e.target.value)}
            placeholder="e.g. Patna"
          />
        </div>

        <div className="space-y-2">
          <Label>Village</Label>
          <Input
            value={village}
            onChange={(e) => setVillage(e.target.value)}
            placeholder="e.g. Barauni"
          />
        </div>
      </div>

      <Button type="submit" disabled={loading} className="w-full rounded-xl py-6 text-base">
        {loading ? "Saving..." : "Complete Setup"}
      </Button>
    </form>
  );
}
