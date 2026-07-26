"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Leaf } from "lucide-react";
import { GoogleLogin, CredentialResponse } from "@react-oauth/google";
import { toast } from "sonner";

import PhoneInput from "./PhoneInput";
import OTPVerification from "./OTPVerification";
import { googleLogin } from "@/services/auth.service";
import { routeAfterLogin } from "@/lib/postLogin";

export default function Login() {
  const router = useRouter();

  const [step, setStep] = useState<"phone" | "otp">("phone");
  const [mobile, setMobile] = useState("");
  const [googleLoading, setGoogleLoading] = useState(false);

  const handleOTPSent = (phone: string) => {
    setMobile(phone);
    setStep("otp");
  };

  const handleGoogleSuccess = async (credentialResponse: CredentialResponse) => {
    if (!credentialResponse.credential) {
      toast.error("Google sign-in failed. Please try again.");
      return;
    }

    setGoogleLoading(true);

    try {
      const response = await googleLogin(credentialResponse.credential);

      localStorage.setItem("access_token", response.access_token);
      localStorage.setItem("refresh_token", response.refresh_token);
      localStorage.setItem("user", JSON.stringify(response.user));

      await routeAfterLogin(router);
    } catch (error) {
      console.error("Google login error:", error);
      toast.error("Unable to sign in with Google. Please try again.");
    } finally {
      setGoogleLoading(false);
    }
  };

  return (
    <section className="flex min-h-screen items-center justify-center bg-gradient-to-br from-emerald-50 via-white to-green-50 px-6">
      <div className="grid w-full max-w-6xl gap-12 lg:grid-cols-2">
        <div className="flex flex-col justify-center">
          <div className="inline-flex w-fit items-center gap-2 rounded-full bg-emerald-100 px-4 py-2 text-sm font-medium text-emerald-700">
            <Leaf className="h-4 w-4" />
            Secure Authentication
          </div>

          <h1 className="mt-8 text-5xl font-bold leading-tight">
            Welcome Back to
            <br />
            <span className="text-emerald-600">VerdiGO AI</span>
          </h1>

          <p className="mt-6 max-w-lg text-lg text-slate-600">
            Login securely using your mobile number or Google account.
          </p>
        </div>

        <div className="rounded-3xl border bg-white p-10 shadow-xl">
          <h2 className="mb-8 text-3xl font-bold">Login</h2>

          <div className="mb-6">
            <div className={googleLoading ? "pointer-events-none opacity-50" : ""}>
              <GoogleLogin
                onSuccess={handleGoogleSuccess}
                onError={() => toast.error("Google sign-in failed. Please try again.")}
                width="100%"
                text="continue_with"
                shape="pill"
              />
            </div>
          </div>

          <div className="mb-6 flex items-center gap-4">
            <div className="h-px flex-1 bg-slate-200" />
            <span className="text-xs font-medium uppercase text-slate-400">or</span>
            <div className="h-px flex-1 bg-slate-200" />
          </div>

          {step === "phone" ? (
            <PhoneInput onSuccess={handleOTPSent} />
          ) : (
            <OTPVerification mobile={mobile} />
          )}
        </div>
      </div>
    </section>
  );
}
