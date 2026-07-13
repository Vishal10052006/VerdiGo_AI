/**
 * ============================================================================
 * Page Header Component
 * ============================================================================
 *
 * Description:
 * Reusable page header component for VerdiGO pages.
 *
 * Module:
 * Phase 1 → Module 2 → Task 10
 *
 * Author:
 * VerdiGO Frontend Team
 * ============================================================================
 */

import * as React from "react";

import { Button } from "@/components/ui/button";

interface PageHeaderProps {
    title: string;
    description?: string;
    icon?: React.ReactNode;

    actionLabel?: string;
    onAction?: () => void;
}

export function PageHeader({
    title,
    description,
    icon,
    actionLabel,
    onAction,
}: PageHeaderProps) {
    return (
        <header className="flex flex-col gap-4 border-b bg-white px-6 py-6 md:flex-row md:items-center md:justify-between">

            {/* Left */}

            <div className="flex items-start gap-4">

                {icon && (
                    <div className="rounded-lg bg-green-100 p-3 text-green-600">
                        {icon}
                    </div>
                )}

                <div>
                    <h1 className="text-3xl font-bold text-gray-900">
                        {title}
                    </h1>

                    {description && (
                        <p className="mt-1 text-gray-500">
                            {description}
                        </p>
                    )}
                </div>

            </div>

            {/* Right */}

            {actionLabel && (
                <Button>
                    {actionLabel}
                </Button>
            )}

        </header>
    );
}