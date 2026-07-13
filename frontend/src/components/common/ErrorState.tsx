"use client";

import { Button } from "@/components/ui/button";

interface ErrorStateProps {
    title: string;
    description: string;
    actionLabel?: string;
    onAction?: () => void;
    icon?: React.ReactNode;
}

export function ErrorState({
    title,
    description,
    actionLabel,
    onAction,
    icon,
}: ErrorStateProps) {
    return (
        <div className="flex flex-col items-center justify-center rounded-xl border border-red-200 bg-red-50 p-12 text-center">

            <div className="mb-4 text-red-600">
                {icon}
            </div>

            <h2 className="text-2xl font-bold text-red-700">
                {title}
            </h2>

            <p className="mt-2 max-w-md text-red-500">
                {description}
            </p>

            {actionLabel && (
                <Button
                    variant="destructive"
                    className="mt-6"
                    onClick={onAction}
                >
                    {actionLabel}
                </Button>
            )}
        </div>
    );
}