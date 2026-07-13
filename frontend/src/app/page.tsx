"use client";

import { Button } from "@/components/ui/button";
import { AppModal } from "@/components/common/AppModal";

import { toast } from "sonner";

export default function Home() {
    return (
        <main className="flex min-h-screen flex-col items-center justify-center gap-6">

            {/* Existing App Modal Demo */}
            <AppModal
                trigger="Delete Farm"
                title="Delete Farm"
                description="Are you sure you want to delete this farm? This action cannot be undone."
                confirmText="Delete"
                cancelText="Cancel"
                onConfirm={() => console.log("Deleted")}
            />

            {/* Toast Demo */}
            <div className="flex flex-wrap gap-4">

                <Button
                    onClick={() => {
                        console.log("Clicked");
                        toast.success("Farm added successfully!");
                    }}
                >
                    Success
                </Button>

                <Button
                    variant="destructive"
                    onClick={() => toast.error("Unable to add farm.")}
                >
                    Error
                </Button>

                <Button
                    variant="secondary"
                    onClick={() => toast.warning("Weather API is slow.")}
                >
                    Warning
                </Button>

                <Button
                    variant="outline"
                    onClick={() => toast.info("AI Assistant is thinking...")}
                >
                    Info
                </Button>

            </div>

        </main>
    );
}