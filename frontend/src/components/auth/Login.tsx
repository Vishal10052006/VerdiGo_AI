"use client";

import { useState } from "react";
import { Leaf } from "lucide-react";

import PhoneInput from "./PhoneInput";
import OTPVerification from "./OTPVerification";

export default function Login() {
  /**
   * Authentication Step
   *
   * phone -> User enters mobile number
   * otp   -> User enters OTP
   */
  const [step, setStep] = useState<"phone" | "otp">("phone");

  /**
   * Store user's mobile number
   * so OTP screen can use it.
   */
  const [mobile, setMobile] = useState("");

  /**
   * Called after OTP is sent successfully.
   */
  const handleOTPSent = (phone: string) => {
    setMobile(phone);
    setStep("otp");
  };

  return (
    <section className="flex min-h-screen items-center justify-center bg-gradient-to-br from-emerald-50 via-white to-green-50 px-6">
      <div className="grid w-full max-w-6xl gap-12 lg:grid-cols-2">
        {/* Left Side */}
        <div className="flex flex-col justify-center">
          <div className="inline-flex w-fit items-center gap-2 rounded-full bg-emerald-100 px-4 py-2 text-sm font-medium text-emerald-700">
            <Leaf className="h-4 w-4" />
            Secure Authentication
          </div>

          <h1 className="mt-8 text-5xl font-bold leading-tight">
            Welcome Back to
            <br />
            <span className="text-emerald-600">
              VerdiGO AI
            </span>
          </h1>

          <p className="mt-6 max-w-lg text-lg text-slate-600">
            Login securely using your mobile number.
            We use OTP-based authentication to keep your account safe.
          </p>
        </div>

        {/* Right Side */}
        <div className="rounded-3xl border bg-white p-10 shadow-xl">
          <h2 className="mb-8 text-3xl font-bold">
            Login
          </h2>

          {step === "phone" ? (
            <PhoneInput
              onSuccess={handleOTPSent}
            />
          ) : (
            <OTPVerification
              mobile={mobile}
            />
          )}
        </div>
      </div>
    </section>
  );
}