"use client";

import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

export default function CTA() {
  return (
    <section className="bg-emerald-600 py-24 text-white">

      <div className="mx-auto max-w-4xl px-6 text-center">

        <span className="rounded-full bg-white/20 px-4 py-2 text-sm font-medium">
          🚀 Join the Future of Agriculture
        </span>

        <h2 className="mt-6 text-5xl font-bold">
          Ready to Transform Your Farming?
        </h2>

        <p className="mx-auto mt-6 max-w-2xl text-lg text-emerald-100">
          Join VerdiGO and leverage Artificial Intelligence, weather insights,
          and smart analytics to improve productivity and maximize profits.
        </p>

        <div className="mt-10 flex flex-wrap justify-center gap-4">

          <Button
            size="lg"
            variant="secondary"
            className="rounded-xl"
          >
            Get Started
            <ArrowRight className="ml-2 h-4 w-4" />
          </Button>

          <Button
            size="lg"
            variant="outline"
            className="rounded-xl border-white bg-transparent text-white hover:bg-white hover:text-emerald-600"
          >
            Book Demo
          </Button>

        </div>

      </div>

    </section>
  );
}