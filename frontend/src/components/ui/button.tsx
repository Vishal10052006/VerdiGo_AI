/**
 * ============================================================================
 * VerdiGO Button Component
 * ============================================================================
 *
 * Description:
 * Reusable button component built on top of shadcn/ui.
 *
 * Module:
 * Phase 1 → Module 2 → Task 3
 *
 * Author:
 * VerdiGO Frontend Team
 * ============================================================================
 */

import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import { Loader2 } from "lucide-react";

import { cn } from "@/lib/utils";

const buttonVariants = cva(
    "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-green-500 disabled:pointer-events-none disabled:opacity-50",
    {
        variants: {
            variant: {
                primary:
                    "bg-green-600 text-white hover:bg-green-700",

                secondary:
                    "bg-blue-600 text-white hover:bg-blue-700",

                outline:
                    "border border-gray-300 bg-white hover:bg-gray-100",

                ghost:
                    "hover:bg-gray-100",

                destructive:
                    "bg-red-600 text-white hover:bg-red-700",
            },

            size: {
                sm: "h-9 px-3",

                default: "h-10 px-4",

                lg: "h-11 px-8",

                icon: "h-10 w-10",
            },
        },

        defaultVariants: {
            variant: "primary",
            size: "default",
        },
    }
);

export interface ButtonProps
    extends React.ButtonHTMLAttributes<HTMLButtonElement>,
        VariantProps<typeof buttonVariants> {
    asChild?: boolean;
    loading?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
    (
        {
            className,
            variant,
            size,
            asChild = false,
            loading = false,
            children,
            disabled,
            ...props
        },
        ref
    ) => {
        const Comp = asChild ? Slot : "button";

        return (
            <Comp
                ref={ref}
                className={cn(buttonVariants({ variant, size, className }))}
                disabled={disabled || loading}
                {...props}
            >
                {loading && (
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                )}

                {children}
            </Comp>
        );
    }
);

Button.displayName = "Button";

export { Button, buttonVariants };