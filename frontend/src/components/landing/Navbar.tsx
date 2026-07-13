"use client";

import { Button } from "@/components/ui/button";
import { Leaf, Menu } from "lucide-react";

export default function Navbar() {
  return (
    <header className="fixed top-0 z-50 w-full border-b border-emerald-100/50 bg-white/80 backdrop-blur-xl">
      <div className="mx-auto flex h-20 max-w-7xl items-center justify-between px-6">

        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-600">
            <Leaf className="h-6 w-6 text-white" />
          </div>

          <div>
            <h2 className="text-xl font-bold">
              Verdi<span className="text-emerald-600">GO</span>
            </h2>

            <p className="text-xs text-muted-foreground">
              AI Agriculture Platform
            </p>
          </div>
        </div>

        {/* Desktop Navigation */}
        <nav className="hidden items-center gap-10 lg:flex">
          <a
            href="#hero"
            className="font-medium transition hover:text-emerald-600"
          >
            Home
          </a>

          <a
            href="#features"
            className="font-medium transition hover:text-emerald-600"
          >
            Features
          </a>

          <a
            href="#how-it-works"
            className="font-medium transition hover:text-emerald-600"
          >
            How It Works
          </a>

          <a
            href="#about"
            className="font-medium transition hover:text-emerald-600"
          >
            About
          </a>

          <a
            href="#contact"
            className="font-medium transition hover:text-emerald-600"
          >
            Contact
          </a>
        </nav>

        {/* Right */}
        <div className="flex items-center gap-4">

          <Button className="hidden rounded-xl lg:flex">
            Get Started
          </Button>

          <button className="lg:hidden">
            <Menu className="h-7 w-7" />
          </button>

        </div>
      </div>
    </header>
  );
}