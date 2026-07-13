"use client";

import { useState } from "react";

import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog";

import { Button } from "@/components/ui/button";

interface AppModalProps {
    trigger: string;
    title: string;
    description: string;
    children?: React.ReactNode;
    confirmText?: string;
    cancelText?: string;
    onConfirm?: () => void;
}

export function AppModal({
    trigger,
    title,
    description,
    children,
    confirmText = "Confirm",
    cancelText = "Cancel",
    onConfirm,
}: AppModalProps) {
    const [open, setOpen] = useState(false);

    const handleConfirm = () => {
        onConfirm?.();
        setOpen(false);
    };

    return (
        <Dialog
            open={open}
            onOpenChange={setOpen}
        >
            <DialogTrigger
                render={
                    <Button variant="destructive" />
                }
            >
                {trigger}
            </DialogTrigger>

            <DialogContent>
                <DialogHeader>
                    <DialogTitle>
                        {title}
                    </DialogTitle>

                    <DialogDescription>
                        {description}
                    </DialogDescription>
                </DialogHeader>

                {children}

                <DialogFooter>
                    <Button
                        variant="outline"
                        onClick={() => setOpen(false)}
                    >
                        {cancelText}
                    </Button>

                    <Button
                        variant="destructive"
                        onClick={() => {
                            onConfirm?.();
                            setOpen(false);
                        }}
                    >
                        {confirmText}
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
}