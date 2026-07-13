"use client";

import {
  Leaf,
  Mail,
  Phone,
  MapPin,
} from "lucide-react";

import {
  FaGithub,
  FaInstagram,
} from "react-icons/fa";

export default function Footer() {
  return (
    <footer
      id="contact"
      className="border-t bg-slate-950 text-slate-300"
    >
      <div className="mx-auto max-w-7xl px-6 py-16">

        <div className="grid gap-12 md:grid-cols-2 lg:grid-cols-4">

          {/* Brand */}

          <div>

            <div className="flex items-center gap-3">

              <div className="rounded-xl bg-emerald-600 p-3">
                <Leaf className="h-6 w-6 text-white" />
              </div>

              <div>

                <h3 className="text-2xl font-bold text-white">
                  VerdiGO
                </h3>

                <p className="text-sm">
                  AI Agriculture Platform
                </p>

              </div>

            </div>

            <p className="mt-6 leading-7">
              Empowering farmers through Artificial Intelligence,
              weather intelligence and precision agriculture.
            </p>

          </div>

          {/* Quick Links */}

          <div>

            <h4 className="mb-5 text-lg font-semibold text-white">
              Quick Links
            </h4>

            <ul className="space-y-3">

              <li><a href="#hero" className="hover:text-emerald-400">Home</a></li>
              <li><a href="#features" className="hover:text-emerald-400">Features</a></li>
              <li><a href="#how-it-works" className="hover:text-emerald-400">How It Works</a></li>
              <li><a href="#about" className="hover:text-emerald-400">About</a></li>

            </ul>

          </div>

          {/* Contact */}

          <div>

            <h4 className="mb-5 text-lg font-semibold text-white">
              Contact
            </h4>

            <div className="space-y-4">

              <div className="flex items-center gap-3">
                <Mail className="h-5 w-5 text-emerald-400" />
                <span>verdigoai@gmail.com</span>
              </div>

              <div className="flex items-center gap-3">
                <Phone className="h-5 w-5 text-emerald-400" />
                <span>+91 9006784489</span>
              </div>

              <div className="flex items-center gap-3">
                <MapPin className="h-5 w-5 text-emerald-400" />
                <span>India</span>
              </div>

            </div>

          </div>

          {/* Social */}

          <div>

            <h4 className="mb-5 text-lg font-semibold text-white">
              Follow Us
            </h4>

            <div className="flex gap-4">

                <a
                    href="https://github.com/Vishal10052006/verdigo-ai"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="rounded-xl bg-slate-800 p-3 transition hover:bg-emerald-600"
                >
                    <FaGithub className="h-5 w-5" />
                </a>

                <a
                    href="https://instagram.com/verdigoai"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="rounded-xl bg-slate-800 p-3 transition hover:bg-emerald-600"
                >
                    <FaInstagram className="h-5 w-5" />
                </a>

            </div>

          </div>

        </div>

        <div className="mt-16 border-t border-slate-800 pt-8 text-center text-sm text-slate-500">
          © 2026 VerdiGO. All Rights Reserved.
        </div>

      </div>
    </footer>
  );
}