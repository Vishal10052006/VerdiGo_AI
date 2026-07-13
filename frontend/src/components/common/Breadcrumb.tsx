"use client";

import Link from "next/link";

import {
    Breadcrumb as UIBreadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbList,
    BreadcrumbPage,
    BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";

interface BreadcrumbItemType {
    label: string;
    href?: string;
}

interface BreadcrumbProps {
    items: BreadcrumbItemType[];
}

export default function Breadcrumb({
    items,
}: BreadcrumbProps) {
    return (
        <UIBreadcrumb>
            <BreadcrumbList>
                {items.map((item, index) => {
                    const isLast = index === items.length - 1;

                    return (
                        <BreadcrumbItem key={item.label}>
                            {isLast ? (
                                <BreadcrumbPage>
                                    {item.label}
                                </BreadcrumbPage>
                            ) : (
                                <BreadcrumbLink href={item.href ?? "#"}>
                                    {item.label}
                                </BreadcrumbLink>
                            )}

                            {!isLast && <BreadcrumbSeparator />}
                        </BreadcrumbItem>
                    );
                })}
            </BreadcrumbList>
        </UIBreadcrumb>
    );
}