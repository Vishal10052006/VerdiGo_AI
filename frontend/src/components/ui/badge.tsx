/**
 * ============================================================================
 * Badge Component
 * ============================================================================
 *
 * Description:
 * Reusable Badge component for VerdiGO.
 *
 * Module:
 * Phase 1 → Module 2 → Task 6
 *
 * Author:
 * VerdiGO Frontend Team
 * ============================================================================
 */

import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

const badgeVariants = cva(
    "inline-flex items-center justify-center rounded-full font-medium transition-colors",
    {
        variants: {
            variant: {
                primary:
                    "bg-green-600 text-white",

                secondary:
                    "bg-blue-600 text-white",

                success:
                    "bg-emerald-100 text-emerald-700",

                warning:
                    "bg-yellow-100 text-yellow-800",

                danger:
                    "bg-red-100 text-red-700",

                outline:
                    "border border-gray-300 bg-white text-gray-700",
            },

            size: {
                sm: "px-2 py-0.5 text-xs",

                md: "px-3 py-1 text-sm",

                lg: "px-4 py-1.5 text-base",
            },
        },

        defaultVariants: {
            variant: "primary",
            size: "md",
        },
    }
);

export interface BadgeProps
    extends React.HTMLAttributes<HTMLSpanElement>,
        VariantProps<typeof badgeVariants> {}

export function Badge({
    className,
    variant,
    size,
    ...props
}: BadgeProps) {
    return (
        <span
            className={cn(
                badgeVariants({
                    variant,
                    size,
                }),
                className
            )}
            {...props}
        />
    );
}

export {
    badgeVariants,
};