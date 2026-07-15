"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";

import { sendOTP } from "@/services/auth.service";

/**
 * PhoneInput Component Props
 */
interface PhoneInputProps {
  /**
   * Triggered after OTP is sent successfully.
   */
  onSuccess: (mobile: string) => void;
}

export default function PhoneInput({
  onSuccess,
}: PhoneInputProps) {
  const [phone, setPhone] = useState("");
  const [loading, setLoading] = useState(false);

  /**
   * Request OTP
   */
  const handleRequestOTP = async () => {
    if (!phone) {
        toast.warning("Please enter your mobile number.");
        return;
    }

    try {
        setLoading(true);

        const response = await sendOTP(phone);

        console.log("OTP Response:", response);

        toast.success("OTP sent successfully.");

        /**
         * Notify parent component.
         */
        onSuccess(phone);

        /**
         * Notify parent component.
         */
        onSuccess(phone);
        } catch (error) {
            console.error("Send OTP Error:", error);

            toast.error("Unable to send OTP. Please try again.");
            } finally {
        setLoading(false);
        }
    };

  return (
    <div className="space-y-6">
      {/* Phone Label */}
      <div>
        <label className="mb-2 block text-sm font-medium text-slate-700">
          Mobile Number
        </label>

        <input
          type="tel"
          placeholder="+91 9876543210"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-emerald-500"
        />
      </div>

      {/* Request OTP Button */}
      <Button
        onClick={handleRequestOTP}
        disabled={loading}
        className="w-full rounded-xl py-6 text-base"
      >
        {loading ? "Sending..." : "Request OTP"}
      </Button>
    </div>
  );
}