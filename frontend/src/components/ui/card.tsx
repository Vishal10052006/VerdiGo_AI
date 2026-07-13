/**
 * ============================================================================
 * Card Component
 * ============================================================================
 *
 * Description:
 * Reusable Card component for VerdiGO.
 *
 * Module:
 * Phase 1 → Module 2 → Task 4
 *
 * Author:
 * VerdiGO Frontend Team
 * ============================================================================
 */

import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";


const cardVariants = cva(
    "rounded-xl transition-all duration-200",
    {
        variants: {
            variant: {
                default:
                    "bg-white border border-gray-200",

                outlined:
                    "border-2 border-green-600 bg-white",

                elevated:
                    "bg-white shadow-lg",

                success:
                    "bg-green-50 border border-green-300",

                warning:
                    "bg-yellow-50 border border-yellow-300",

                danger:
                    "bg-red-50 border border-red-300",
            },

            size: {
                sm: "p-4",

                md: "p-6",

                lg: "p-8",
            },
        },

        defaultVariants: {
            variant: "default",
            size: "md",
        },
    }
);

export interface CardProps
    extends React.HTMLAttributes<HTMLElement>,
        VariantProps<typeof cardVariants> {}

export function Card({
    className,
    variant,
    size,
    ...props
}: CardProps) {
    return (
        <article
            className={cn(
                cardVariants({
                    variant,
                    size,
                }),
                className
            )}
            {...props}
        />
    );
}

export function CardHeader({
    className,
    ...props
}: React.HTMLAttributes<HTMLDivElement>) {
    return (
        <div
            className={cn(
                "mb-4 flex flex-col gap-1",
                className
            )}
            {...props}
        />
    );
}

export function CardTitle({
    className,
    ...props
}: React.HTMLAttributes<HTMLHeadingElement>) {
    return (
        <h3
            className={cn(
                "text-lg font-semibold",
                className
            )}
            {...props}
        />
    );
}

export function CardDescription({
    className,
    ...props
}: React.HTMLAttributes<HTMLParagraphElement>) {
    return (
        <p
            className={cn(
                "text-sm text-gray-500",
                className
            )}
            {...props}
        />
    );
}

export function CardContent({
    className,
    ...props
}: React.HTMLAttributes<HTMLDivElement>) {
    return (
        <div
            className={cn(className)}
            {...props}
        />
    );
}

export function CardFooter({
    className,
    ...props
}: React.HTMLAttributes<HTMLDivElement>) {
    return (
        <div
            className={cn(
                "mt-4 flex items-center justify-end",
                className
            )}
            {...props}
        />
    );
}

export {
    cardVariants,
};