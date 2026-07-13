/**
 * ============================================================================
 * Loading Skeleton Component
 * ============================================================================
 *
 * Description:
 * Reusable loading skeletons for VerdiGO.
 *
 * Module:
 * Phase 1 → Module 2 → Task 11
 *
 * Author:
 * VerdiGO Frontend Team
 * ============================================================================
 */

import { Skeleton } from "@/components/ui/skeleton";

interface LoadingSkeletonProps {
    variant?: "card" | "table" | "profile" | "list";
}

export function LoadingSkeleton({
    variant = "card",
}: LoadingSkeletonProps) {
    switch (variant) {
        case "table":
            return (
                <div className="space-y-3">
                    {Array.from({ length: 5 }).map((_, index) => (
                        <Skeleton
                            key={index}
                            className="h-10 w-full rounded-lg"
                        />
                    ))}
                </div>
            );

        case "profile":
            return (
                <div className="flex items-center gap-4">
                    <Skeleton className="h-16 w-16 rounded-full" />

                    <div className="flex-1 space-y-2">
                        <Skeleton className="h-5 w-40" />
                        <Skeleton className="h-4 w-64" />
                    </div>
                </div>
            );

        case "list":
            return (
                <div className="space-y-4">
                    {Array.from({ length: 6 }).map((_, index) => (
                        <div
                            key={index}
                            className="flex items-center gap-3"
                        >
                            <Skeleton className="h-10 w-10 rounded-full" />
                            <Skeleton className="h-5 flex-1" />
                        </div>
                    ))}
                </div>
            );

        default:
            return (
                <div className="space-y-4 rounded-xl border p-6">
                    <Skeleton className="h-6 w-40" />
                    <Skeleton className="h-4 w-full" />
                    <Skeleton className="h-4 w-3/4" />
                    <Skeleton className="h-10 w-28" />
                </div>
            );
    }
}