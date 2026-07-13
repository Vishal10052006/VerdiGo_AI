/**
 * ============================================================================
 * Footer Component
 * ============================================================================
 *
 * Description:
 * Reusable footer component for VerdiGO.
 *
 * Module:
 * Phase 1 → Module 2 → Task 9
 *
 * Author:
 * VerdiGO Frontend Team
 * ============================================================================
 */

import Link from "next/link";

import {
    FaGithub,
    FaLinkedin,
    FaXTwitter,
} from "react-icons/fa6";

export function Footer() {
    return (
        <footer className="border-t bg-white">
            <div className="mx-auto flex max-w-7xl flex-col items-center gap-6 px-6 py-10">

                {/* Logo */}

                <h2 className="text-2xl font-bold text-green-600">
                    VerdiGO AI
                </h2>

                {/* Navigation */}

                <nav className="flex flex-wrap items-center justify-center gap-6 text-sm text-gray-600">

                    <Link href="/">
                        Home
                    </Link>

                    <Link href="/weather">
                        Weather
                    </Link>

                    <Link href="/marketplace">
                        Marketplace
                    </Link>

                    <Link href="/assistant">
                        AI Assistant
                    </Link>

                </nav>

                {/* Legal */}

                <nav className="flex flex-wrap items-center justify-center gap-6 text-sm text-gray-500">

                    <Link href="/privacy">
                        Privacy Policy
                    </Link>

                    <Link href="/terms">
                        Terms
                    </Link>

                </nav>

                {/* Social */}

                <div className="flex items-center gap-5 text-gray-600">

                    <FaGithub className="h-5 w-5" />
                    <FaLinkedin className="h-5 w-5" />
                    <FaXTwitter className="h-5 w-5" />

                </div>

                {/* Copyright */}

                <p className="text-sm text-gray-500">
                    © 2026 VerdiGO AI. All rights reserved.
                </p>

            </div>
        </footer>
    );
}