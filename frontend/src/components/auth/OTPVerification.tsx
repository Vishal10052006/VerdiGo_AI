"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

import {
  verifyOTP,
  sendOTP,
} from "@/services/auth.service";

interface OTPVerificationProps {
  /**
   * Mobile number to verify.
   */
  mobile: string;
}

export default function OTPVerification({
  mobile,
}: OTPVerificationProps) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const [otp, setOtp] = useState(["", "", "", "", "", ""]);

  /**
   * OTP Countdown Timer (30 seconds)
   */
  const [timeLeft, setTimeLeft] = useState(30);

  /**
   * Controls Resend OTP button state.
   */
  const [resending, setResending] = useState(false);

  /**
   * Countdown timer.
   */
  useEffect(() => {
    /**
     * Stop timer at zero.
     */
    if (timeLeft <= 0) {
      return;
    }

    /**
     * Decrease timer every second.
     */
    const timer = setInterval(() => {
      setTimeLeft((previousTime) => previousTime - 1);
    }, 1000);

    /**
     * Cleanup interval.
     */
    return () => clearInterval(timer);

  }, [timeLeft]);

  const handleChange = (value: string, index: number) => {
    if (!/^\d?$/.test(value)) return;

    const updated = [...otp];
    updated[index] = value;
    setOtp(updated);

    if (value && index < 5) {
      const next = document.getElementById(
        `otp-${index + 1}`
      ) as HTMLInputElement;

      next?.focus();
    }
  };

  /**
   * Verify OTP
   */
  const handleVerifyOTP = async () => {
    const otpCode = otp.join("");

    if (otpCode.length !== 6) {
      toast.warning("Enter a valid 6-digit OTP.");
      return;
    }

    try {
      setLoading(true);

      const response = await verifyOTP(
          mobile,
          otpCode
      );

      console.log("Verify OTP Response:", response);

      /**
       * Store authentication tokens.
       */
      localStorage.setItem(
        "access_token",
        response.access_token
      );

      localStorage.setItem(
        "refresh_token",
        response.refresh_token
      );

      /**
       * Store authenticated user.
       */
      localStorage.setItem(
        "user",
        JSON.stringify(response.user)
      );

      /**
       * Navigate to dashboard.
       */
      router.push("/dashboard");

    } catch (error) {
      console.error(error);

      toast.error("Invalid OTP.");
    } finally {
      setLoading(false);
    }
  };


  /**
   * Request a new OTP.
   */
  const handleResendOTP = async () => {
    /**
     * Prevent resend before timer ends.
     */
    if (timeLeft > 0) {
      return;
    }

    try {
      setResending(true);

      await sendOTP(mobile);

      /**
       * Restart countdown.
       */
      setTimeLeft(30);

      toast.success("OTP sent successfully.");

    } catch (error) {
      console.error(error);

      toast.error("Unable to resend OTP.");

    } finally {
      setResending(false);
    }
  };

  return (
    <div className="space-y-8">

      {/* Heading */}

      <div>

        <h2 className="text-3xl font-bold">
          Verify OTP
        </h2>

        <p className="mt-2 text-slate-600">
          Enter the 6-digit code sent to your mobile number.
        </p>

      </div>

      {/* OTP Boxes */}

      <div className="flex justify-between gap-3">

        {otp.map((digit, index) => (

          <input
            key={index}
            id={`otp-${index}`}
            type="text"
            maxLength={1}
            value={digit}
            onChange={(e) =>
              handleChange(e.target.value, index)
            }
            className="h-16 w-16 rounded-xl border text-center text-2xl font-bold outline-none transition focus:border-emerald-500"
          />

        ))}

      </div>

      {/* Timer */}

      <div className="flex items-center justify-between">

        <p className="text-slate-500">
          OTP expires in
          <span className="ml-2 font-semibold text-emerald-600">
            {`00:${String(timeLeft).padStart(2, "0")}`}
          </span>
        </p>

        <button
          onClick={handleResendOTP}
          disabled={timeLeft > 0 || resending}
          className={`text-sm font-medium ${
            timeLeft > 0
              ? "cursor-not-allowed text-gray-400"
              : "text-emerald-600 hover:underline"
          }`}
        >
          {resending ? "Sending..." : "Resend OTP"}
        </button>

      </div>

      {/* Verify */}

      <Button
          onClick={handleVerifyOTP}
          disabled={loading}
          className="w-full rounded-xl py-6 text-base"
      >
          {loading ? "Verifying..." : "Verify OTP"}
      </Button>

    </div>
  );
}