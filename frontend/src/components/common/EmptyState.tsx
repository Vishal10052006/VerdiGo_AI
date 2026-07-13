"use client";

import { Button } from "@/components/ui/button";

interface EmptyStateProps {
    title: string;
    description: string;
    actionLabel?: string;
    onAction?: () => void;
    icon?: React.ReactNode;
}

export function EmptyState({
    title,
    description,
    actionLabel,
    onAction,
    icon,
}: EmptyStateProps) {
    return (
        <div className="flex flex-col items-center justify-center rounded-xl border border-dashed p-12 text-center">
            <div className="mb-4 text-green-600">
                {icon}
            </div>

            <h2 className="text-2xl font-bold">
                {title}
            </h2>

            <p className="mt-2 max-w-md text-gray-500">
                {description}
            </p>

            {actionLabel && (
                <Button
                    className="mt-6"
                    onClick={onAction}
                >
                    {actionLabel}
                </Button>
            )}
        </div>
    );
}